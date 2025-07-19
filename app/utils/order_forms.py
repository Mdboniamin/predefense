from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class OrderForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Add to Cart")

