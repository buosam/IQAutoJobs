"""Submit a Senior Software Engineer job posting to the PostgreSQL database.

This script connects to the configured PostgreSQL database and ensures that a
published "Senior Software Engineer" role located in Erbil exists.  It creates a
supporting employer user and company if they are missing so the job can be
inserted safely in an empty database.

Usage:
    python -m backend.scripts.submit_job

Make sure the ``DATABASE_URL`` environment variable points to your PostgreSQL
instance before running the script.  Optionally place the variable inside a
``.env`` file at the project root or inside ``backend/.env``.
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# Ensure the backend package is importable when running as a module
BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Load environment variables from .env files if they exist
for env_path in (PROJECT_ROOT / ".env", BACKEND_DIR / ".env"):
    if env_path.exists():
        load_dotenv(env_path, override=False)

# Imports that rely on the backend package
from app.db.models import (  # noqa: E402  pylint: disable=wrong-import-position
    Company,
    EmploymentType,
    Job,
    JobStatus,
    User,
    UserRole,
)


JOB_TITLE = "Senior Software Engineer"
JOB_LOCATION = "Erbil"
EMPLOYER_EMAIL = "erbil.employer@iqautojobs.local"
COMPANY_NAME = "Erbil Tech Alliance"
COMPANY_DESCRIPTION = (
    "A technology collective in Erbil focused on building scalable software "
    "solutions for global clients."
)


def _get_database_url() -> str:
    """Return the DATABASE_URL environment variable or raise an error."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is required to submit a job."
        )
    return database_url


def _create_engine(database_url: str):
    """Create a synchronous SQLAlchemy engine for the provided URL."""
    url = make_url(database_url)
    if "+" in url.drivername:
        url = url.set(drivername=url.drivername.split("+")[0])
    return create_engine(url, future=True)


def _slugify(value: str) -> str:
    """Generate a URL-friendly slug from the given text."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def _ensure_employer(session: Session) -> Tuple[User, bool]:
    """Fetch or create the employer user required for the job posting."""
    statement = select(User).where(User.email == EMPLOYER_EMAIL)
    employer = session.execute(statement).scalar_one_or_none()
    if employer:
        return employer, False

    employer = User(
        id=uuid4(),
        email=EMPLOYER_EMAIL,
        role=UserRole.EMPLOYER,
        first_name="Erbil",
        last_name="Coordinator",
        is_active=True,
    )
    session.add(employer)
    session.flush()
    return employer, True


def _ensure_company(session: Session, employer: User) -> Tuple[Company, bool]:
    """Fetch or create the company that will own the job posting."""
    company_slug = _slugify(COMPANY_NAME)
    statement = select(Company).where(Company.slug == company_slug)
    company = session.execute(statement).scalar_one_or_none()
    if company:
        return company, False

    company = Company(
        id=uuid4(),
        owner_user_id=employer.id,
        name=COMPANY_NAME,
        slug=company_slug,
        description=COMPANY_DESCRIPTION,
        industry="Technology",
        size="50-200",
        location=JOB_LOCATION,
    )
    session.add(company)
    session.flush()
    return company, True


def _generate_unique_slug(session: Session, company_id, base_slug: str) -> str:
    """Generate a slug unique to the given company."""
    slug = base_slug
    suffix = 2
    while session.execute(
        select(Job.id).where(Job.company_id == company_id, Job.slug == slug)
    ).scalar_one_or_none():
        slug = f"{base_slug}-{suffix}"
        suffix += 1
    return slug


def _ensure_job(session: Session, company: Company) -> Tuple[Job, bool]:
    """Create the Senior Software Engineer job if it does not exist."""
    statement = select(Job).where(
        Job.company_id == company.id,
        Job.title == JOB_TITLE,
        Job.location == JOB_LOCATION,
    )
    job = session.execute(statement).scalar_one_or_none()
    if job:
        return job, False

    base_slug = _slugify(JOB_TITLE)
    slug = _generate_unique_slug(session, company.id, base_slug)

    job = Job(
        id=uuid4(),
        company_id=company.id,
        title=JOB_TITLE,
        slug=slug,
        description=(
            "Lead the development of resilient backend services, mentor a "
            "growing engineering team, and collaborate with stakeholders to "
            "deliver products for international clients."
        ),
        location=JOB_LOCATION,
        type=EmploymentType.FT,
        category="Engineering",
        experience_level="Senior",
        salary_min=60000,
        salary_max=85000,
        currency="USD",
        status=JobStatus.PUBLISHED,
        published_at=datetime.now(timezone.utc),
        apply_email="careers@erbiltechalliance.example",
    )
    session.add(job)
    session.flush()
    return job, True


def submit_job() -> None:
    """Ensure the Erbil Senior Software Engineer role exists in the database."""
    database_url = _get_database_url()
    engine = _create_engine(database_url)

    created_user = created_company = created_job = False

    try:
        with Session(bind=engine) as session:
            employer, created_user = _ensure_employer(session)
            company, created_company = _ensure_company(session, employer)
            job, created_job = _ensure_job(session, company)
            session.commit()
    except SQLAlchemyError as exc:
        raise RuntimeError("Failed to submit job to the database") from exc

    if created_job:
        print(
            f"Created job '{JOB_TITLE}' in {JOB_LOCATION} for company "
            f"'{COMPANY_NAME}'."
        )
    else:
        print(
            f"Job '{JOB_TITLE}' in {JOB_LOCATION} already exists for "
            f"company '{COMPANY_NAME}'."
        )

    if created_company:
        print(f"Created company '{COMPANY_NAME}' and associated it with the job.")
    if created_user:
        print(
            "Created employer account '"
            f"{EMPLOYER_EMAIL}' as the owner of the company."
        )


if __name__ == "__main__":
    submit_job()
