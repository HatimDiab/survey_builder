from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# Base schemas for Data Vault entities
class ObjectiveBase(BaseModel):
    label: str = Field(..., description="Objective label")
    display_order: int = Field(..., description="Display order for sorting")

class QuestionBase(BaseModel):
    text: str = Field(..., description="Question text")
    q_type: str = Field(..., description="Question type (multiple_choice, text, etc.)")
    est_seconds: int = Field(..., description="Estimated time in seconds")
    options: Optional[str] = Field(None, description="JSON string for multiple choice options")

class ClientCustomizationBase(BaseModel):
    company_name: str = Field(..., description="Company name")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    primary_color: Optional[str] = Field(None, description="Primary brand color")
    secondary_color: Optional[str] = Field(None, description="Secondary brand color")

# Request schemas
class SaveObjectivesRequest(BaseModel):
    company_name: str = Field(..., description="Company name")
    survey_title: str = Field(..., description="Survey title")
    objectives: List[ObjectiveBase] = Field(..., description="List of objectives")

class SaveCustomizationRequest(BaseModel):
    company_name: str = Field(..., description="Company name")
    survey_title: str = Field(..., description="Survey title")
    customization: ClientCustomizationBase = Field(..., description="Client customization data")

class SaveQuestionsRequest(BaseModel):
    company_name: str = Field(..., description="Company name")
    survey_title: str = Field(..., description="Survey title")
    questions: List[QuestionBase] = Field(..., description="List of questions")

class ExportSurveyRequest(BaseModel):
    company_name: str = Field(..., description="Company name")
    survey_title: str = Field(..., description="Survey title")
    format: str = Field(default="json", description="Export format")

# Response schemas
class ObjectiveResponse(ObjectiveBase):
    id: str = Field(..., description="Objective ID")

class QuestionResponse(QuestionBase):
    id: str = Field(..., description="Question ID")

class ClientCustomizationResponse(ClientCustomizationBase):
    pass

class SurveyDataResponse(BaseModel):
    company_name: str
    survey_title: str
    objectives: List[ObjectiveResponse]
    questions: List[QuestionResponse]
    customization: Optional[ClientCustomizationResponse]

class SaveResponse(BaseModel):
    status: str = Field(..., description="Success or error status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")

class ExportResponse(BaseModel):
    status: str = Field(..., description="Success or error status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Exported survey data") 