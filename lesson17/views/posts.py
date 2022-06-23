import sqlite3
from flask import render_template, request, url_for, flash, redirect, Blueprint
from werkzeug.exceptions import abort


posts_bp = Blueprint('posts', __name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@posts_bp.route('/')
def home():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('home.html', posts=posts)


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@posts_bp.route('/post/<int:post_id>')
def show_post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@posts_bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        if not content:
            flash('Content is required!')

        if title and content:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template('create.html')


@posts_bp.route('/edit/<int:post_id>', methods=('GET', 'POST'))
def edit(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        if not content:
            flash('Content is required!')

        if title and content:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template('edit.html', post=post)


@posts_bp.route('/delete/<int:post_id>', methods=('POST',))
def delete(post_id):
    post = get_post(post_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    flash(f'"{post["title"]}" was successfully deleted!')
    return redirect(url_for('home'))