from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_login import current_user
from app.models.user import User

class UpdateProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone Number", validators=[DataRequired(), Length(min=10, max=20)])
    location = StringField("Location", validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField("Update Profile")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose a different one.")

    def validate_phone_number(self, phone_number):
        if phone_number.data != current_user.phone_number:
            user = User.query.filter_by(phone_number=phone_number.data).first()
            if user:
                raise ValidationError("That phone number is taken. Please choose a different one.")

