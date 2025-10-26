import joblib
import pandas as pd

model = joblib.load("./model/logistic_model_20251026_114819.pkl")
scaler = joblib.load("./model/scaler_20251026_114819.pkl")

jobs = {
    4: "blue-collar",
    3: "entrepreneur",
    11: "housemaid",
    1: "management",
    6: "retired",
    9: "self-employed",
    8: "services",
    12: "student",
    2: "technician",
    10: "unemployed",
    5: "unknown",
    7: "admin"
}

poutcomes = {
    3: "other",
    4: "success",
    1: "unknown",
    2: "failure"
}

maritals = {
    1: "married",
    2: "single",
    3: "divorced"
}

months = {
    9: "aug",
    13: "dec",
    3: "feb",
    2: "jan",
    8: "jul",
    7: "jun",
    4: "mar",
    6: "may",
    12: "nov",
    11: "oct",
    10: "sep",
    5: "apr"
}

contact_methods = {
    3: "telephone",
    1: "unknown",
    2: "cellular"
}

def add_marital_features(transformed_data: dict, marital_id: int) -> dict:
    marital_status = maritals.get(marital_id, "unknown")

    transformed_data['marital_married'] = True if marital_status == "married" else False
    transformed_data['marital_single'] = True if marital_status == "single" else False

    return transformed_data

def add_job_features(transformed_data: dict, job_id: int) -> dict:
    job_name = jobs.get(job_id, "unknown")

    for job in jobs.values():
        if job == "admin":
            continue
        feature_name = f"job_{job}"
        transformed_data[feature_name] = True if job_name == job else False

    return transformed_data

def add_poutcome_features(transformed_data: dict, poutcome_id: int) -> dict:
    poutcome_name = poutcomes.get(poutcome_id, "unknown")

    transformed_data['poutcome_other'] = True if poutcome_name == "other" else False
    transformed_data['poutcome_success'] = True if poutcome_name == "success" else False
    transformed_data['poutcome_unknown'] = True if poutcome_name == "unknown" else False

    return transformed_data

def add_month_features(transformed_data: dict, month_id: int) -> dict:
    month_name = months.get(month_id, "unknown")

    for month in months.values():
        if month == "apr":
            continue
        feature_name = f"month_{month}"
        transformed_data[feature_name] = True if month_name == month else False

    return transformed_data

def add_contact_features(transformed_data: dict, contact_id: int) -> dict:
    contact_name = contact_methods.get(contact_id, "unknown")

    transformed_data['contact_telephone'] = True if contact_name == "telephone" else False
    transformed_data['contact_unknown'] = True if contact_name == "unknown" else False

    return transformed_data

def transform_data(casted_data: dict) -> dict:
    transformed_data = {}

    transformed_data['age'] = casted_data['age']
    transformed_data['education'] = casted_data['education_level_id']
    transformed_data['default'] = casted_data['default']
    transformed_data['balance'] = casted_data['balance']
    transformed_data['housing'] = casted_data['housing']
    transformed_data['loan'] = casted_data['loan']
    transformed_data['day'] = casted_data['day']
    transformed_data['duration'] = casted_data['duration']
    transformed_data['campaign'] = casted_data['campaign']
    transformed_data['pdays'] = casted_data['pdays']
    transformed_data['previous'] = casted_data['previous']

    transformed_data = add_job_features(transformed_data, casted_data['job_id'])
    transformed_data = add_marital_features(transformed_data, casted_data['marital_id'])
    transformed_data = add_contact_features(transformed_data, casted_data['contact_id'])
    transformed_data = add_month_features(transformed_data, casted_data['month_id'])
    transformed_data = add_poutcome_features(transformed_data, casted_data['poutcome_id'])

    return transformed_data

def get_prediction(casted_data: dict) -> float:
    transformed_data = transform_data(casted_data)

    df_predict = pd.DataFrame(transformed_data, index=[0])

    df_scaled = scaler.transform(df_predict)

    probs = model.predict_proba(df_scaled)[:,1]

    return float(probs[0])
