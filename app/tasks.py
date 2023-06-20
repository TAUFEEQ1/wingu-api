from app import db,celery
from app.models import DwellTime,UserModel
import pickle
from sklearn.cluster import DBSCAN

@celery.task
def train_model(username, web_id):
    # Load all dwell_times for the user and web_id
    dwell_times = DwellTime.query.filter_by(web_id=web_id, username=username).all()

    # Split dwell_times by ',' into a list
    dwells_list = []
    for dwell_time in dwell_times:
        dwells = dwell_time.dwells.split(',')
        dwells_list.extend(dwells)

    # Fit the model
    dbscan = DBSCAN(eps=0.5, min_samples=12)
    dbscan.fit(dwells_list)
    

    # Serialize the model to a pickle
    model_pickle = pickle.dumps(dbscan)

    # Save the model to the UserModel
    user_model = UserModel.query.filter_by(username=username, web_id=web_id).first()
    if user_model is None:
        user_model = UserModel(username=username, web_id=web_id, model=model_pickle)
        db.session.add(user_model)
    else:
        user_model.model = model_pickle
    db.session.commit()
