from app import db


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    notas = db.Column(db.Text)
    edad = db.Column(db.Integer, nullable=False)
    ingreso_anual = db.Column(db.Float, nullable=False)
    propiedad_vivienda = db.Column(db.String(20), nullable=False)
    anos_empleo = db.Column(db.Integer, nullable=False)
    proposito_prestamo = db.Column(db.String(20), nullable=False)
    calificacion_prestamo = db.Column(db.String(1), nullable=False)
    monto_prestamo = db.Column(db.Float, nullable=False)
    tasa_interes = db.Column(db.Float, nullable=False)
    deuda_ingreso = db.Column(db.Float, nullable=False)
    incumplimiento_anterior = db.Column(db.String(1), nullable=False)
    historial_crediticio = db.Column(db.Integer, nullable=False)
    estado_deuda = db.Column(db.String(1))
    prediccion_incumplimiento = db.Column(db.String(1))
    probabilidad_incumplimiento = db.Column(db.Float)
    h20_predicciones = db.Column(db.Text)
    h20_prediccion_clase = db.Column(db.String(1))