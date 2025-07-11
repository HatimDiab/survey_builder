from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .connection import Base

class HubProject(Base):
    """Hub table for projects (surveys)"""
    __tablename__ = "hub_project"
    
    hk_project = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bk_project = Column(String, nullable=False, unique=True)  # Business key: company_name + survey_title
    load_dts = Column(DateTime, nullable=False, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app")

class HubClient(Base):
    """Hub table for clients (companies)"""
    __tablename__ = "hub_client"
    
    hk_client = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bk_client = Column(String, nullable=False, unique=True)  # Business key: company_name
    load_dts = Column(DateTime, nullable=False, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app")

class HubObjective(Base):
    """Hub table for objectives (formerly categories)"""
    __tablename__ = "hub_objective"
    
    hk_objective = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bk_objective = Column(String, nullable=False, unique=True)  # Business key: objective_id
    load_dts = Column(DateTime, nullable=False, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app")

class HubQuestion(Base):
    """Hub table for questions"""
    __tablename__ = "hub_question"
    
    hk_question = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bk_question = Column(String, nullable=False, unique=True)  # Business key: question_id
    load_dts = Column(DateTime, nullable=False, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app")

class LinkProjectObjective(Base):
    """Link table connecting projects to objectives"""
    __tablename__ = "link_project_objective"
    
    hk_project_objective = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hk_project = Column(UUID(as_uuid=True), ForeignKey("hub_project.hk_project"), nullable=False)
    hk_objective = Column(UUID(as_uuid=True), ForeignKey("hub_objective.hk_objective"), nullable=False)
    load_dts = Column(DateTime, nullable=False, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app")
    
    __table_args__ = (UniqueConstraint('hk_project', 'hk_objective'),)

class LinkProjectQuestion(Base):
    """Link table connecting projects to questions"""
    __tablename__ = "link_project_question"
    
    hk_project_question = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hk_project = Column(UUID(as_uuid=True), ForeignKey("hub_project.hk_project"), nullable=False)
    hk_question = Column(UUID(as_uuid=True), ForeignKey("hub_question.hk_question"), nullable=False)
    load_dts = Column(DateTime, nullable=False, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app")
    
    __table_args__ = (UniqueConstraint('hk_project', 'hk_question'),)

class SatProject(Base):
    """Satellite table for project attributes"""
    __tablename__ = "sat_project"
    
    hk_project = Column(UUID(as_uuid=True), ForeignKey("hub_project.hk_project"), primary_key=True)
    name = Column(String, nullable=False)
    duration_min = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    load_dts = Column(DateTime, nullable=False, primary_key=True, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app")

class SatClient(Base):
    """Satellite table for client attributes"""
    __tablename__ = "sat_client"
    
    hk_client = Column(UUID(as_uuid=True), ForeignKey("hub_client.hk_client"), primary_key=True)
    company_name = Column(String, nullable=False)
    logo_url = Column(String)
    primary_color = Column(String)
    secondary_color = Column(String)
    load_dts = Column(DateTime, nullable=False, primary_key=True, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app")

class SatObjective(Base):
    """Satellite table for objective attributes"""
    __tablename__ = "sat_objective"
    
    hk_objective = Column(UUID(as_uuid=True), ForeignKey("hub_objective.hk_objective"), primary_key=True)
    label = Column(String, nullable=False)
    display_order = Column(Integer, nullable=False)
    load_dts = Column(DateTime, nullable=False, primary_key=True, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app")

class SatQuestion(Base):
    """Satellite table for question attributes"""
    __tablename__ = "sat_question"
    
    hk_question = Column(UUID(as_uuid=True), ForeignKey("hub_question.hk_question"), primary_key=True)
    text = Column(Text, nullable=False)
    q_type = Column(String, nullable=False)  # 'multiple_choice', 'text', etc.
    est_seconds = Column(Integer, nullable=False)
    options = Column(Text)  # JSON string for multiple choice options
    load_dts = Column(DateTime, nullable=False, primary_key=True, default=datetime.utcnow)
    rec_src = Column(String, nullable=False, default="app") 