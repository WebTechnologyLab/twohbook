from datetime import datetime
from hashlib import md5

from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, MessageForm
from app.models import User, Post, Message
from werkzeug.urls import url_parse


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('index.html',form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page, app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('dashboard', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('dashboard', page=posts.prev_num) if posts.has_prev else None
    return render_template('dashboard.html',user=current_user,posts=posts.items,\
            next_url=next_url, prev_url=prev_url)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html',user=user)

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.college = form.college.data
        current_user.year = form.year.data
        current_user.branch = form.branch.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.college.data = current_user.college
        form.branch.data = current_user.branch
        form.year.data = current_user.year
    return render_template('edit_profile.html',form=form)

@app.route('/post', methods=["GET","POST"])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(book_name=form.book_name.data, year=form.year.data, branch=form.branch.data,\
                    cost=form.cost.data, author=current_user)
        db.session.add(p)
        db.session.commit()
        flash('Your post is successfully submitted!')
        return redirect(url_for('post'))
    return render_template('post.html',form=form)

@app.route('/send_message/<recipient>', methods=['GET','POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent')
        return redirect(url_for('dashboard'))
    return render_template('send_message.html', form=form, recipient=recipient)

@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.message_received.order_by(
            Message.timestamp.desc()).paginate(
                page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages', page=messages.next_num) \
            if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
            if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                        next_url=next_url, prev_url=prev_url)


@app.route('/starred')
@login_required
def starred():
    posts = current_user.starred
    return render_template('starred.html', posts=posts)

@app.route('/star/<int:postid>')
@login_required
def star(postid):
    post = Post.query.filter_by(id=postid).first()
    if post is None:
        flash('Post not found')
        return redirect(url_for('dashboard'))
    if post.author == current_user:
        flash('You cannot star your own posts')
        return redirect(url_for('dashboard'))
    current_user.star(post)
    db.session.commit()
    flash('You have starred the post!')
    return redirect(url_for('dashboard'))

@app.route('/unstar/<int:postid>')
@login_required
def unstar(postid):
    post = Post.query.filter_by(id=postid).first()
    if post is None:
        flash('Post not found')
        return redirect(url_for('dashboard'))
    if post.author == current_user:
        flash('You cannot unstar own posts!')
        return redirect(url_for('dashboard'))
    current_user.unstar(post)
    db.session.commit()
    flash('You have successfully unstarred the posts')
    return redirect(url_for('dashboard'))

@app.route('/signup',methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, name=form.name.data, college=form.college.data, \
                branch=form.branch.data, year=form.year.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations!You have successfully registered.')
        return redirect(url_for('index'))
    return render_template('signup.html',form=form)

@app.route('/my_listings')
@login_required
def my_listings():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user_id=current_user.id).paginate(page,\
            app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('my_listings', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('my_listings', page=posts.prev_num) if posts.has_prev else None
    return render_template('my_listings.html',posts=posts.items, prev_url=prev_url, next_url=next_url)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
