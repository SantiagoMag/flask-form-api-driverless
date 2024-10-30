import numpy as np
from sqlalchemy.exc import SQLAlchemyError

import os
from werkzeug.utils import secure_filename
import pandas as pd
import driverlessai
import json
import requests
from flask import request, jsonify
from flask import Blueprint, render_template
from app.models.loan import Loan
from app.forms.loan_form import LoanForm
from app import db
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from app.models.config_settings import ResConfigSettings
from sqlalchemy import desc
from flask_paginate import Pagination, get_page_parameter

loan_bp = Blueprint('loan', __name__)

@loan_bp.route('/')
def index():
    registros = Loan.query.order_by(desc(Loan.id)).all()
    per_page = 10
    page = request.args.get(get_page_parameter(), type=int, default=1)
    total = Loan.query.count()
    pagination_data = Loan.query.order_by(desc(Loan.id)).paginate(page=page, per_page=per_page, error_out=False)
    registros = pagination_data.items
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')
    return render_template('loan/listar_registros.html', registros=registros, pagination=pagination)

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
        return redirect(url_for('loan.index'))

    return render_template('loan/formulario.html', form=form, errors=form.errors, edit_mode=False)

@loan_bp.route('/delete/<int:id>', methods=['POST'])
def delete_id(id):
    registro = Loan.query.get(id)
    if registro:
        db.session.delete(registro)
        db.session.commit()
        return redirect(url_for('loan.index'))
    return "Registro no encontrado", 404

@loan_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    registro = Loan.query.get_or_404(id)
    form = LoanForm(obj=registro)  # Asumiendo que LoanForm es tu formulario

    if form.validate_on_submit():
        # Aquí actualizas los datos
        form.populate_obj(registro)
        db.session.commit()
        return redirect(url_for('loan.index'))

    return render_template('loan/formulario.html', form=form, registro=registro, edit_mode=True)

@loan_bp.route("/predict_selected", methods=["POST"])
def predict_selected():
    selected_ids = request.form.getlist('selected_ids')

    if not selected_ids:
        flash("No seleccionaste ningún registro.", "warning")
        return redirect(url_for('loan.index'))
    
    # Consultar los registros seleccionados
    registros = Loan.query.filter(Loan.id.in_(selected_ids)).all()
        # Crear un diccionario con los datos necesarios para el DataFrame
    data = {
            'person_age': [registro.edad for registro in registros],
            'person_income': [registro.ingreso_anual for registro in registros],
            'person_home_ownership': [registro.propiedad_vivienda for registro in registros],
            'person_emp_length': [registro.anos_empleo for registro in registros],
            'loan_intent': [registro.proposito_prestamo for registro in registros],
            'loan_grade': [registro.calificacion_prestamo for registro in registros],
            'loan_amnt': [registro.monto_prestamo for registro in registros],
            'loan_int_rate': [registro.tasa_interes for registro in registros],
            'loan_percent_income': [registro.deuda_ingreso for registro in registros],
            'cb_person_default_on_file': [registro.incumplimiento_anterior for registro in registros],
            'cb_person_cred_hist_length': [registro.historial_crediticio for registro in registros] ,
            'name': [registro.nombre for registro in registros],
    }
    
    # Convertir el diccionario en un DataFrame
    df = pd.DataFrame(data)
    
    print(df,flush=False)
    print(len(df),flush=False)
    
    return jsonify({'message': 'PREDICT!'}), 201

@loan_bp.route('/predict/<int:id>', methods=['POST', 'GET'])
def predict_id(id):
    if request.method == 'POST':
        # Lógica para manejar la predicción usando el ID

        registro = Loan.query.get_or_404(id)

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
            'name': [registro.nombre],
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
            prediction = experiment.predict(df).to_pandas()
            predictions = prediction.to_json(orient='records')
            
            
            val_max = 0
            class_max = ""
            predictions = json.loads(predictions)

            for k,v in predictions[0].items() :
                if v > val_max :
                    val_max = v
                    class_max = k[-1]


            registro.h20_predicciones  = str(predictions)
            registro.h20_prediccion_clase  = str(class_max)
            registro.probabilidad_incumplimiento  = float(val_max)
            
            
            db.session.commit()  
            return redirect(url_for('loan.index'))

        except Exception as e:
            return jsonify({"mensaje": "Error en la predicción", "error": str(e)}), 500


    else:
        # Esto es para manejar la solicitud GET si es necesario
        return f'Prediction (GET) for loan ID: {id}'


@loan_bp.route("/bulk_upload", methods=["POST"])
def bulk_upload():
    # Verificar si el archivo fue enviado en la solicitud
    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo', 'warning')
        return redirect(url_for('loan.index'))

    file = request.files['file']
    if file.filename == '':
        flash('Archivo no válido', 'warning')
        return redirect(url_for('loan.index'))

    if file:
        filename = secure_filename(file.filename)
        os.makedirs('uploads', exist_ok=True)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        try:
            df = pd.read_csv(file_path,sep=",")

            replace_columns={
                    'name'                          :'nombre',  
                    "person_age"                    :'edad',
                    "person_income"                 :"ingreso_anual",
                    "person_home_ownership"         :"propiedad_vivienda",
                    "person_emp_length"             :"anos_empleo",
                    "loan_intent"                   :"proposito_prestamo",
                    "loan_grade"                    :"calificacion_prestamo",
                    "loan_amnt"                     :"monto_prestamo",
                    "loan_int_rate"                 :"tasa_interes",
                    "loan_status"                   :"estado_deuda",
                    "loan_percent_income"           :"deuda_ingreso",
                    "cb_person_default_on_file"     :"incumplimiento_anterior",
                    "cb_person_cred_hist_length"    :"historial_crediticio"
            }
            
            df = df.rename(columns=replace_columns, errors="raise")
            df = df.replace(np.nan, None)
            records = df.to_dict(orient='records')

            print("----------------------------------------",flush=True)
            db.session.bulk_insert_mappings(Loan, records)
            db.session.commit()

            flash("Carga masiva completada exitosamente.", "success")
            print("-3", flush=True)
            
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error en la transacción: {str(e)}", "danger")
            print(f"Detalle del error: {e}")
            return redirect(url_for('loan.index'))
        return redirect(url_for('loan.index'))



@loan_bp.route('/delete_all', methods=['POST'])
def delete_all():
    try:
        # Borra todos los registros de la tabla Loan
        Loan.query.delete()
        db.session.commit()
        flash("Toda la información ha sido eliminada correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error al eliminar la información: {}".format(e), "danger")
    return redirect(url_for('loan.index'))