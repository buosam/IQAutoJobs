from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    user_type = Column(String(20), nullable=False) # 'job_seeker' or 'employer'

class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='profile')
    name = Column(String(120))
    headline = Column(String(120))
    bio = Column(Text)
    resume = Column(String(200))

class CompanyProfile(db.Model):
    __tablename__ = 'company_profile'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='company_profile')
    name = Column(String(120), nullable=False)
    description = Column(Text)
    website = Column(String(120))
    logo = Column(String(200))

class Job(db.Model):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    company = Column(String(120), nullable=False)
    location = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    employer_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    employer = relationship('User', backref='jobs')

class Application(db.Model):
    __tablename__ = 'application'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    user = relationship('User', backref='applications')
    job = relationship('Job', backref='applications')
