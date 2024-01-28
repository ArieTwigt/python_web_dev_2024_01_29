from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError



# custom validators
def validate_country_code(self, field):
    if field.data.isdigit():
        raise ValidationError('Country code must not be numeric.')

def validate_city(self, field):
    if field.data.isdigit():
        raise ValidationError('City name must not be numeric.')

def NonNumeric():
    message = 'Field must not be numeric.'

    def _non_numeric(form, field):
        if field.data.isdigit():
            raise ValidationError(message)

    return _non_numeric


# prediction request form
class PredictionRequestForm(FlaskForm):
    country_code = StringField('Country Code')
    city = StringField('City', validators=[DataRequired(message="Insert a city name"),
                                           Length(min=0, max=80),
                                           NonNumeric()])
    submit = SubmitField('Submit')

    