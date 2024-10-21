
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length


class LoanForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    notas = TextAreaField('Notas')
    edad = IntegerField('Edad', validators=[DataRequired(), NumberRange(min=0)])
    ingreso_anual = FloatField('Ingreso Anual', validators=[DataRequired()])
    propiedad_vivienda = SelectField('Propiedad Vivienda', choices=[
        ('RENT', 'Rent'),
        ('OWN', 'Own'),
        ('MORTGAGE', 'Mortgage'),
        ('OTHER', 'Other')
    ], validators=[DataRequired()])
    anos_empleo = IntegerField('Años Empleo', validators=[DataRequired(), NumberRange(min=0)])
    proposito_prestamo = SelectField('Propósito Préstamo', choices=[
        ('PERSONAL', 'Personal'),
        ('EDUCATION', 'Education'),
        ('MEDICAL', 'Medical'),
        ('VENTURE', 'Venture'),
        ('HOMEIMPROVEMENT', 'Home Improvement'),
        ('DEBTCONSOLIDATION', 'Debt Consolidation')
    ], validators=[DataRequired()])
    calificacion_prestamo = SelectField('Calificación Préstamo', choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), 
        ('E', 'E'), ('F', 'F'), ('G', 'G')
    ], validators=[DataRequired()])
    monto_prestamo = FloatField('Monto Préstamo', validators=[DataRequired()])
    tasa_interes = FloatField('Tasa de Interés', validators=[DataRequired()])
    deuda_ingreso = FloatField('Deuda/Ingreso', validators=[DataRequired()])
    incumplimiento_anterior = SelectField('Incumplimiento Anterior', choices=[
        ('Y', 'Yes'), ('N', 'No')
    ], validators=[DataRequired()])
    historial_crediticio = IntegerField('Historial Crediticio (años)', validators=[DataRequired(), NumberRange(min=0)])
    estado_deuda = SelectField('Estado de Deuda', choices=[
        ('', 'Seleccione una opción'),  # Opción vacía
        ('0', 'Cumplimiento'),
        ('1', 'Incumplimiento')
    ], validators=[Optional()])
    prediccion_incumplimiento = SelectField('Predicción Incumplimiento', choices=[
        ('', 'Seleccione una opción'),  # Opción vacía
        ('0', 'Cumplimiento'),
        ('1', 'Incumplimiento')
    ], validators=[Optional()])
    probabilidad_incumplimiento = FloatField('Probabilidad de Incumplimiento')
    h20_predicciones = TextAreaField('Predicción H2O')
    h20_prediccion_clase = SelectField('Predicción de Clase', choices=[
        ('', 'Seleccione una opción'),  # Opción vacía
        ('0', 'Cumplimiento'),
        ('1', 'Incumplimiento')
    ], validators=[Optional()])

    submit = SubmitField('Enviar')
