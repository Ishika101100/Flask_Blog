# Flask Blog App 

***

## Setup

``` 
git clone REPOSITORY_URL
cd FOLDER_NAME
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
```

It should throw errors for database as we have not yet integrated database with it. So let's do that.

### 1. Install Postgres

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" >
/etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add
sudo apt-get update
sudo apt-get -y install postgresql # You can define specific version here

Please refer these links for more information

    https://www.postgresql.org/download/linux/ubuntu/	
    https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

***

### 2. Creating a database

* You should be able to create a database in postgres using createdb command, the database name you can keep it as you
  want. This database connection details is to be stored in .env file where we will store secrets. This file is in
  gitognore (What's the meaning of adding it in git, It's Top secret ;) )

``` 
DEVELOPMENT_DB_URL='postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{DATABASE_NAME}'
```


### 3. Set below variable

* You can set this variable directly to your terminal(you need to set it with every new terminal)
* or you can set it in .env file
* for information about debug mode https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling in this refer Debug Mode part 
* Also set all required variable(shown in .exapmle-env) in .env 

```
export FLASK_APP=run.py
export FLASK_DEBUG=True
FLASK_ENV=development
```

### 4. Migration
* In Detail It has given below.
* Run migrations command to migrate our models(Flask-Migrate Expalin below)
* Optinally, You can define db.create_all() in your application context like below

### 5. Run Below command in terminal
```
flask run
```

# Packages Used

These are the packages which are most-commonly used in a flask project based on API.

### Flask

- <a href="https://flask.palletsprojects.com/en/2.2.x/" target="_blank">Package Link</a>
- It is an extension for Flask that adds support for quickly building REST APIs.

### Flask-SQLAlchemy

- <a href="https://flask-sqlalchemy.palletsprojects.com/en/2.x/" target="_blank">Package Link</a>
- It provides support for SQLAlchemy and ORM using SQL databases like sqlite, mysql, postgres, oracle.

### Flask-Migrate

- <a href="https://flask-migrate.readthedocs.io/en/latest/" target="_blank">Package Link</a>
- Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.


### Flask-Bcrypt

- <a href="https://flask-bcrypt.readthedocs.io/en/latest/" target="_blank">Package Link</a>
- It is used to serializing and deserialize


### Flask-Mail

- <a href="https://pythonhosted.org/Flask-Mail/" target="_blank">Package Link</a>
- It is used for sending email with flask

### python-dotenv

- <a href="https://pypi.org/project/python-dotenv/" target="_blank">Package Link</a>
- It would be annoying to set environment variables every time we open our terminal, so we can set environment variables in a local file called .env instead and grab those variables using a Python library like python-dotenv.


# Database and Migration

## Flask-SQLAlchemy

- For most of the  relational database(in our case postgresql) connection in a flask application we can use Flask-SQLAlchemy Package. 
- It provides support for sqlalchemy and ORM using SQL databases like sqlite, mysql, postgres, oracle.
- It also provides support for ORM.

- For creating tables from models we have a command


```
from yourapplication import db
db.create_all()
```


## Flask-Migrate

- To use it we have very simple step as below:

```
  flask db init
  flask db migrate -m "Message related to change"
  flask db upgrade
```

  
- First command will create a directory named Migrations. That need to be on version control, to detect every change in the future.
- Second command will create a python script(you can see it inside migrations/versions directory) that refers to the changes. That also needs to be on version control.
- Third will update the latest changes on to the database.
- In __init__.py crete migrate object and initialize it with db and app instance
commandline

```
db = SQLAlchemy()
migrate = Migrate()

migrate.init_app(app=app, db=db) #inside create_app()
```

## Query Optimization 
- There are a few differences between load_only and with_entities. The most important one when discarding unwanted columns (as in the question) is that using load_only will still result in creation of an object (a Model instance), while using with_entities will just get you tuples with values of chosen columns.
- for example:
```
Post.query.options(load_only("title", "date_posted","content","user_id")).order_by(Post.date_posted.desc()) #returns model instance
Post.query.with_entities(Post.title,Post.date_posted,Post.content,Post.user_id).order_by(Post.date_posted.desc()) # returns tuple
```
- defer is useful when one wants to avoid loading a large text or binary field into memory when it's not needed
- for example:
```
Post.query.options(defer("title")).order_by(Post.date_posted.desc())
```
- count() will take less time for execution as query is executed at database level and returns int value from database
- for example:
```
Post.query.count()
```
- len(all())will take more time as it returns a list of all details of table and then calculates length of list
- for example:
```
len(Post.query.all())
```

