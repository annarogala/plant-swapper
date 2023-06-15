from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user

from app import app, db, bcrypt
from .models import Plant, User
from .login_form import LoginForm, RegisterForm


@app.route('/')
@app.route('/index')
def index():
    plants = Plant.query.order_by(Plant.date_created).all()
    return render_template('plants-listing.html', plants=plants)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/new-plant', methods=['GET', 'POST'])
@login_required
def new_plant():
    if request.method == 'POST':
        plant_content =  request.form['content']
        new_plant = Plant(content=plant_content)

        try:
            db.session.add(new_plant)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error happened while adding a plant'
    else:
        plants = Plant.query.order_by(Plant.date_created).all()
        return render_template('plant-form.html', plants=plants)


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
        plant_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error happened while updating plant content'
    else:
        return render_template('update.html', plant=plant_to_update)