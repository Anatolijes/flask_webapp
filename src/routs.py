from src import app, bcrypt
from flask import render_template, request, url_for, redirect, session, flash
from src import db
from src.forms import LoginForm, PostFrom
from src.models import User, Post
from flask_login import login_user, logout_user, current_user

app.secret_key = 'salt'


@app.before_first_request
def create_table():
    db.create_all()
    post1 = Post(title="1", content="2")
    post2 = Post(title="3", content="4")
    post3 = Post(title="5", content="6")
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    user = User(username='Admin', password_hash='$2b$12$nS1jV3whFFDRmAQ3uWNjduAgXo4kLpoVhoOki1Z1n1a2ODXlshkZ6')
    db.session.add(user)
    db.session.commit()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login() -> 'html':
    if current_user.is_authenticated:
        redirect(url_for("/"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            logout_user(user, remember=form.remember_me.data)
            app.debug("user with name " + {form.username.data} + "was logged in")
            flash("You have Logged in")
            return redirect('/')
    else:
        flash("Login was Unsuccessful")
    return render_template('login.html', the_title='login', form=form)


@app.route('/logout')
def logout():

    return render_template('login.html', the_title='logout')


@app.route('/posts', methods=['GET'])
def retrieve_posts():
    posts = Post.query.all()
    return render_template('posts.html', the_title='posts', posts=posts)


@app.route('/post-delete')
def delete_post():
    return render_template('posts.html', the_title='delete')


@app.route('/post-update', methods=['POST'])
def update_post():
    form = PostFrom()
    if form.validate_on_submit():
        flash("Post added successfully")
        redirect(url_for('index'))
    return render_template('posts.html', the_title='Update', form=form)


@app.route('/post-create', methods=['POST', 'GET'])
def create_post():
    return render_template('add_post.html', the_title='try again')


def check_logged_in() -> bool:
    if session['logged_in']:
        return True
    else:
        return False
