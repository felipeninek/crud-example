#imports
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


#database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


#select post from database
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjdghnvghçfgneajfnbjnrjnboetnbwókmnbwrng'


#page index
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


#page of the post
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


#page create post
@app.route('/create', methods=('GET', 'POST'))
def create():
    #check request from form
    if request.method == 'POST':
        #request items from form
        title = request.form['title']
        content = request.form['content']

        #check title
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required')
        else:
            #connection with database
            conn = get_db_connection()
            #execute query to insert values in database
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            #confirm
            conn.commit()
            #close connection
            conn.close()
            #redirect to page index
            return redirect(url_for('index'))

    return render_template('create.html')


#page edit post
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
