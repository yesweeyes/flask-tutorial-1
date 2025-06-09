from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_todo = Todo(content=content)
            db.session.add(new_todo)
            db.session.commit()
    else:
        return render_template("index.html", tasks=Todo.query.all())
    
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id: int):
    todo_to_delete = Todo.query.get_or_404(id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return '', 204

@app.route('/update/<int:id>', methods=['POST'])
def update(id: int):
    todo_to_update = Todo.query.get_or_404(id)
    content = request.form.get('content')
    if content:
        todo_to_update.content = content
        db.session.commit()
    return '', 204


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='localhost')