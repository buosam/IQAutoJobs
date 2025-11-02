#!/usr/bin/env python3
"""
Sample Data Creation Script for IQAutoJobs

This script creates sample data for development and testing purposes.
It populates the database with:
- Sample users (candidates, employers, admin)
- Sample companies
- Sample job postings
- Sample applications
- Sample audit logs

Usage: python create_sample_data.py
"""

import asyncio
import random
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, delete

from app.db.base import Base
from app.db.models import User, Company, Job, Application, SavedJob, AuditLog, UserRole
from app.core.security import get_password_hash
from app.repositories.base import BaseRepository
from app.repositories.user_repo import UserRepository
from app.repositories.company_repo import CompanyRepository
from app.repositories.job_repo import JobRepository
from app.repositories.application_repo import ApplicationRepository
from app.repositories.saved_job_repo import SavedJobRepository
from app.repositories.audit_log_repo import AuditLogRepository

# Sample data
SAMPLE_COMPANIES = [
    {
        "name": "TechCorp Solutions",
        "description": "Leading technology company specializing in AI and machine learning solutions.",
        "industry": "Technology",
        "location": "San Francisco, CA",
        "website": "https://techcorp.com",
        "size": "500-1000",
    },
    {
        "name": "InnovateLab",
        "description": "Startup focused on innovative software development and digital transformation.",
        "industry": "Software",
        "location": "New York, NY",
        "website": "https://innovatelab.io",
        "size": "50-200",
    },
    {
        "name": "DataFlow Systems",
        "description": "Data analytics and business intelligence platform provider.",
        "industry": "Data Analytics",
        "location": "Austin, TX",
        "website": "https://dataflow.com",
        "size": "200-500",
    },
    {
        "name": "CloudFirst Technologies",
        "description": "Cloud infrastructure and DevOps solutions company.",
        "industry": "Cloud Computing",
        "location": "Seattle, WA",
        "website": "https://cloudfirst.tech",
        "size": "100-300",
    },
    {
        "name": "MobileFirst Apps",
        "description": "Mobile app development and digital agency.",
        "industry": "Mobile Development",
        "location": "Los Angeles, CA",
        "website": "https://mobilefirst.com",
        "size": "30-100",
    }
]

SAMPLE_JOBS = [
    {
        "title": "Senior Frontend Developer",
        "description": "We are looking for a Senior Frontend Developer to join our team. You will be responsible for developing user-facing web applications using React, TypeScript, and modern frontend technologies.",
        "category": "Engineering",
        "type": "Full-time",
        "experience_level": "Senior",
        "salary_min": 120000,
        "salary_max": 180000,
        "currency": "USD"
    },
    {
        "title": "Backend Software Engineer",
        "description": "Join our backend team to build scalable APIs and microservices. You'll work with Python, FastAPI, and PostgreSQL to create robust server-side applications.",
        "category": "Engineering",
        "type": "Full-time",
        "experience_level": "Mid-Level",
        "salary_min": 100000,
        "salary_max": 150000,
        "currency": "USD"
    },
    {
        "title": "Data Scientist",
        "description": "We're seeking a Data Scientist to help us extract insights from large datasets and build machine learning models. You'll work with Python, TensorFlow, and various data visualization tools.",
        "category": "Data Science",
        "type": "Full-time",
        "experience_level": "Senior",
        "salary_min": 130000,
        "salary_max": 190000,
        "currency": "USD"
    },
    {
        "title": "DevOps Engineer",
        "description": "Looking for a DevOps Engineer to automate our infrastructure and deployment processes. You'll work with Docker, Kubernetes, and CI/CD pipelines to ensure smooth operations.",
        "category": "DevOps",
        "type": "Full-time",
        "experience_level": "Mid-Level",
        "salary_min": 110000,
        "salary_max": 160000,
        "currency": "USD"
    },
    {
        "title": "UX/UI Designer",
        "description": "Join our design team to create beautiful and intuitive user interfaces. You'll work closely with product managers and developers to deliver exceptional user experiences.",
        "category": "Design",
        "type": "Full-time",
        "experience_level": "Mid-Level",
        "salary_min": 90000,
        "salary_max": 130000,
        "currency": "USD"
    }
]

SAMPLE_USERS = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "role": "candidate",
        "headline": "Senior Frontend Developer",
        "location": "San Francisco, CA",
        "skills": ["React", "TypeScript", "JavaScript", "HTML5", "CSS3", "Redux"]
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "password": "password123",
        "role": "candidate",
        "headline": "Data Scientist",
        "location": "New York, NY",
        "skills": ["Python", "Machine Learning", "TensorFlow", "Pandas", "SQL", "Statistics"]
    },
    {
        "first_name": "Mike",
        "last_name": "Johnson",
        "email": "mike.johnson@example.com",
        "password": "password123",
        "role": "employer",
        "headline": "CTO at TechCorp",
        "location": "San Francisco, CA",
        "skills": ["Leadership", "Strategy", "Technology", "Management"]
    },
    {
        "first_name": "Sarah",
        "last_name": "Wilson",
        "email": "sarah.wilson@example.com",
        "password": "password123",
        "role": "employer",
        "headline": "HR Director at InnovateLab",
        "location": "New York, NY",
        "skills": ["Recruitment", "HR", "Management", "Communication"]
    },
    {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@iqautojobs.com",
        "password": "admin123",
        "role": "admin",
        "headline": "System Administrator",
        "location": "Remote",
        "skills": ["Administration", "Security", "System Management"]
    }
]

LOCATIONS = [
    "San Francisco, CA",
    "New York, NY",
    "Austin, TX",
    "Seattle, WA",
    "Los Angeles, CA",
    "Boston, MA",
    "Chicago, IL",
    "Denver, CO",
    "Miami, FL",
    "Portland, OR"
]

