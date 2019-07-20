import time

from flask import (
    request,
    Blueprint,
    render_template
)

from routes import (
    current_user,
    login_required
)
from utils import log

bp = Blueprint('public', __name__)


@bp.route('/')
# @login_required
def index():
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user()
    return render_template('index.html', username=u.username, current_time=time.time())
    # return render_template('index.html', username=u.username)
