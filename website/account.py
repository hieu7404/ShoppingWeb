from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from website import db
from werkzeug.security import generate_password_hash, check_password_hash



account_bp = Blueprint('account', __name__)

@account_bp.route('/account', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'login':
            # Handle login
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                else:
                    flash('Incorrect password, try again', category='error')
            else:
                flash('Email does not exist.', category='error')

            print("Login data: ", request.form)
        elif action == 'register':
            # Handle register
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()

            if user:
                flash('Email already exists.', category='error')
            elif len(username) < 2:
                flash('Username is too short.', category='error')
                pass
            elif len(email) < 4:
                flash('Email is invalid.', category='error')
                pass
            elif len(password) < 6:
                flash('Password must be at least 6 characters.', category='error')
                pass
            else: 
                new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()

                flash('Account created!', category='success')
                return redirect(url_for('views.home'))

            print("Register data: ", request.form)
    return render_template("account.html")