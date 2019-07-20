from models import Model
from models.base_model import SQLModel
from models.comment import Comment
from utils import log


class Todo(SQLModel):
    """
    针对我们的数据 TODO
    我们要做 4 件事情
    C create 创建数据
    R read 读取数据
    U update 更新数据
    D delete 删除数据

    Todo.new() 来创建一个 todo
    """

    sql_create = '''
                CREATE TABLE `todo` (
                    `id`        INT NOT NULL AUTO_INCREMENT,
                    `title`  VARCHAR(255) NOT NULL,
                    `user_id`  INT NOT NULL,
                    PRIMARY KEY (`id`)
                );
                '''

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        log('todo_form:', form)
        Todo.insert(form)


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