## Relationship Loading
- The primary forms of relationship loading are: 
- Consider following example for understanding of relationship:
```
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy="select")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```
### 1. lazy loading 
- available via "select" (or True) or the lazyload() option, this is the form of loading that emits a SELECT statement at attribute access time to lazily load a related reference on a single object at a time. 
- By default, all inter-object relationships are lazy loading. The scalar or collection attribute associated with a relationship() contains a trigger which fires the first time the attribute is accessed. 
- Time, query and output when we add lazy = "select" (or True):
```
lazy=select
    time=1.4970ms
    query:SELECT "user".id AS user_id, "user".username AS user_username, "user".email AS user_email, "user".image_file AS user_image_file, "user".password AS user_password FROM "user"
    output:
    [Post('First Posst', '2022-08-26 08:04:07.747359'), Post('noahcurtis@example.org', '1994-03-28 00:00:00'), Post('jamesjohnson@example.net', '2000-10-13 00:00:00'), Post('ikirby@example.com', '1998-02-14 00:00:00'), Post('hayesjennifer@example.com', '1991-09-06 00:00:00'), Post('wolfenathan@example.org', '2020-05-01 00:00:00'), Post('haley57@example.com', '2004-03-28 00:00:00'), Post('beverlycastillo@example.com', '2019-10-20 00:00:00')]
```

### 2. joined loading
- available via lazy='joined' or the joinedload() option, this form of loading applies a JOIN to the given SELECT statement so that related rows are loaded in the same result set.
- Joined eager loading is the most fundamental style of eager loading in the ORM. It works by connecting a JOIN (by default a LEFT OUTER join) to the SELECT statement emitted by a Query and populates the target scalar/collection from the same result set as that of the parent.
- Time, query and output when we add lazy = "joined":
```
lazy=dynamic
    time=0.6900ms
    query:SELECT "user".id AS user_id, "user".username AS user_username, "user".email AS user_email, "user".image_file AS user_image_file, "user".password AS user_password FROM "user"
    input:User.query.all()
    output:
    SELECT post.id AS post_id, post.title AS post_title, post.date_posted AS post_date_posted, post.content AS post_content, post.user_id AS post_user_id FROM post WHERE %(param_1)s = post.user_id
```

### 3. select IN loading 
- available via lazy='selectin' or the selectinload() option, this form of loading emits a second (or more) SELECT statement which assembles the primary key identifiers of the parent objects into an IN clause, so that all members of related collections / scalar references are loaded at once by primary key.
- Select IN loading is similar in operation to subquery eager loading, however the SELECT statement which is emitted has a much simpler structure than that of subquery eager loading. In most cases, selectin loading is the most simple and efficient way to eagerly load collections of objects. The only scenario in which selectin eager loading is not feasible is when the model is using composite primary keys, and the backend database does not support tuples with IN, which currently includes SQL Server.
- Time, query and output when we add lazy = "selectin":
```
lazy=selectin
    total 2 queries:
    time 1: 0.8368 ms
    time 2: 5.4226 ms
    input:User.query.all()
    query 1:SELECT "user".id AS user_id, "user".username AS user_username, "user".email AS user_email, "user".image_file AS user_image_file, "user".password AS user_password FROM "user"
    query 2:SELECT post.user_id AS post_user_id, post.id AS post_id, post.title AS post_title, post.date_posted AS post_date_posted, post.content AS post_content FROM post WHERE post.user_id IN (%(primary_keys_1)s)
    output:
    [Post('First Posst', '2022-08-26 08:04:07.747359'), Post('noahcurtis@example.org', '1994-03-28 00:00:00'), Post('jamesjohnson@example.net', '2000-10-13 00:00:00'), Post('ikirby@example.com', '1998-02-14 00:00:00'), Post('hayesjennifer@example.com', '1991-09-06 00:00:00'), Post('wolfenathan@example.org', '2020-05-01 00:00:00'), Post('haley57@example.com', '2004-03-28 00:00:00'), Post('beverlycastillo@example.com', '2019-10-20 00:00:00'), Post('michael92@example.com', '1971-12-14 00:00:00'), Post('christie70@example.net', '2018-12-10 00:00:00'), Post('steve46@example.net', '1990-09-08 00:00:00')]
```

