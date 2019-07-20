from werkzeug.datastructures import ImmutableMultiDict

from models.comment import Comment
from models.user import User
from models.weibo import Weibo
from routes import (
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

bp = Blueprint('weibo',__name__)

@bp.route('/weibo/index')
def index():
    """
    weibo 首页的路由函数
    """
    u = current_user()
    weibos = Weibo.all(user_id=u.id)
    # 替换模板文件中的标记字符串
    return render_template('weibo_index.html', weibos=weibos, user=u)

@bp.route('/weibo/add', methods=['POST'])
def add():
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user()
    form: ImmutableMultiDict = request.form
    Weibo.add(form.to_dict(), u.id)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')

@bp.route('/weibo/delete')
def delete():
    weibo_id = int(request.args['id'])
    Weibo.delete(weibo_id)
    # 注意删除所有微博对应评论
    cs = Comment.all(weibo_id=weibo_id)
    for c in cs:
        c.delete(c.id)
    return redirect('/weibo/index')

@bp.route('/weibo/edit')
def edit():
    weibo_id = int(request.args['id'])
    log('request_args',request.args)
    w = Weibo.one(id=weibo_id)
    log('w:',w)
    return render_template('weibo_edit.html', weibo=w)

@bp.route('/weibo/update', methods=['POST'])
def update():
    """
    用于增加新 weibo 的路由函数
    """
    form: ImmutableMultiDict = request.form
    log('request_form',form)
    log('form_to_dict',form.to_dict())
    #Weibo.update无法直接获取form.to_dict的值，前面需要加2个星号才行
    Weibo.update(**form.to_dict())
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')

@bp.route('/comment/add', methods=['POST'])
def comment_add():
    u = current_user()
    form: ImmutableMultiDict = request.form
    form = form.to_dict()
    weibo_id = int(form['weibo_id'])

    c = form
    c['user_id']= u.id
    c['weibo_id']= weibo_id
    Comment.insert(c)

    # c = Comment(form)
    # c.user_id = u.id
    # c.weibo_id = weibo_id
    # c.save()

    log('comment add', c, u, form)
    return redirect('/weibo/index')

@bp.route('/comment/delete')
def comment_delete():
    # 删除评论
    # 判断当前用户是否有权限
    comment_id = int(request.args['id'])
    # 只有评论用户和评论所属的微博的用户都能删除评论
    Comment.delete(comment_id)
    return redirect('/weibo/index')

@bp.route('/comment/edit')
def comment_edit():
    comment_id = int(request.args['id'])
    c = Comment.one(id=comment_id)
    log('comment_edit:', c)
    return render_template('comment_edit.html', comment=c)

@bp.route('/comment/update', methods=['POST'])
def comment_update():
    log('comment update')
    form = request.form
    form: ImmutableMultiDict = form.to_dict()
    log('updated comment form', form)
    Comment.update(**form)
    # 重定向到用户的主页
    return redirect('/weibo/index')


def weibo_owner_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f(request):
        log('weibo_owner_required')
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        w = Weibo.find_by(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/weibo/add':  login_required(add),
        '/weibo/delete':  login_required(delete),
        '/weibo/edit':  login_required(edit),
        '/weibo/update':  login_required(update),
        '/weibo/index':  login_required(index),
        # 评论功能
        '/comment/add':  login_required(comment_add),
        '/comment/delete': login_required(comment_delete),
        '/comment/edit': login_required(comment_edit),
        '/comment/update': login_required(comment_update),
    }
    return d
