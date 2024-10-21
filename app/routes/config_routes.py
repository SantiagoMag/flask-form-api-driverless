from flask import Blueprint, render_template, request, redirect, url_for
from app.models.config_settings import ResConfigSettings
from app import db
from app.forms import ResConfigSettingsForm

config_bp = Blueprint('config', __name__)

@config_bp.route('/config', methods=['GET', 'POST'])
def configure_settings():
    form = ResConfigSettingsForm()
    settings = ResConfigSettings.query.first()

    if form.validate_on_submit():
        if settings is None:
            settings = ResConfigSettings(
                h2o_driverless_address=form.h2o_driverless_address.data,
                h2o_driverless_username=form.h2o_driverless_username.data,
                h2o_driverless_password=form.h2o_driverless_password.data,
                h2o_driverless_name_experiment=form.h2o_driverless_name_experiment.data,
                api_vm_url=form.api_vm_url.data
            )
            db.session.add(settings)
        else:
            settings.h2o_driverless_address = form.h2o_driverless_address.data
            settings.h2o_driverless_username = form.h2o_driverless_username.data
            settings.h2o_driverless_password = form.h2o_driverless_password.data
            settings.h2o_driverless_name_experiment = form.h2o_driverless_name_experiment.data
            settings.api_vm_url = form.api_vm_url.data

        db.session.commit()
        return redirect(url_for('loan.index'))

    if settings:
        form.h2o_driverless_address.data = settings.h2o_driverless_address
        form.h2o_driverless_username.data = settings.h2o_driverless_username
        form.h2o_driverless_password.data = settings.h2o_driverless_password
        form.h2o_driverless_name_experiment.data = settings.h2o_driverless_name_experiment
        form.api_vm_url.data = settings.api_vm_url

    return render_template('config_settings/config_form.html', form=form)



