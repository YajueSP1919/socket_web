from models import Model
from models.base_model import SQLModel
from models.comment import Comment
from utils import log


class Weibo(SQLModel):
    """
    微博类
    """
    sql_create = '''
            CREATE TABLE `weibo` (
                `id`        INT NOT NULL AUTO_INCREMENT,
                `content`  VARCHAR(255) NOT NULL,
                `user_id`  INT NOT NULL,
                PRIMARY KEY (`id`)
            );
            '''

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        log('weibo_form:',form)
        Weibo.insert(form)
        # w = Weibo(form)
        # log('w:',w)
        # w.user_id = user_id
        # log('w2:',w)
        # w.save()

    @classmethod
    def update(cls, id, **kwargs):
        # UPDATE
        #     `User`
        # SET
        #     `username`=%s, `password`=%s
        # WHERE `id`=%s;
        log('update kwargs', kwargs)
        sql_set = ', '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        log('update sql_set', sql_set)
        sql_update = 'UPDATE {} SET {} WHERE `id`=%s'.format(
            cls.table_name(),
            sql_set,
        )
        log('ORM update <{}>'.format(sql_update.replace('\n', ' ')))

        values = list(kwargs.values())
        values.append(id)
        values = tuple(values)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_update, values)
        cls.connection.commit()

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs