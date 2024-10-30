from app import db



class ResConfigSettings(db.Model):
    __tablename__ = 'ResConfigSettings'
    __table_args__ = {"schema":"azure"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """
        H2O Configuration
    """
    api_vm_url = db.Column(db.String(255), nullable=True)

    def __init__(self, api_vm_url):
        self.api_vm_url = api_vm_url


