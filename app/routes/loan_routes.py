# Librerías estándar de Python
import os
import json
import urllib.request
import urllib.error

# Librerías de terceros
import numpy as np
import pandas as pd
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

# Importaciones específicas del proyecto
from app import db
from app.models.loan import Loan
from app.models.config_settings import ResConfigSettings
from app.forms.loan_form import LoanForm

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
    
    registros = Loan.query.filter(Loan.id.in_(selected_ids)).all()

    example = {}
    data = []
    for registro in registros:
        val = {
            'person_age': registro.edad,
            'person_income': registro.ingreso_anual,
            'person_home_ownership': registro.propiedad_vivienda,
            'person_emp_length': registro.anos_empleo,
            'loan_intent': registro.proposito_prestamo,
            'loan_grade': registro.calificacion_prestamo,
            'loan_amnt': registro.monto_prestamo,
            'loan_int_rate': registro.tasa_interes,
            'loan_percent_income': registro.deuda_ingreso,
            'cb_person_default_on_file': registro.incumplimiento_anterior,
            'cb_person_cred_hist_length': registro.historial_crediticio,
            'name': registro.nombre,
        }
        data.append(val)
        
    example["Inputs"] = {}
    example["Inputs"]["data"] = data
    example["GlobalParameters"] = {}
    example["GlobalParameters"]["method"] = "predict"
        
    settings = ResConfigSettings.query.first()
    URL=settings.api_vm_url

    body = str.encode(json.dumps(example))
    headers = {'Content-Type':'application/json'}
    req = urllib.request.Request(URL, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        results = json.loads(result.decode('utf-8'))

        for enum,registro in enumerate(registros):
            registro.h20_prediccion_clase = results["Results"][enum]
        
        db.session.commit()  
        return redirect(url_for('loan.index'))
        
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code), flush=True)
        print(error.info(), flush=True)
        print(error.read().decode("utf8", 'ignore'), flush=True)


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