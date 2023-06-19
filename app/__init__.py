from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from configparser import ConfigParser
from flask_mail import Mail
from celery import Celery

appl = Flask(__name__)
appl.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'  # Replace with your preferred database URI

db = SQLAlchemy(appl)
migrate = Migrate(appl, db)

app_config = ConfigParser()
app_config.read("settings.ini")
appl.config['MAIL_SERVER'] = app_config.get('DEFAULT','MAIL_SERVER')
appl.config['MAIL_PORT'] = app_config.get('DEFAULT','MAIL_PORT')
appl.config['MAIL_USERNAME'] = app_config.get('DEFAULT','MAIL_USERNAME')
appl.config['MAIL_PASSWORD'] = app_config.get('DEFAULT','MAIL_PASSWORD')
appl.config['MAIL_USE_SSL'] = True

mail = Mail(appl)

appl.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
appl.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(appl.name, broker=appl.config['CELERY_BROKER_URL'])
celery.conf.update(appl.config)

