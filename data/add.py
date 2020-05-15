from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    image = StringField('Картинка:', validators=[DataRequired()])
    submit = SubmitField('Добавить')
