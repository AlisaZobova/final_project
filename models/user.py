from . import db


class User(db.Model):
    """Class to store users and information about them"""
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    name = db.Column(db.VARCHAR(50), nullable=False)
    email = db.Column(db.VARCHAR(50), nullable=False)
    password = db.Column(db.VARCHAR(50), nullable=False)

    def __str__(self):
        return f'User {self.user_id}: {self.name}'
