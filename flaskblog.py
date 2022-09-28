from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ireallyhopenobdyhacksme'

# password = 'test'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/matthewhartz/python_practice/projects/flask_blog/blog_data.db'
#db = SQLALchemy(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post



@app.route("/")
@app.route("/home")
def home():
    conn = get_db_connection()
    posts = conn.execute('Select * from posts').fetchall()
    conn.close()
    return render_template('home.html', posts=posts, title='My Blog')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        password = request.form['password']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
            return render_template('createblog.html')
        elif password == 'test':
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                        (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

        else:
            flash('Wrong Password!')
            return render_template('createblog.html')

    return render_template('createblog.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        password = request.form['password']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        elif password == 'test':
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

        else:
            flash('Wrong Password!')

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash(f"{post['title']} was successfully deleted!")
    return redirect(url_for('home'))


@app.route('/quotes')
def quotes():
    return render_template('quotes.html')