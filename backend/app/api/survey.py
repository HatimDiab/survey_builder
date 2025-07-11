from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..db.connection import get_db
from ..crud.survey import SurveyCRUD
from ..schemas.survey import (
    SaveObjectivesRequest, SaveCustomizationRequest, SaveQuestionsRequest,
    ExportSurveyRequest, SaveResponse, ExportResponse, SurveyDataResponse
)

router = APIRouter(prefix="/api", tags=["survey"])

@router.post("/save-objectives", response_model=SaveResponse)
async def save_objectives(
    request: SaveObjectivesRequest,
    db: Session = Depends(get_db)
):
    """Save objectives for a survey"""
    try:
        crud = SurveyCRUD(db)
        result = crud.save_objectives(
            company_name=request.company_name,
            survey_title=request.survey_title,
            objectives=request.objectives
        )
        return SaveResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-customization", response_model=SaveResponse)
async def save_customization(
    request: SaveCustomizationRequest,
    db: Session = Depends(get_db)
):
    """Save client customization data"""
    try:
        crud = SurveyCRUD(db)
        result = crud.save_customization(
            company_name=request.company_name,
            survey_title=request.survey_title,
            customization=request.customization
        )
        return SaveResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-questions", response_model=SaveResponse)
async def save_questions(
    request: SaveQuestionsRequest,
    db: Session = Depends(get_db)
):
    """Save questions for a survey"""
    try:
        crud = SurveyCRUD(db)
        result = crud.save_questions(
            company_name=request.company_name,
            survey_title=request.survey_title,
            questions=request.questions
        )
        return SaveResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/survey-data/{company_name}/{survey_title}", response_model=SurveyDataResponse)
async def get_survey_data(
    company_name: str,
    survey_title: str,
    db: Session = Depends(get_db)
):
    """Get survey data including objectives, questions, and customization"""
    try:
        crud = SurveyCRUD(db)
        result = crud.get_survey_data(company_name, survey_title)
        
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["message"])
        
        return SurveyDataResponse(**result["data"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export", response_model=ExportResponse)
async def export_survey(
    request: ExportSurveyRequest,
    db: Session = Depends(get_db)
):
    """Export survey data in specified format"""
    try:
        crud = SurveyCRUD(db)
        survey_data = crud.get_survey_data(request.company_name, request.survey_title)
        
        if survey_data["status"] == "error":
            raise HTTPException(status_code=404, detail=survey_data["message"])
        
        # Format the export data based on requested format
        export_data = {
            "format": request.format,
            "survey": survey_data["data"]
        }
        
        if request.format == "json":
            return ExportResponse(
                status="success",
                message="Survey exported successfully",
                data=export_data
            )
        else:
            # For other formats, you could add conversion logic here
            return ExportResponse(
                status="success",
                message=f"Survey exported in {request.format} format",
                data=export_data
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 