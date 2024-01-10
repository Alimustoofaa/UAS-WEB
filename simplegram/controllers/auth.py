from flask import render_template, redirect, flash
from simplegram.forms import LoginForm, RegisterForm, ProfileForm, ResetPasswordForm
from simplegram.models.models import User
from config import db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from pathlib import Path
from simplegram.ai.face_validation import validation_face

def login():
    if current_user.is_authenticated:
        return redirect('/')

    loginForm = LoginForm()
    return render_template('login.html', form=loginForm)

def login_post():
    # from bootstrap import bcrypt
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user: 
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('/')
            else:
                flash({'error': 'Username & Password tidak sesuai'})
        else:
            flash({'error': 'Username & Password tidak sesuai'})
    
    return render_template('login.html', form=form)

def register():
    if current_user.is_authenticated:
        return redirect('/')
    
    form = RegisterForm()
    return render_template('register.html', form=form)

def register_post():
    # from bootstrap import bcrypt
    form = RegisterForm()
    if form.validate_on_submit():
        safe_pass = generate_password_hash(form.password.data)
        newUser = User(username=form.username.data, email=form.email.data, 
                       password=safe_pass, fullname=form.fullname.data)
        db.session.add(newUser)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html', form=form)

def reset_password():
    if current_user.is_authenticated:
        return redirect('/')

    resetPassword = ResetPasswordForm()
    return render_template('reset_password.html', form=resetPassword)

def reset_password_post():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            safe_pass = generate_password_hash(form.password.data)
            user.password = safe_pass
            db.session.commit()
            flash({'info': 'berhasil reset password'})
            return redirect('/login')
        else:
            flash({'error': 'Email Tidak Ditemukan'})    
    return render_template('reset_password.html', form=form)

@login_required
def my_profile():
    form = ProfileForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.fullname = form.fullname.data
        user.description = form.description.data

        # if profpic

        # if password

        db.session.commit()
    else:
        form.fullname.data = current_user.fullname
        form.profpic.data = current_user.profpic
        form.description.data = current_user.description

    return render_template('profil.html', form=form, )

@login_required
def my_profile_post():
    form = ProfileForm()

    user = User.query.get(current_user.id)
    user.fullname = form.fullname.data
    user.description = form.description.data

    if form.profpic.data:
        imFile = form.profpic.data
        fileName = secure_filename(imFile.filename)

        # save path
        path_saved = f'./static/profiles/{user.username}'
        Path(path_saved).mkdir(parents=True, exist_ok=True)
        imFile.save(f'{path_saved}/{fileName}')
        
        # validation face
        if not validation_face(f'{path_saved}/{fileName}'):
            flash({'error': 'validasi foto gagal, silahkan upload foto muka'})
            return render_template('profil.html', form=form, )
        else:
            user.profpic = fileName
            
    if form.password.data:
        safe_pass = generate_password_hash(form.password.data)
        user.password = safe_pass
    
    db.session.commit()

    flash({'info': 'berhasil simpan profile'})
    return render_template('profil.html', form=form, )

def logout():
    logout_user()
    return redirect('/login')