SKILLS_POOL = [
    "JavaScript", "Python", "Java", "C++", "React", "Angular", "Vue.js", "Node.js",
    "TypeScript", "HTML5", "CSS3", "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL",
    "AWS", "Docker", "Kubernetes", "DevOps", "CI/CD", "Git", "Linux", "Machine Learning",
    "Data Science", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn",
    "Project Management", "Agile", "Scrum", "Leadership", "Communication", "Teamwork"
]

async def create_sample_data():
    """Create sample data in the database."""
    # Database connection
    engine = create_async_engine("postgresql+asyncpg://iqautojobs_user:iqautojobs_password@localhost/iqautojobs")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Clean the database
            await session.execute(delete(AuditLog))
            await session.execute(delete(SavedJob))
            await session.execute(delete(Application))
            await session.execute(delete(Job))
            await session.execute(delete(Company))
            await session.execute(delete(User))
            await session.commit()
            print("Database cleaned.")

            # Create repositories
            user_repo = UserRepository(session)
            company_repo = CompanyRepository(session)
            job_repo = JobRepository(session)
            application_repo = ApplicationRepository(session)
            saved_job_repo = SavedJobRepository(session)
            audit_repo = AuditLogRepository(session)

            print("Creating sample data...")

            # Create users
            users = []
            for user_data in SAMPLE_USERS:
                user_create_data = user_data.copy()
                user_create_data["hashed_password"] = await get_password_hash(user_create_data.pop("password"))
                user_create_data["role"] = user_create_data["role"].upper()
                user = await user_repo.create(user_create_data)
                users.append(user)
                print(f"Created user: {user.first_name} {user.last_name}")

            # Create companies
            companies = []
            for i, company_data in enumerate(SAMPLE_COMPANIES):
                company_create_data = company_data.copy()
                company_create_data["id"] = uuid.uuid4()
                company_create_data["owner_user_id"] = users[2 + (i % 2)].id
                company_create_data["slug"] = company_create_data["name"].lower().replace(" ", "-")
                company = await company_repo.create(company_create_data)
                companies.append(company)
                print(f"Created company: {company.name}")
            
            # Create jobs
            jobs = []
            for i, job_data in enumerate(SAMPLE_JOBS):
                job_create_data = job_data.copy()
                job_create_data["id"] = uuid.uuid4()
                job_create_data["location"] = random.choice(LOCATIONS)
                job_create_data["company_id"] = companies[i % len(companies)].id
                job_create_data["status"] = "PUBLISHED"
                job_create_data["slug"] = job_create_data["title"].lower().replace(" ", "-")
                if job_create_data["type"] == "Full-time":
                    job_create_data["type"] = "FT"
                elif job_create_data["type"] == "Part-time":
                    job_create_data["type"] = "PT"
                elif job_create_data["type"] == "Contract":
                    job_create_data["type"] = "CONTRACT"
                elif job_create_data["type"] == "Internship":
                    job_create_data["type"] = "INTERN"
                job = await job_repo.create(job_create_data)
                jobs.append(job)
                print(f"Created job: {job.title} at {companies[i % len(companies)].name}")

            # Create applications
            application_statuses = ["RECEIVED", "SHORTLISTED", "INTERVIEW", "REJECTED", "HIRED"]
            for i in range(20):  # Create 20 applications
                candidate = random.choice([u for u in users if u.role == UserRole.CANDIDATE])
                job = random.choice(jobs)

                application_create_data = {
                    "id": uuid.uuid4(),
                    "candidate_user_id": candidate.id,
                    "job_id": job.id,
                    "status": random.choice(application_statuses),
                    "cover_letter": f"I am excited to apply for the {job.title} position at {job.company.name}. My skills and experience make me a strong candidate for this role.",
                    "cv_key": "dummy_cv.pdf"
                }
                await application_repo.create(application_create_data)
                print(f"Created application: {candidate.first_name} {candidate.last_name} -> {job.title}")

            # Create saved jobs
            saved_jobs_set = set()
            for i in range(15):  # Create 15 saved jobs
                candidate = random.choice([u for u in users if u.role == UserRole.CANDIDATE])
                job = random.choice(jobs)

                if (candidate.id, job.id) in saved_jobs_set:
                    continue

                saved_job_create_data = {
                    "id": uuid.uuid4(),
                    "user_id": candidate.id,
                    "job_id": job.id,
                }
                await saved_job_repo.create(saved_job_create_data)
                saved_jobs_set.add((candidate.id, job.id))
                print(f"Created saved job: {candidate.first_name} {candidate.last_name} saved {job.title}")
            
            # Create audit logs
            actions = ["USER_LOGIN", "USER_LOGOUT", "JOB_CREATE", "JOB_UPDATE", "APPLICATION_SUBMIT"]
            for i in range(50):  # Create 50 audit logs
                user = random.choice(users)
                action = random.choice(actions)

                audit_log_create_data = {
                    "id": uuid.uuid4(),
                    "actor_user_id": user.id,
                    "action": action,
                    "subject_type": random.choice(["user", "company", "job", "application"]),
                    "subject_id": str(uuid.uuid4()),
                    "payload": {"details": f"User {user.first_name} {user.last_name} performed {action} action"},
                }
                await audit_repo.create(audit_log_create_data)
                print(f"Created audit log: {user.first_name} {user.last_name} - {action}")
            
            print("\nSample data creation completed!")
            print(f"Created {len(users)} users")
            print(f"Created {len(companies)} companies")
            print(f"Created {len(jobs)} jobs")
            print(f"Created 20 applications")
            print(f"Created 15 saved jobs")
            print(f"Created 50 audit logs")
        except Exception as e:
            print(f"An error occurred: {e}")
            await session.rollback()
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(create_sample_data())
