from flask import Flask, render_template, request, redirect, session, flash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# User class to store user details
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Post class to store post details
class Post:
    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content
        self.comments = []

    def add_comment(self, comment):
        """Add a comment to the post."""
        self.comments.append(comment)

# Comment class to store comment details
class Comment:
    def __init__(self, author, content):
        self.author = author
        self.content = content

# In-memory storage for users and posts
users = {}
posts = {}

@app.route('/')
def index():
    """Render the homepage and show all posts."""
    return render_template('home.html', posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('User already exists.')
        else:
            users[username] = User(username, password)
            flash('Signup successful! Please log in.')
            return redirect('/')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user.password == password:
            session['username'] = username
            return redirect('/')
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Log out the current user."""
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    """Allow logged-in users to create a post."""
    if 'username' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post_id = len(posts) + 1
        new_post = Post(session['username'], title, content)
        posts[post_id] = new_post
        return redirect('/')
    
    return render_template('create_post.html')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    """View a post and add comments."""
    post = posts.get(post_id)
    if not post:
        return "Post not found", 404
    
    if request.method == 'POST':
        comment_content = request.form['comment']
        author = session.get('username', 'Anonymous')
        new_comment = Comment(author, comment_content)
        post.add_comment(new_comment)
    
    return render_template('post.html', post=post)

@app.route('/reset', methods=['POST'])
def reset():
    """Reset all users and posts (for testing/demo purposes)."""
    global users, posts
    users = {}
    posts = {}
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
