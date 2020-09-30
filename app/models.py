from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from sqlalchemy import desc


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    usertype = db.Column(db.String(255),index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    pass_secure = db.Column(db.String(255))

    blogs = db.relationship('Blogs',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Blogs(db.Model):

    __tablename__='blogs'

    id = db.Column(db.Integer,primary_key = True)
    blog_title = db.Column(db.String)
    blog_category = db.Column(db.String)
    blog_content = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    deleted = db.Column(db.Boolean, default=False)

    comments = db.relationship('Comment', backref = 'blogs',lazy = "dynamic")

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    #get all blogs
    @classmethod
    def get_blogs(cls):
        blog = Blogs.query.filter_by(deleted=False).all()
        return blog

    #get blogs according to persons id
    @classmethod
    def get_userblog(cls,id):
        blog = Blogs.query.filter_by(user_id=id).filter_by(deleted=False).all()
        return blog

    #get the new blogs
    @classmethod
    def get_newblogs(cls):

        blog = Blogs.query.order_by(desc(Blogs.id)).filter_by(deleted=False).limit(5)
#        blog = Blogs.select().order_by(Blogs.c.id.desc())

        return blog

    #get blog according to id
    @classmethod
    def get_singleblog(cls,id):
        blogs = Blogs.query.filter_by(id=id).first()
        return blogs

class Comment(db.Model):

    __tablename__='comments'

    id = db.Column(db.Integer,primary_key = True)
    comment_description = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))
    deleted = db.Column(db.Boolean, default=False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    #get comments according to  pitchid
    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id=id).filter_by(deleted=False).all()
        return comments

    #get blog according to id
    @classmethod
    def get_singcomment(cls,id):
        com = Comment.query.filter_by(id=id).first()
        return com
