from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flaskblog import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy="select")#select=1.23ms,joined=10.30ms,true=0.71
    """
    lazy=select
    time=1.4970ms
    query:SELECT "user".id AS user_id, "user".username AS user_username, "user".email AS user_email, "user".image_file AS user_image_file, "user".password AS user_password FROM "user"
    output:
    [Post('First Posst', '2022-08-26 08:04:07.747359'), Post('noahcurtis@example.org', '1994-03-28 00:00:00'), Post('jamesjohnson@example.net', '2000-10-13 00:00:00'), Post('ikirby@example.com', '1998-02-14 00:00:00'), Post('hayesjennifer@example.com', '1991-09-06 00:00:00'), Post('wolfenathan@example.org', '2020-05-01 00:00:00'), Post('haley57@example.com', '2004-03-28 00:00:00'), Post('beverlycastillo@example.com', '2019-10-20 00:00:00')]

    
    lazy=dynamic
    time=0.6900ms
    query:SELECT "user".id AS user_id, "user".username AS user_username, "user".email AS user_email, "user".image_file AS user_image_file, "user".password AS user_password FROM "user"
    input:User.query.all()
    output:
    SELECT post.id AS post_id, post.title AS post_title, post.date_posted AS post_date_posted, post.content AS post_content, post.user_id AS post_user_id FROM post WHERE %(param_1)s = post.user_id
    
    
    lazy=joined
    time=5.8527ms
    query:SELECT "user".id AS user_id, "user".username AS user_username, "user".email AS user_email, "user".image_file AS user_image_file, "user".password AS user_password, post_1.id AS post_1_id, post_1.title AS post_1_title, post_1.date_posted AS post_1_date_posted, post_1.content AS post_1_content, post_1.user_id AS post_1_user_id FROM "user" LEFT OUTER JOIN post AS post_1 ON "user".id = post_1.user_id
    input:User.query.all()
    output:
    [Post('First Posst', '2022-08-26 08:04:07.747359'), Post('noahcurtis@example.org', '1994-03-28 00:00:00'), Post('jamesjohnson@example.net', '2000-10-13 00:00:00'), Post('ikirby@example.com', '1998-02-14 00:00:00'), Post('hayesjennifer@example.com', '1991-09-06 00:00:00'), Post('wolfenathan@example.org', '2020-05-01 00:00:00'), Post('haley57@example.com', '2004-03-28 00:00:00'), Post('beverlycastillo@example.com', '2019-10-20 00:00:00'), Post('michael92@example.com', '1971-12-14 00:00:00'), Post('christie70@example.net', '2018-12-10 00:00:00'), Post('steve46@example.net', '1990-09-08 00:00:00')]
    """

    """
    lazy=selectin
    total 2 queries:
    time 1: 0.8368 ms
    time 2: 5.4226 ms
    input:User.query.all()
    query 1:SELECT "user".id AS user_id, "user".username AS user_username, "user".email AS user_email, "user".image_file AS user_image_file, "user".password AS user_password FROM "user"
    query 2:SELECT post.user_id AS post_user_id, post.id AS post_id, post.title AS post_title, post.date_posted AS post_date_posted, post.content AS post_content FROM post WHERE post.user_id IN (%(primary_keys_1)s)
    output:
    [Post('First Posst', '2022-08-26 08:04:07.747359'), Post('noahcurtis@example.org', '1994-03-28 00:00:00'), Post('jamesjohnson@example.net', '2000-10-13 00:00:00'), Post('ikirby@example.com', '1998-02-14 00:00:00'), Post('hayesjennifer@example.com', '1991-09-06 00:00:00'), Post('wolfenathan@example.org', '2020-05-01 00:00:00'), Post('haley57@example.com', '2004-03-28 00:00:00'), Post('beverlycastillo@example.com', '2019-10-20 00:00:00'), Post('michael92@example.com', '1971-12-14 00:00:00'), Post('christie70@example.net', '2018-12-10 00:00:00'), Post('steve46@example.net', '1990-09-08 00:00:00')]
    """
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

