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
		
		# Filter out any current mentors
		if current_user.is_superintendant:
			all_mentors = User.query.filter_by (is_admin = True).all()
		else:
			# Only display mentors who are currently sharing at least one class
			filtered_mentors = []
			teacher_turmas = app.classes.models.get_teacher_classes_from_teacher_id (current_user.id)
			all_mentors = User.query.filter_by (is_admin = True).all()
			for mentor in all_mentors:
				for turma in teacher_turmas:
					if app.classes.models.check_if_turma_id_belongs_to_a_teacher (turma.id, mentor.id) is True:
						filtered_mentors.append (mentor)
			
			# Overwrite main variable
			all_mentors = filtered_mentors
			
		current_mentors = models.get_mentors_from_student_id (student_id)
		mentors = list(set(all_mentors) - set (current_mentors))
		
		return render_template('add_mentor.html', student = student, mentors = mentors)
	abort (403)
	
# Add a mentor
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
	
# Remove a mentor
@bp.route('/remove/<student_id>/<mentor_id>')
def remove_mentor (student_id, mentor_id):
	if current_user.is_authenticated and app.models.is_admin(current_user.username):
		student = User.query.get (student_id)
		mentor = User.query.get (mentor_id)
		if student is None or mentor is None:
			abort (403)
			
		mentor_relationship = MentoringRelationship.query.filter_by(student_id = student.id).filter_by(mentor_id = mentor.id).first()
		db.session.delete(mentor_relationship)
		db.session.commit()
		flash('Mentor removed successfully.', 'success')
		return redirect(url_for('mentors.view_mentors', student_id = student.id))
	abort (403)