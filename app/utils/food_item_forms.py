from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed

class FoodItemForm(FlaskForm):
    name = StringField("Food Item Name", validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField("Description", validators=[Length(max=500)])
    price = DecimalField("Price", validators=[DataRequired(), NumberRange(min=0.01)])
    image = FileField("Food Image (Optional)", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Save Food Item")

