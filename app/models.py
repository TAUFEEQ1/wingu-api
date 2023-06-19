from app import db


class WebClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(120), nullable=False)
    login_url = db.Column(db.String(512), nullable=False)
    dwell_times = db.relationship('DwellTime', backref='web_client', lazy=True)


class DwellTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    web_id = db.Column(db.Integer, db.ForeignKey('web_client.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password_dwell_times = db.Column(db.String(50), nullable=False)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    web_id = db.Column(db.Integer, db.ForeignKey('web_client.id'), nullable=False)
    model = db.Column(db.LargeBinary, nullable=False)
