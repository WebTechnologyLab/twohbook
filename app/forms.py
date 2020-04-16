from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SelectField, SubmitField, IntegerField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo, Length
from app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=4,max=12)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8, max=15,message="Password must be between 8 and 15 characters")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=4,max=12)])
    name = StringField('Name', validators=[InputRequired()])
    college = SelectField('College',choices=[('pict','Pune Institute of Computer Technology,Pune')],validators=[InputRequired()])
    branch = SelectField('Branch',choices=[('cse','CSE'),('entc','ENTC'),('it','IT')],validators=[InputRequired()])
    year = SelectField('Year',choices=[('fe','FE'),('se','SE'),('te','TE'),('be','BE')],validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators=[InputRequired(),\
            Length(min=8, max=15,message="Password must be between 8 and 15 characters")])
    repassword = PasswordField('Re-enter Password',validators=[InputRequired(), \
        EqualTo('password',message="Password doesn't match"),Length(min=8, max=15,message="Password must be between 8 and 15 characters")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Please use differet email address')

class EditProfileForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired()])
    college = SelectField('College',choices=[('pict','Pune Institute of Computer Technology,Pune')],validators=[InputRequired()])
    branch = SelectField('Branch',choices=[('cse','CSE'),('entc','ENTC'),('it','IT')],validators=[InputRequired()])
    year = SelectField('Year',choices=[('fe','FE'),('se','SE'),('te','TE'),('be','BE')],validators=[InputRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username,*args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None :
                raise ValidationError('Please use a different username')

class PostForm(FlaskForm):
    book_name = StringField('Book Name',validators=[InputRequired()])
    year = SelectField('Year',choices=[('fe','FE'),('se','SE'),('te','TE'),('be','BE')],validators=[InputRequired()])
    branch = SelectField('Branch',choices=[('cse','CSE'),('entc','ENTC'),('it','IT')],validators=[InputRequired()])
    cost = IntegerField('Cost',validators=[InputRequired()])
    submit = SubmitField('Post')
