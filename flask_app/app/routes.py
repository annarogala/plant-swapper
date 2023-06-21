from flask import flash, render_template, request, redirect, session, url_for
from flask_login import current_user, login_user, login_required, logout_user

from app import app, db, bcrypt
from .models import Plant, User
from .login_form import LoginForm, RegisterForm
from .plant_form import PlantForm
from .reset_password_form import ResetPasswordRequestedForm, ResetPasswordForm
from .email import send_password_reset_email


@app.route('/')
@app.route('/index')
def index():
    plants = Plant.query.order_by(Plant.date_created).all()
    return render_template('plants-listing.html', plants=plants)


@app.route('/my-plants')
def my_plants():
    plants = Plant.query.order_by(Plant.date_created).all()
    return render_template('my-plants-listing.html', plants=plants)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect('/')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created, please log in')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))


@app.route('/new-plant', methods=['GET', 'POST'])
@login_required
def new_plant():
    form = PlantForm()

    user_id = session['user_id']

    if form.validate_on_submit():
        new_plant = Plant(name=form.name.data, description=form.description.data, city=form.city.data, image=form.image.data, user_id=user_id)
        db.session.add(new_plant)
        db.session.commit()
        flash('Plant added')
        return redirect(url_for('my_plants'))

    plants = Plant.query.order_by(Plant.date_created).all()
    return render_template('add-plant-form.html', plants=plants, form=form)


@app.route('/delete/<int:id>')
def delete(id):
    plant_to_delete = Plant.query.get_or_404(id)

    try:
        db.session.delete(plant_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error happened while deleting the plant'
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    plant_to_update = Plant.query.get_or_404(id)

    if request.method == 'POST':
        plant_to_update.description = request.form['description']

        try:
            db.session.commit()
            return redirect(url_for('my_plants'))
        except:
            return 'Error happened while updating plant content'
    else:
        return render_template('update.html', plant=plant_to_update)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        flash('You are already logged in')
        return redirect(('/'))
    
    form = ResetPasswordRequestedForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
        
        return redirect(url_for('login'))
    
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.verify_reset_password_token(token)
    
    if not user:
        return redirect(url_for('index'))
    
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been changed.')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', form=form)

