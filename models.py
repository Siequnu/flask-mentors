from flask import current_app
from flask_login import current_user
from datetime import datetime
from app import db
from app.models import User
import app.models

class MentoringRelationship(db.Model):
	__table_args__ = {'sqlite_autoincrement': True}
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Mentoring relationship {}>'.format(self.id)
	
def get_mentors_from_student_id (student_id):
	mentor_relationships = MentoringRelationship.query.filter_by(student_id = student_id).all()
	mentors = []
	for teaching_connection in mentor_relationships:
		mentors.append (User.query.get(teaching_connection.mentor_id))
	return mentors
