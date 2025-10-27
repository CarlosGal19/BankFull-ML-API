from flask import Flask, jsonify, request
from db.config import Config
from db.connection import db
from dotenv import load_dotenv
import os
from schema.schemas import Education, Job, Marital, Contact, Month, Poutcome, Prediction
from helpers.catalogs import serialize_catalog
from helpers.get_prediction import get_prediction

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

port = int(os.getenv("PORT", 5000))

@app.route("/form_options", methods=["GET"])
def get_form_options():
    educations = serialize_catalog(Education.query.all())
    jobs = serialize_catalog(Job.query.all())
    marital_statuses = serialize_catalog(Marital.query.all())
    contacts = serialize_catalog(Contact.query.all())
    months = serialize_catalog(Month.query.all())
    poutcomes = serialize_catalog(Poutcome.query.all())

    return jsonify({
        "educations": educations,
        "jobs": jobs,
        "marital_statuses": marital_statuses,
        "contacts": contacts,
        "months": months,
        "poutcomes": poutcomes
    })

@app.route("/prediction", methods=["POST"])
def make_prediction():

    try:
        data = request.get_json()
        casted_data = {}

        casted_data['age'] = int(data.get("age"))
        casted_data['default'] = bool(data.get("default"))
        casted_data['balance'] = float(data.get("balance"))
        casted_data['housing'] = bool(data.get("housing"))
        casted_data['loan'] = bool(data.get("loan"))
        casted_data['day'] = int(data.get("day"))
        casted_data['duration'] = int(data.get("duration"))
        casted_data['campaign'] = int(data.get("campaign"))
        casted_data['pdays'] = int(data.get("pdays"))
        casted_data['previous'] = int(data.get("previous"))
        casted_data['job_id'] = int(data.get("job_id"))
        casted_data['marital_id'] = int(data.get("marital_id"))
        casted_data['education_level_id'] = int(data.get("education_level_id"))
        casted_data['contact_id'] = int(data.get("contact_id"))
        casted_data['month_id'] = int(data.get("month_id"))
        casted_data['poutcome_id'] = int(data.get("poutcome_id"))
        casted_data['real_value'] = data.get("real_value", None)

        predicted_value = get_prediction(casted_data)

        prediction = Prediction(
            age=casted_data['age'],
            default=casted_data['default'],
            balance=casted_data['balance'],
            housing=casted_data['housing'],
            loan=casted_data['loan'],
            day=casted_data['day'],
            duration=casted_data['duration'],
            campaign=casted_data['campaign'],
            pdays=casted_data['pdays'],
            previous=casted_data['previous'],
            job_id=casted_data['job_id'],
            marital_id=casted_data['marital_id'],
            education_level_id=casted_data['education_level_id'],
            contact_id=casted_data['contact_id'],
            month_id=casted_data['month_id'],
            poutcome_id=casted_data['poutcome_id'],
            predicted_value=predicted_value,
            real_value=casted_data['real_value'] if casted_data['real_value'] is not None else None
        )

        db.session.add(prediction)
        db.session.commit()

        return jsonify({
            "predicted_value": predicted_value
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

@app.route("/predictions", methods=["GET"])
def get_last_predictions():

    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    skip = (page - 1) * per_page

    last_predictions = (
        Prediction.query
        .order_by(Prediction.id.desc())
        .offset(skip)
        .limit(per_page)
        .all()
    )

    serialized_predictions = [
        {
            "id": pred.id,
            "age": pred.age,
            "default": pred.default,
            "balance": pred.balance,
            "housing": pred.housing,
            "loan": pred.loan,
            "day": pred.day,
            "duration": pred.duration,
            "campaign": pred.campaign,
            "pdays": pred.pdays,
            "previous": pred.previous,
            "job_name": pred.job.name,
            "marital_name": pred.marital.name,
            "education_level_name": pred.education_level.name,
            "contact_name": pred.contact.name,
            "month_name": pred.month.name,
            "poutcome_name": pred.poutcome.name,
            "predicted_value": pred.predicted_value
        }
        for pred in last_predictions
    ]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "data": serialized_predictions
    })
