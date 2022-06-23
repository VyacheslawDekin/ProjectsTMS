import sqlite3
from flask import render_template, request, url_for, flash, redirect, Blueprint
from werkzeug.exceptions import abort
from models import Posts
from app import db


posts = Blueprint('posts', __name__)


@posts.route('/')
def home():
    posts = Posts.query.all()
    return render_template('home.html', posts=posts)


@posts.route('/post/<int:post_id>')
def show_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)
    return render_template('post.html', post=post)


@posts.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        if not content:
            flash('Content is required!')

        if title and content:
            post = Posts(title=title, content=content)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('create.html')


@posts.route('/edit/<int:post_id>', methods=('GET', 'POST'))
def edit(post_id):
    post = Posts.query.filter_by(id=post_id).first()

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']

        if not post.title:
            flash('Title is required!')
        if not post.content:
            flash('Content is required!')

        if post.title and post.content:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('show_post', post_id=post_id))

    return render_template('edit.html', post=post)


@posts.route('/delete/<int:post_id>', methods=('POST',))
def delete(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash(f'"{post.title}" was successfully deleted!')
    return redirect(url_for('home'))