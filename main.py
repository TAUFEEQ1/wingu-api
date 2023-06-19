from app import appl,db
from flask import request, jsonify
from app.models import WebClient, DwellTime, UserModel
import requests
import pickle
from flask_mail import Message
from app import mail
from app.tasks import train_model

@appl.route("login", methods=['POST'])
def login():
    web_host = request.host
    username = request.json['username']
    password = request.json['password']
    dwells = request.json['dwells']

    # Get the first matching WebClient instance based on the host field
    web_client = WebClient.query.filter_by(host=web_host).first()

    # Attempt login at the web host with the username and password
    response = requests.post(web_client.login_url, json={'username': username, 'password': password})

    if response.status_code == 200:
        # Login successful
        login_sessions = DwellTime.query.filter_by(web_id=web_client.id, username=username).count()

        if login_sessions < 15:
            # Record the session in DwellTime
            dwell_time = DwellTime(web_id=web_client.id, username=username,password_dwell_times=",".join(dwells[:8]))
            db.session.add(dwell_time)
            db.session.commit()
            if login_sessions==14:
                train_model.delay(username,web_client.id)
        else:
            # Login sessions exceeded 15, fetch the model pickle using the username and web_id
            user_model = UserModel.query.filter_by(username=username, web_id=web_client.id).first()

            if user_model is not None:
                # Load the model pickle
                model = pickle.loads(user_model.model)

                # Use the model to predict 1 or 0 based on dwells array
                prediction = model.predict([dwells])
                # Rest of your code...
                if prediction[0]==0:
                    message = Message('Suspicious Activity Detected', recipients=[username])
                    message.body = f"Hello {username}, we have detected suspicious activity on your account. Please review your recent login attempt and contact our support team if you did not perform this action."
                    mail.send(message)

    # Login unsuccessful, return the response
    return jsonify(response.json()), response.status_code
