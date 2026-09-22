import uuid
from datetime import datetime, timezone
from typing import Generator
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Index,
    JSON,
    Uuid,
    create_engine
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from config import settings

Base = declarative_base()

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    extracted_requirements = Column(JSON, nullable=False, default=dict)
    required_years_experience = Column(Integer, nullable=True)
    seniority_level = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    candidates = relationship("Candidate", back_populates="job", cascade="all, delete-orphan")
    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    job_id = Column(Uuid, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_text = Column(Text, nullable=False)
    extracted_skills = Column(JSON, nullable=False, default=dict)
    experience_years = Column(Integer, nullable=True, default=0)
    certification_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    job = relationship("JobPosting", back_populates="candidates")
    match = relationship("JobMatch", back_populates="candidate", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_candidates_job_id", "job_id"),
    )


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    candidate_id = Column(Uuid, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Uuid, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float, nullable=False)
    matched_skills = Column(JSON, nullable=False, default=list)
    missing_skills = Column(JSON, nullable=False, default=list)
    extra_skills = Column(JSON, nullable=False, default=list)
    assessment = Column(Text, nullable=False, default="")
    rank = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    candidate = relationship("Candidate", back_populates="match")
    job = relationship("JobPosting", back_populates="matches")

    __table_args__ = (
        Index("idx_job_matches_candidate_id", "candidate_id"),
        Index("idx_job_matches_job_id", "job_id"),
        Index("idx_job_matches_score", "match_score"),
    )


# Database Engine and Session
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Dependency for obtaining a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
