import requests
from flask import request, jsonify
from flask import Blueprint, render_template
from app.models.loan import Loan
from app.forms.loan_form import LoanForm
from app import db
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from app.models.config_settings import ResConfigSettings

loan_bp = Blueprint('loan', __name__)

@loan_bp.route('/')
def index():
    registros = Loan.query.all()
    return render_template('loan/listar_registros.html', registros=registros)

@loan_bp.route("/submit", methods=["GET", "POST"])
def submit():
    form = LoanForm()
    if form.validate_on_submit():
        nuevo_prestamo = Loan(
            nombre=form.nombre.data,
            notas=form.notas.data,
            edad=form.edad.data,
            ingreso_anual=form.ingreso_anual.data,
            propiedad_vivienda=form.propiedad_vivienda.data,
            anos_empleo=form.anos_empleo.data,
            proposito_prestamo=form.proposito_prestamo.data,
            calificacion_prestamo=form.calificacion_prestamo.data,
            monto_prestamo=form.monto_prestamo.data,
            tasa_interes=form.tasa_interes.data,
            deuda_ingreso=form.deuda_ingreso.data,
            incumplimiento_anterior=form.incumplimiento_anterior.data,
            historial_crediticio=form.historial_crediticio.data,
            estado_deuda=form.estado_deuda.data,
            prediccion_incumplimiento=form.prediccion_incumplimiento.data,
            probabilidad_incumplimiento=form.probabilidad_incumplimiento.data,
            h20_predicciones=form.h20_predicciones.data,
            h20_prediccion_clase=form.h20_prediccion_clase.data
        )
        db.session.add(nuevo_prestamo)
        db.session.commit()
        flash('Registro guardado con éxito!', 'success')
        return redirect(url_for('index'))

    return render_template('loan/formulario.html', form=form, errors=form.errors,)

@loan_bp.route("/predict", methods=["GET", "POST"])
def predict():
    return jsonify({'message': 'PREDICT!'}), 201

@loan_bp.route('/predict/<int:id>', methods=['POST', 'GET'])
def predict_id(id):
    if request.method == 'POST':
        # Lógica para manejar la predicción usando el ID

        registro = Loan.query.get_or_404(id)
        import pandas as pd
        import driverlessai

        data = {
            'person_age': [registro.edad],
            'person_income': [registro.ingreso_anual],
            'person_home_ownership': [registro.propiedad_vivienda],
            'person_emp_length': [registro.anos_empleo],
            'loan_intent': [registro.proposito_prestamo],
            'loan_grade': [registro.calificacion_prestamo],
            'loan_amnt': [registro.monto_prestamo],
            'loan_int_rate': [registro.tasa_interes],
            'loan_percent_income': [registro.deuda_ingreso],
            'cb_person_default_on_file': [registro.incumplimiento_anterior],
            'cb_person_cred_hist_length': [registro.historial_crediticio],
        }
        df = pd.DataFrame(data)
        
        settings = ResConfigSettings.query.first()
        
        ADDRESS=settings.h2o_driverless_address
        USERNAME=settings.h2o_driverless_username 
        PASSWORD=settings.h2o_driverless_password 
        NAME_EXPERIMENT = settings.h2o_driverless_name_experiment 
        
        try:
            client = driverlessai.Client(address=ADDRESS, 
                                         username=USERNAME, 
                                         password=PASSWORD, 
                                         verify=False)
            experiment = client.experiments.get_by_name(NAME_EXPERIMENT)
            print("A",flush=True)
            prediction = experiment.predict(df).to_pandas()
            print("B",flush=True)
            
            predictions = prediction.to_json(orient='records')
            print("C",flush=True)
            
            registro.h20_predicciones  = str(predictions)
            print("D",flush=True)
            db.session.commit()  
            return redirect(url_for('loan.index'))

        except Exception as e:
            return jsonify({"mensaje": "Error en la predicción", "error": str(e)}), 500


    else:
        # Esto es para manejar la solicitud GET si es necesario
        return f'Prediction (GET) for loan ID: {id}'
