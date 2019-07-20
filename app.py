import socket
import _thread
import time

from flask import Flask
#
# from request import Request
# from utils import log
#
from models.base_model import SQLModel
#
# from routes import error
#
# from routes.routes_todo import route_dict as todo_routes
# from routes.routes_weibo import route_dict as weibo_routes
# from routes.routes_user import route_dict as user_routes
from routes.routes_public import bp as public_bp
from routes.routes_user import bp as user_bp
from routes.routes_weibo import bp as weibo_bp
from routes.routes_todo import bp as todo_bp
from secret import secret_key
from utils import log

app = Flask(__name__)
app.register_blueprint(public_bp)
app.register_blueprint(user_bp)
app.register_blueprint(weibo_bp)
app.register_blueprint(todo_bp)
app.secret_key = secret_key
SQLModel.init_db()

@app.errorhandler(404)
def error_view(error):
    return '自定义404'


@app.context_processor
def current_time():
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    return dict(current_time=formatted)


@app.template_filter('formatted_time')
def formatted_time(value):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(value))
    formatted = time.strftime(time_format, localtime)
    return formatted


if __name__ == '__main__':
    
    # 生成配置并且运行程序
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=3000,
    )
    
    log('url_map', app.url_map)
    app.run(**config)
