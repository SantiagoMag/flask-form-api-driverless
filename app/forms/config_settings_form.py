

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length


class ResConfigSettingsForm(FlaskForm):

    api_vm_url = StringField(
        'API URL',
        validators=[Optional(), Length(max=255)]
    )
    submit = SubmitField('Guardar')