from db.connection import db

class Education(db.Model):
    __tablename__ = 'education_levels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    abreviation = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    abreviation = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Marital(db.Model):
    __tablename__ = 'marital_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    abreviation = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Contact(db.Model):
    __tablename__ = 'contact_methods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    abreviation = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Month(db.Model):
    __tablename__ = 'month'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    abreviation = db.Column(db.String(5), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Poutcome(db.Model):
    __tablename__ = 'poutcome'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    abreviation = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Prediction(db.Model):
    __tablename__ = 'prediction'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    default = db.Column(db.Boolean, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    housing = db.Column(db.Boolean, nullable=False)
    loan = db.Column(db.Boolean, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    campaign = db.Column(db.Integer, nullable=False)
    pdays = db.Column(db.Integer, nullable=False)
    previous = db.Column(db.Integer, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    marital_id = db.Column(db.Integer, db.ForeignKey('marital_status.id'), nullable=False)
    education_level_id = db.Column(db.Integer, db.ForeignKey('education_levels.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact_methods.id'), nullable=False)
    month_id = db.Column(db.Integer, db.ForeignKey('month.id'), nullable=False)
    poutcome_id = db.Column(db.Integer, db.ForeignKey('poutcome.id'), nullable=False)
    predicted_value = db.Column(db.Float, nullable=False)
    real_value = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    job = db.relationship('Job', backref=db.backref('predictions', lazy=True))
    marital = db.relationship('Marital', backref=db.backref('predictions', lazy=True))
    education_level = db.relationship('Education', backref=db.backref('predictions', lazy=True))
    contact = db.relationship('Contact', backref=db.backref('predictions', lazy=True))
    month = db.relationship('Month', backref=db.backref('predictions', lazy=True))
    poutcome = db.relationship('Poutcome', backref=db.backref('predictions', lazy=True))
