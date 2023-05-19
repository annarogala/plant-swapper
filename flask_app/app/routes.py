from flask import render_template, request, redirect
from .models import Plant
from app import app, db

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    if request.method == 'POST':
        plant_content =  request.form['content']
        new_plant = Plant(content=plant_content)

        try:
            db.session.add(new_plant)
            db.session.commit()
            return redirect ('/')
        except:
            return 'Error happened while adding a plant'
    else:
        plants = Plant.query.order_by(Plant.date_created).all()
        return render_template('index.html', plants=plants)

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