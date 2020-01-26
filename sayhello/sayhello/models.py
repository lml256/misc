from datetime import datetime
from sayhello import db


# 数据库建模
class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(200))
	name = db.Column(db.String(20))
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
