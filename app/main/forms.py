from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required

class BlogForm(FlaskForm):

    title = StringField('Blog title',validators=[Required()])
    category = SelectField('Blog category', choices=[('Poem', 'Poem'), ('Short-story', 'Short-story'),('Opinion-piece', 'Opinion-piece'), ('Vent', 'Vent')], validators=[Required()])
    content = TextAreaField('Blog content', validators=[Required()])
    submit = SubmitField('Submit')

class Commentform(FlaskForm):
    description = TextAreaField('Comment description', validators=[Required()])
    submit = SubmitField('Submit')

class Deleteform(FlaskForm):
    submit1 = SubmitField('Delete')
