from flask import render_template, request, Blueprint
from sqlalchemy.orm import lazyload, load_only, defer

from flaskblog import db, fake
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    # posts= Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    post2=Post.query.count()
    post3=Post.query.all()
    return "<body><h1>data"+str(post2)+str(len(post3))+"</body></h1>"
    # return render_template('home.html', posts=posts)

@main.route('/insert_data_with_bulk')
def insert_with_bulk():
    """
    will have 1 insert operation
    :return: html template showing data added content
    """
    count = 0
    save_user = []
    for i in range(100):
        count = count + 1
        new_person = Post(title=fake.email(),date_posted=fake.date(),content=fake.phone_number(),user_id=1)
        save_user.append(new_person)
    db.session.bulk_save_objects(save_user)
    db.session.commit()
    return "<body><h1>data  added</body></h1>"

@main.route('/insert_data_without_bulk')
def insert_without_bulk():
    """
    will have 100 insert operations
    :return: html template showing data added content
    """
    count = 0
    for i in range(100):
        count = count + 1
        new_person = Post(title=fake.email(),date_posted=fake.date(),content=fake.phone_number(),user_id=1)
        db.session.add(new_person)
        db.session.commit()
    return "<body><h1>data  added</h1></body>"

def post_queries():
    Post.query.options(load_only("title", "date_posted","content","user_id")).order_by(Post.date_posted.desc())
    Post.query.with_entities(Post.title,Post.date_posted,Post.content,Post.user_id).order_by(Post.date_posted.desc())
    """
    There are a few differences between load_only and with_entities. The most important one when discarding unwanted columns (as in the question) is that using load_only will still result in creation of an object (a Model instance), while using with_entities will just get you tuples with values of chosen columns.
    """
    Post.query.options(defer("title")).order_by(Post.date_posted.desc())
    """
    This feature is useful when one wants to avoid loading a large text or binary field into memory when it's not needed
    """





@main.route("/about")
def about():
    return render_template('about.html', title='About')