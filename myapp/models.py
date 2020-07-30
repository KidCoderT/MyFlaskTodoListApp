from myapp import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    profile_image = db.Column(db.String(1000), default="https://image.shutterstock.com/image-vector/user-icon-trendy-flat-style-260nw-418179856.jpg")
    password = db.Column(db.String())
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.name

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return self.text