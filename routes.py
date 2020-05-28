from flask import render_template, flash, redirect, url_for, request, abort, current_app, session, Response
from flask_login import current_user, login_required

from . import bp, models
from .models import MentoringRelationship

from app import db
from app.models import User
import app.models

# View a student's mentors
@bp.route('/student/<student_id>')
def view_mentors (student_id):
	if current_user.is_authenticated and app.models.is_admin(current_user.username):
		student = User.query.get(student_id)
		mentors = models.get_mentors_from_student_id (student_id)
		return render_template('view_mentors.html', student = student, mentors = mentors)
	abort (403)

# View a student's mentors
@bp.route('/search/<student_id>')
def search_for_mentors (student_id):
	if current_user.is_authenticated and app.models.is_admin(current_user.username):
		student = User.query.get (student_id)
		if student is None:
			abort (403)
		mentors = User.query.filter_by (is_admin = True).all()
		return render_template('add_mentor.html', student = student, mentors = mentors)
	abort (403)
	
# View a student's mentors
@bp.route('/add/<student_id>/<mentor_id>')
def add_mentor (student_id, mentor_id):
	if current_user.is_authenticated and app.models.is_admin(current_user.username):
		student = User.query.get (student_id)
		mentor = User.query.get (mentor_id)
		if student is None or mentor is None:
			abort (403)
			
		mentor_relationship = MentoringRelationship (student_id = student.id, mentor_id = mentor.id)
		db.session.add(mentor_relationship)
		db.session.commit()
		flash('Mentor added successfully.', 'success')
		return redirect(url_for('mentors.view_mentors', student_id = student.id))
	abort (403)