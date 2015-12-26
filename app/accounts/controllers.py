from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for 
from forms import LoginForm

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')

def current_user():
	if 'id' in session:
		uid = session['id']
		return User.query.get(uid)
	return None

@accounts.route('/login')
def login():
	form = LoginForm(request.form)
	if request.method =='POST':
		username = request.form.get('username')
		user = User.query.filter_by(username=username).first()
		if not user:
			user = User(username=username)
	return render_template('accounts/login.html', form=form,) 
