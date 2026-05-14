import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    nom     = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date    = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    messages = Message.query.order_by(Message.date.desc()).all()
    return render_template('index.html', messages=messages)

@app.route('/add', methods=['POST'])
def add():
    nom     = request.form.get('nom', '').strip()
    message = request.form.get('message', '').strip()
    if nom and message:
        nouveau = Message(nom=nom, message=message)
        db.session.add(nouveau)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
