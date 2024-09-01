from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sms.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Student %r>' % self.id


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['firstname']
        student = Student(first_name=first_name)
        try:
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding student'
    else:
        students = Student.query.order_by(Student.id).all()
        return render_template("index.html", students=students)


@app.route('/delete/<int:id>')
def delete(id):
    student_to_delete = Student.query.get_or_404(id)
    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an problem deleting the student"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.first_name = request.form['firstname']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating student"
    else:
        return render_template('/update.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)
