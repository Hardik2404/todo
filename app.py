from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template("index.html" , allTodo=allTodo)
    

@app.route("/info")
def info():
    return "hello"

@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    try:
        # Fetch the todo item by sno
        todo = Todo.query.filter_by(sno=sno).first()
        if not todo:
            return "Todo not found", 404  # Return a 404 error if the todo does not exist

        # Delete the todo item
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        # Log the error for debugging
        print(f"Error deleting todo: {e}")
        return "An error occurred while deleting the todo.", 500

@app.route("/product")
def product():
    return render_template("pro.html")

@app.route("/show")
def show():
    allTodo=Todo.query.all()
    print(allTodo)
    return "hello"

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True ,port=2404)

