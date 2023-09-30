from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class IPAddr(db.Model):
    __tablename__ = "ip_addresses"
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), unique=True, nullable=False)
    status = db.Column(db.Enum('available','allocated', 'reserved'), nullable=False)
    customer_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    
    def __init__(self, ip_address, status):
        self.ip_address = ip_address
        self.status = status