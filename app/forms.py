from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


# prediction request form
class PredictionRequestForm(FlaskForm):
    country_code = StringField('Country Code')
    city = StringField('City', validators=[DataRequired(),
                                           Length(min=0, max=80)])
    submit = SubmitField('Submit')