from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class PlantForm(FlaskForm):
    name = StringField(validators=[
                           InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "name"})
    description = StringField(validators=[
                             InputRequired(), Length(min=8, max=400)], render_kw={"placeholder": "description"})
    city = StringField(validators=[
                             InputRequired(), Length(min=2, max=30)], render_kw={"placeholder": "city"})
    image = StringField(validators=[
                             InputRequired(), Length(min=8, max=300)], render_kw={"placeholder": "image url"})
    
    submit = SubmitField('Add plant')
    