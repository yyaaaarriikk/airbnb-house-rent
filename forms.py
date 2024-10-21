from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, TextAreaField, FloatField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange, Optional 
from models import User
from datetime import date
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Це ім’я користувача зайнято. Виберіть інший.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class AddHouseForm(FlaskForm):
    name=StringField('House Name', validators=[DataRequired(), Length(min=2, max=20)])
    description=StringField('Description', validators=[DataRequired(), Length(min=2)])
    residents = IntegerField('Residents', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    address=StringField('Address', validators=[DataRequired()])
    price = FloatField('Price', validators=[Optional(), NumberRange(min=0)], default=0)
    image = FileField('House Image', validators=[Optional(), FileAllowed(['jpg','png', 'jpeg'], 'IMagesOnly')])


class BookingForm(FlaskForm):
    booking_name = StringField('Booking Name', validators=[DataRequired(), Length(min=2, max=20)])
    arrival_date = DateField('Arrival Time', validators=[DataRequired()], format='%Y-%m-%d')
    departure_date = DateField('Departure Time', validators=[DataRequired()], format='%Y-%m-%d')
    arrival_residents = IntegerField('Arrival Residents', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Book')


    def validate_departure_date(self, departure_date):
            if departure_date.data <= self.arrival_date.data:
                raise ValidationError('Дата від’їзду повинна бути пізніше дати приїзду.')

    def validate_arrival_date(self, arrival_date):
        if arrival_date.data < date.today():
            raise ValidationError('Дата приїзду не може бути в минулому.')
