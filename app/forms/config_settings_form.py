

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length


class ResConfigSettingsForm(FlaskForm):
    h2o_driverless_address = StringField(
        'URL',
        validators=[Optional(), Length(max=255)]
    )
    h2o_driverless_username = StringField(
        'Username',
        validators=[Optional(), Length(max=255)]
    )
    h2o_driverless_password = StringField(
        'Password',
        validators=[Optional(), Length(max=255)]
    )
    h2o_driverless_name_experiment = StringField(
        'Nombre Experimento',
        validators=[Optional(), Length(max=255)]
    )
    api_vm_url = StringField(
        'API URL',
        validators=[Optional(), Length(max=255)]
    )
    submit = SubmitField('Guardar')