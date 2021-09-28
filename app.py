from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    pk =db.Column(db.Integer,primary_key = True)
    title =db.Column(db.String(100),nullable=False)
    description =db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.pk} - {self.title}"

@app.route('/',methods=['GET','POST'])
def Home():

    if request.method=='POST':
        title = request.form['title']
        desc = request.form['description']
        todo = Todo(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()
        
    all_todolist = Todo.query.all() 
    return render_template("HomeTodo.html",allTodo=all_todolist)

@app.route('/update/<int:pk>', methods=['GET', 'POST'])
def update(pk):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['description']
        todo = Todo.query.filter_by(pk=pk).first()
        todo.title = title
        todo.description = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(pk=pk).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:pk>')
def delete(pk):
    todo = Todo.query.filter_by(pk=pk).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)