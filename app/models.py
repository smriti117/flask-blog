from app import db , login_manager
from datetime import datetime 
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))



class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __str__(self):
		return self.id


class Post(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	title       = db.Column(db.String(30), nullable=False)
	# slug        = db.Column(db.String(30), nullable=False)
	content     = db.Column(db.Text, nullable=False)
	dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	dateUpdated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	# image       = db.Column(db.String(20), nullable=False, default='default.jpg')

	def __str__(self):
		return self.id

