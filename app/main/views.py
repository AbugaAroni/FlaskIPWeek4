from flask import render_template,request,redirect,url_for, abort
from . import main
from flask_login import login_required, current_user
from ..models import User, Blogs, Comment
from .. import db
from .forms import BlogForm, Deleteform, Commentform, Deletecomment, UpdateBlog

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

@main.route('/viewblog/<int:blogid>', methods = ['GET','POST'])
@login_required
def comment(blogid):
    form = Commentform()

    #blog id needs a unique number
    blogid=blogid
    blogs = Blogs.get_singleblog(blogid)
    comments = Comment.get_comments(blogid)
    user = User.query.all()

    if form.validate_on_submit():
       description = form.description.data
       new_comment = Comment(comment_description=description, user=current_user, blog_id = blogid)
       new_comment.save_comment()

       return redirect(url_for('main.comment',blogid=blogid))


    title = 'View blog post'
    return render_template('viewblogpost.html',title = title, blogs = blogs, form=form, comments =comments, user =user)

@main.route('/manageblogpost/<int:blogid>', methods = ['GET','POST'])
@login_required
def manage(blogid):

    form1 = Deleteform()
    form2= UpdateBlog()

    #blog id needs a unique number
    blogid=blogid
    blogs = Blogs.get_singleblog(blogid)
    comments = Comment.get_comments(blogid)
    user = User.query.all()


    if form1.validate_on_submit() and form1.submit1.data:
        blogs.deleted = True
        db.session.add(blogs)
        db.session.commit()

        return redirect(url_for('main.profile', uname=current_user.username))

    if form2.validate_on_submit() and form2.submit3.data:
        blogs.blog_content = form2.content.data

        db.session.add(blogs)
        db.session.commit()

        return redirect(url_for('main.manage', blogid = blogs.id))

    title = 'View blog post'
    return render_template('manageblogposts.html',title = title, blogs = blogs,comments =comments, user =user, form1=form1, form2=form2)

#background process happening without any refreshing
@main.route('/comment/delete/<int:comid>')
def commdelete(comid):

    commentrow = Comment.query.filter_by(id = comid).first()
    blogid=commentrow.blog_id
    comments = Comment.get_singcomment(comid)
    comments.deleted = True
    db.session.add(comments)
    db.session.commit()

    return redirect(url_for('main.manage', blogid=blogid))
