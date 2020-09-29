from flask import render_template,request,redirect,url_for, abort
from . import main
from flask_login import login_required
from ..models import User, Blogs
from .. import db
from .forms import BlogForm

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    blogposts = Blogs.get_blogs()
    return render_template('index.html', blogposts =blogposts)

@main.route('/latestblogs')
def latestblogs():

    '''
    View latest page function that returns 5 newest blog posts and its data
    '''
    blogposts = Blogs.get_newblogs()
    return render_template('latestblogs.html', blogposts =blogposts)


#view and acess user profile
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    userid = user.id
    blogs = Blogs.get_userblog(userid)

    if user is None:
        abort(404)

    return render_template("profile/profile.html",user = user, blogs=blogs)

#submit a pitch view, need to change the unique id
@main.route('/newpost/<int:userid>', methods = ['GET','POST'])
@login_required
def new_pitch(userid):
    form = BlogForm()

    useri=userid
    current_user = User.query.filter_by(id = userid).first()

    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        content = form.content.data
        new_blog = Blogs(blog_title=title,blog_category=category,blog_content=content, user_id=useri)
        new_blog.save_blog()


        return redirect(url_for('main.profile',uname=current_user.username))

    title = 'New Blog Post'
    return render_template('submitblogs.html',title = title, blog_form=form)
