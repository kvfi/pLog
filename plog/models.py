from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from plog import db
from plog import login


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())


class TodoType(db.Model):
    __tablename__ = 'todo_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    project_id = db.Column(db.ForeignKey('projects.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    status = db.Column(db.Integer)
    created_by = db.Column(db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    type = db.Column(db.ForeignKey('todo_types.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    due_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())
    finished_at = db.Column(db.DateTime, server_default=func.now())

    user = db.relationship('User', primaryjoin='Todo.created_by == User.id', backref='todoes')
    project = db.relationship('Project', primaryjoin='Todo.project_id == Project.id', backref='todoes')
    todo_type = db.relationship('TodoType', primaryjoin='Todo.type == TodoType.id', backref='todoes')


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(50))
    password = db.Column(db.String(200))
    email = db.Column(db.String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
