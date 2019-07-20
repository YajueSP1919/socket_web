from werkzeug.datastructures import ImmutableMultiDict

from models.todo import Todo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


from flask import (
    flash,
    session,
    request,
    redirect,
    Blueprint,
    render_template,
    current_app
)

bp = Blueprint('todo',__name__)

@bp.route('/todo/index')
def index():
    """
    todo 首页的路由函数
    """
    u = current_user()
    todos = Todo.all(user_id=u.id)
    # 替换模板文件中的标记字符串
    return render_template('todo_index.html', todos=todos)

@bp.route('/todo/add', methods=['POST'])
def add():
    """
    用于增加新 todo 的路由函数
    """
    u = current_user()
    form: ImmutableMultiDict = request.form
    Todo.add(form.to_dict(), u.id)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo/index')


@bp.route('/todo/delete')
def delete():
    todo_id = int(request.args['id'])
    Todo.delete(todo_id)
    return redirect('/todo/index')

@bp.route('/todo/edit')
def edit():
    todo_id = int(request.args['id'])
    t = Todo.one(id=todo_id)
    return render_template('todo_edit.html', todo=t)


@bp.route('/todo/update', methods=['POST'])
def update():
    """
    用于增加新 todo 的路由函数
    """
    form: ImmutableMultiDict = request.form
    log('request_form', form)
    log('form_to_dict', form.to_dict())
    Todo.update(form)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo/index')


def same_user_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f(request):
        log('same_user_required')
        u = current_user(request)
        if 'id' in request.query:
            todo_id = request.query['id']
        else:
            todo_id = request.form()['id']
        t = Todo.one(id=int(todo_id))

        if t.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/todo/index')

    return f


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/todo/add': login_required(add),
        '/todo/delete': login_required(same_user_required(delete)),
        '/todo/edit': login_required(same_user_required(edit)),
        '/todo/update': login_required(same_user_required(update)),
        '/todo/index': login_required(index),
    }
    return d
