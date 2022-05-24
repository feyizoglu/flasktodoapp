from matplotlib.pyplot import title
from sympy import re
from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Python Çalışmalar/2. Seviye/TodoApp/todo.db'
db = SQLAlchemy(app)
@app.route("/")
def index():
    todos = Todo.query.all() #Listedeki veriler sözlük yapısı olarak döncek. sonra biz bunun üzerinde for döngüsü yazabiliriz
    return render_template("index.html",todos=todos)

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first() #bunları falan hep internetten bakıyoruz
    """if todo.complete = True:
        todo.complete=False
    else:
        todo.complete =True"""
    todo.complete = not todo.complete #yukarıdakinin kısayol olarak yapılması bu şekilde oluyor.
    
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/add",methods = ["POST"]) #sadece post requeste izin veriyoruz
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title=title,complete = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))
    
@app.route("/delete/<string:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)  #tamamlanıp tamamlanmadığını burdan kontrol ediyoruz
    
if __name__ == "__main__":
    db.create_all() #Classtaki tüm özellikleri tablo olarak ekliyoruz.
    app.run(debug=True)
    
    