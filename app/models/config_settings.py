from app import db



class ResConfigSettings(db.Model):
    __tablename__ = 'ResConfigSettings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """
        H2O Configuration
    """
    h2o_driverless_address = db.Column(db.String(255), nullable=True)
    h2o_driverless_username = db.Column(db.String(255), nullable=True)
    h2o_driverless_password = db.Column(db.String(255), nullable=True)
    h2o_driverless_name_experiment = db.Column(db.String(255), nullable=True)
    api_vm_url = db.Column(db.String(255), nullable=True)

    def __init__(self, h2o_driverless_address, h2o_driverless_username, h2o_driverless_password, h2o_driverless_name_experiment, api_vm_url):
        self.h2o_driverless_address = h2o_driverless_address
        self.h2o_driverless_username = h2o_driverless_username
        self.h2o_driverless_password = h2o_driverless_password
        self.h2o_driverless_name_experiment = h2o_driverless_name_experiment
        self.api_vm_url = api_vm_url


