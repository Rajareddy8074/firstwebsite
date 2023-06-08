from flask import Flask, render_template, url_for, request, redirect,session 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) 
class Todo(db.Model): 
 id = db.Column(db.Integer, primary_key=True) 
 content = db.Column(db.String(200), nullable=False) 
 date_created = db.Column(db.DateTime, default=datetime.utcnow) 
 def __repr__(self): 
 return '<Task %r>' % self.id 
app.secret_key = 'mysecretkey'
@app.route('/') 
def index(): 
 return render_template('login.html') 
@app.route('/user/<username>') 
def show_user_profile(username): 
 return f'User {username}'
@app.route('/category/<category_name>/<int:page>') 
def show_category(category_name, page): 
 return f'Category {category_name}, page {page}'
@app.route('/logout') 
def logout(): 
 # Remove the username from the session if it's there
 session.pop('username', None) 
 return redirect(url_for('login')) 
@app.route('/login', methods=['POST', 'GET']) 
def login(): 
 if request.method == 'POST': 
 # Get the username from the form data
 username = request.form['username'] 
 mail=request.form['mail'] 
 # Store the username in the session
 session['username'] = username 
 session['mail'] = mail 
 return redirect(url_for('home')) 
 return render_template('login.html') 
@app.route('/sessions',methods=['POST', 'GET']) 
def home(): 
 # Check if user is logged in. If not, redirect to the login page.
 if 'username' in session: 
 username = session['username'] 
 mail = session['mail'] 
 if request.method == 'POST': 
 task_content = request.form['content'] 
 new_task = Todo(content=task_content) 
 try: 
 db.session.add(new_task) 
 db.session.commit() 
 return redirect('/sessions') 
 except: 
 return 'There was an issue adding your task'
 else: 
 tasks = Todo.query.order_by(Todo.date_created).all() 
return render_template('index.html', tasks=tasks,username=username, mail=mail) 
 
@app.route('/delete/<int:id>') 
def delete(id): 
 task_to_delete = Todo.query.get_or_404(id) 
 try: 
 db.session.delete(task_to_delete) 
 db.session.commit() 
 return redirect('/sessions') 
 except: 
 return 'There was a problem deleting that task'
@app.route('/update/<int:id>', methods=['GET', 'POST']) 
def update(id): 
 task = Todo.query.get_or_404(id) 
 if request.method == 'POST': 
 task.content = request.form['content'] 
 try: 
 db.session.commit() 
 return redirect('/sessions') 
 except: 
 return 'There was an issue updating your task'
 else: 
 return render_template('update.html', task=task) 
if __name__ == "__main__": 
 app.run(debug=True) 
