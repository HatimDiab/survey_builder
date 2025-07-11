from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import json

from ..db.models import (
    HubProject, HubClient, HubObjective, HubQuestion,
    LinkProjectObjective, LinkProjectQuestion,
    SatProject, SatClient, SatObjective, SatQuestion
)
from ..schemas.survey import ObjectiveBase, QuestionBase, ClientCustomizationBase

class SurveyCRUD:
    """CRUD operations for survey data using Data Vault model"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _get_or_create_hub_project(self, company_name: str, survey_title: str) -> HubProject:
        """Get or create hub project entry"""
        bk_project = f"{company_name}_{survey_title}"
        
        hub_project = self.db.query(HubProject).filter(
            HubProject.bk_project == bk_project
        ).first()
        
        if not hub_project:
            hub_project = HubProject(bk_project=bk_project)
            self.db.add(hub_project)
            self.db.flush()  # Get the ID without committing
        
        return hub_project
    
    def _get_or_create_hub_client(self, company_name: str) -> HubClient:
        """Get or create hub client entry"""
        hub_client = self.db.query(HubClient).filter(
            HubClient.bk_client == company_name
        ).first()
        
        if not hub_client:
            hub_client = HubClient(bk_client=company_name)
            self.db.add(hub_client)
            self.db.flush()
        
        return hub_client
    
    def _get_or_create_hub_objective(self, objective_id: str) -> HubObjective:
        """Get or create hub objective entry"""
        hub_objective = self.db.query(HubObjective).filter(
            HubObjective.bk_objective == objective_id
        ).first()
        
        if not hub_objective:
            hub_objective = HubObjective(bk_objective=objective_id)
            self.db.add(hub_objective)
            self.db.flush()
        
        return hub_objective
    
    def _get_or_create_hub_question(self, question_id: str) -> HubQuestion:
        """Get or create hub question entry"""
        hub_question = self.db.query(HubQuestion).filter(
            HubQuestion.bk_question == question_id
        ).first()
        
        if not hub_question:
            hub_question = HubQuestion(bk_question=question_id)
            self.db.add(hub_question)
            self.db.flush()
        
        return hub_question
    
    def save_objectives(self, company_name: str, survey_title: str, objectives: List[ObjectiveBase]) -> Dict[str, Any]:
        """Save objectives using Data Vault model"""
        try:
            # Get or create hub project
            hub_project = self._get_or_create_hub_project(company_name, survey_title)
            
            # Create satellite project if it doesn't exist
            sat_project = self.db.query(SatProject).filter(
                SatProject.hk_project == hub_project.hk_project
            ).first()
            
            if not sat_project:
                sat_project = SatProject(
                    hk_project=hub_project.hk_project,
                    name=survey_title,
                    duration_min=len(objectives) * 5  # Estimate 5 min per objective
                )
                self.db.add(sat_project)
            
            saved_objectives = []
            
            for i, objective in enumerate(objectives):
                # Create unique objective ID
                objective_id = f"{company_name}_{survey_title}_obj_{i}"
                
                # Get or create hub objective
                hub_objective = self._get_or_create_hub_objective(objective_id)
                
                # Create satellite objective
                sat_objective = SatObjective(
                    hk_objective=hub_objective.hk_objective,
                    label=objective.label,
                    display_order=objective.display_order
                )
                self.db.add(sat_objective)
                
                # Create link if it doesn't exist
                link = self.db.query(LinkProjectObjective).filter(
                    and_(
                        LinkProjectObjective.hk_project == hub_project.hk_project,
                        LinkProjectObjective.hk_objective == hub_objective.hk_objective
                    )
                ).first()
                
                if not link:
                    link = LinkProjectObjective(
                        hk_project=hub_project.hk_project,
                        hk_objective=hub_objective.hk_objective
                    )
                    self.db.add(link)
                
                saved_objectives.append({
                    "id": objective_id,
                    "label": objective.label,
                    "display_order": objective.display_order
                })
            
            self.db.commit()
            
            return {
                "status": "success",
                "message": f"Saved {len(objectives)} objectives",
                "objectives": saved_objectives
            }
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error saving objectives: {str(e)}")
    
    def save_customization(self, company_name: str, survey_title: str, customization: ClientCustomizationBase) -> Dict[str, Any]:
        """Save client customization using Data Vault model"""
        try:
            # Get or create hub client
            hub_client = self._get_or_create_hub_client(company_name)
            
            # Create satellite client
            sat_client = SatClient(
                hk_client=hub_client.hk_client,
                company_name=customization.company_name,
                logo_url=customization.logo_url,
                primary_color=customization.primary_color,
                secondary_color=customization.secondary_color
            )
            self.db.add(sat_client)
            
            self.db.commit()
            
            return {
                "status": "success",
                "message": "Customization saved successfully",
                "customization": {
                    "company_name": customization.company_name,
                    "logo_url": customization.logo_url,
                    "primary_color": customization.primary_color,
                    "secondary_color": customization.secondary_color
                }
            }
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error saving customization: {str(e)}")
    
    def save_questions(self, company_name: str, survey_title: str, questions: List[QuestionBase]) -> Dict[str, Any]:
        """Save questions using Data Vault model"""
        try:
            # Get or create hub project
            hub_project = self._get_or_create_hub_project(company_name, survey_title)
            
            saved_questions = []
            
            for i, question in enumerate(questions):
                # Create unique question ID
                question_id = f"{company_name}_{survey_title}_q_{i}"
                
                # Get or create hub question
                hub_question = self._get_or_create_hub_question(question_id)
                
                # Create satellite question
                sat_question = SatQuestion(
                    hk_question=hub_question.hk_question,
                    text=question.text,
                    q_type=question.q_type,
                    est_seconds=question.est_seconds,
                    options=question.options
                )
                self.db.add(sat_question)
                
                # Create link if it doesn't exist
                link = self.db.query(LinkProjectQuestion).filter(
                    and_(
                        LinkProjectQuestion.hk_project == hub_project.hk_project,
                        LinkProjectQuestion.hk_question == hub_question.hk_question
                    )
                ).first()
                
                if not link:
                    link = LinkProjectQuestion(
                        hk_project=hub_project.hk_project,
                        hk_question=hub_question.hk_question
                    )
                    self.db.add(link)
                
                saved_questions.append({
                    "id": question_id,
                    "text": question.text,
                    "q_type": question.q_type,
                    "est_seconds": question.est_seconds,
                    "options": question.options
                })
            
            self.db.commit()
            
            return {
                "status": "success",
                "message": f"Saved {len(questions)} questions",
                "questions": saved_questions
            }
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error saving questions: {str(e)}")
    
    def get_survey_data(self, company_name: str, survey_title: str) -> Dict[str, Any]:
        """Retrieve survey data using Data Vault model"""
        try:
            # Get hub project
            bk_project = f"{company_name}_{survey_title}"
            hub_project = self.db.query(HubProject).filter(
                HubProject.bk_project == bk_project
            ).first()
            
            if not hub_project:
                return {
                    "status": "error",
                    "message": "Survey not found"
                }
            
            # Get project details
            sat_project = self.db.query(SatProject).filter(
                SatProject.hk_project == hub_project.hk_project
            ).order_by(SatProject.load_dts.desc()).first()
            
            # Get objectives
            objectives = []
            objective_links = self.db.query(LinkProjectObjective).filter(
                LinkProjectObjective.hk_project == hub_project.hk_project
            ).all()
            
            for link in objective_links:
                sat_objective = self.db.query(SatObjective).filter(
                    SatObjective.hk_objective == link.hk_objective
                ).order_by(SatObjective.load_dts.desc()).first()
                
                if sat_objective:
                    objectives.append({
                        "id": link.hk_objective,
                        "label": sat_objective.label,
                        "display_order": sat_objective.display_order
                    })
            
            # Get questions
            questions = []
            question_links = self.db.query(LinkProjectQuestion).filter(
                LinkProjectQuestion.hk_project == hub_project.hk_project
            ).all()
            
            for link in question_links:
                sat_question = self.db.query(SatQuestion).filter(
                    SatQuestion.hk_question == link.hk_question
                ).order_by(SatQuestion.load_dts.desc()).first()
                
                if sat_question:
                    questions.append({
                        "id": link.hk_question,
                        "text": sat_question.text,
                        "q_type": sat_question.q_type,
                        "est_seconds": sat_question.est_seconds,
                        "options": sat_question.options
                    })
            
            # Get client customization
            hub_client = self.db.query(HubClient).filter(
                HubClient.bk_client == company_name
            ).first()
            
            customization = None
            if hub_client:
                sat_client = self.db.query(SatClient).filter(
                    SatClient.hk_client == hub_client.hk_client
                ).order_by(SatClient.load_dts.desc()).first()
                
                if sat_client:
                    customization = {
                        "company_name": sat_client.company_name,
                        "logo_url": sat_client.logo_url,
                        "primary_color": sat_client.primary_color,
                        "secondary_color": sat_client.secondary_color
                    }
            
            return {
                "status": "success",
                "data": {
                    "company_name": company_name,
                    "survey_title": survey_title,
                    "objectives": objectives,
                    "questions": questions,
                    "customization": customization
                }
            }
            
        except Exception as e:
            raise Exception(f"Error retrieving survey data: {str(e)}") 