from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)

class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='profile')
    name = db.Column(db.String(120))
    headline = db.Column(db.String(120))
    bio = db.Column(db.Text)
    resume = db.Column(db.String(200))

class CompanyProfile(db.Model):
    __tablename__ = 'company_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='company_profile')
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(120))
    logo = db.Column(db.String(200))

class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employer = db.relationship('User', backref='jobs')

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user = db.relationship('User', backref='applications')
    job = db.relationship('Job', backref='applications')
