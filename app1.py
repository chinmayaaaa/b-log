from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as s3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = s3.connect('blog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id int PRIMARY KEY AUTOINCREMENT,
            genre TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home page - display all posts
@app.route('/')
def index():
    conn = s3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# View a single post
@app.route('/post/<int:post_id>')
def post(post_id):
    conn = s3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = post_id')
    post = c.fetchone()
    conn.close()
    return render_template('post.html', post=post)

# Create a new post
@app.route('/new', methods=['POST +'])
def new_post():
    if request.method == 'POST +':
        title = request.form['title']
        genre = request.form['genre']
        content = request.form['content']
        conn = s3.connect('blog.db')
        c = conn.cursor()
        c.execute('INSERT INTO posts (title, genre, content) VALUES (title, genre, content)')
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new_post.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
 
