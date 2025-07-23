"""
Opportunity API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.core.response import create_success_response, create_list_response
from app.core.exceptions import (
    ValidationException, NotFoundException, OperationNotAllowedException
)
from app.services.opportunity_service_adapter import OpportunityServiceAdapter
from app.schemas.opportunity import (
    OpportunityCreateRequest, OpportunityResponse, OpportunityDetailsResponse,
    OpportunityListResponse, OpportunitySubmitRequest, OpportunityCancelRequest,
    OpportunityReactivateRequest, ProblemStatementCreateRequest, ProblemStatementResponse,
    SkillRequirementCreateRequest, SkillRequirementResponse,
    TimelineRequirementCreateRequest, TimelineRequirementResponse
)

router = APIRouter()


@router.post("", response_model=dict, status_code=201)
async def create_opportunity(
    request: Request,
    opportunity_data: OpportunityCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new opportunity."""
    service = OpportunityServiceAdapter(db)
    
    opportunity = service.create_opportunity(
        title=opportunity_data.title,
        customer_id=opportunity_data.customer_id,
        customer_name=opportunity_data.customer_name,
        sales_manager_id=opportunity_data.sales_manager_id,
        description=opportunity_data.description,
        priority=opportunity_data.priority.value,
        annual_recurring_revenue=opportunity_data.annual_recurring_revenue,
        geographic_requirements=opportunity_data.geographic_requirements.dict()
    )
    
    response_data = OpportunityResponse.from_orm(opportunity)
    return create_success_response(request, response_data.dict(), "Opportunity created successfully")


@router.get("/{opportunity_id}", response_model=dict)
async def get_opportunity_details(
    request: Request,
    opportunity_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get comprehensive details about an opportunity."""
    service = OpportunityServiceAdapter(db)
    
    details = service.get_opportunity_details(opportunity_id)
    
    # Convert to response format
    response_data = {
        "opportunity": OpportunityResponse.from_orm(details["opportunity"]).dict(),
        "problem_statement": ProblemStatementResponse.from_orm(details["problem_statement"]).dict() if details["problem_statement"] else None,
        "skill_requirements": [SkillRequirementResponse.from_orm(sr).dict() for sr in details["skill_requirements"]],
        "timeline": TimelineRequirementResponse.from_orm(details["timeline"]).dict() if details["timeline"] else None,
        "status_history": [
            {
                "id": str(sh.id),
                "opportunity_id": str(sh.opportunity_id),
                "status": sh.status,
                "changed_by": str(sh.changed_by),
                "reason": sh.reason,
                "changed_at": sh.changed_at.isoformat()
            } for sh in details["status_history"]
        ],
        "change_history": [
            {
                "id": str(ch.id),
                "opportunity_id": str(ch.opportunity_id),
                "changed_by": str(ch.changed_by),
                "field_changed": ch.field_changed,
                "reason": ch.reason,
                "old_value": ch.old_value,
                "new_value": ch.new_value,
                "changed_at": ch.changed_at.isoformat()
            } for ch in details["change_history"]
        ],
        "attachments": [
            {
                "id": str(att.id),
                "problem_statement_id": str(att.problem_statement_id),
                "file_name": att.file_name,
                "file_type": att.file_type,
                "file_size": att.file_size,
                "file_url": att.file_url,
                "uploaded_by": str(att.uploaded_by),
                "uploaded_at": att.uploaded_at.isoformat(),
                "is_removed": att.is_removed
            } for att in details["attachments"]
        ]
    }
    
    return create_success_response(request, response_data, "Opportunity details retrieved successfully")


@router.get("", response_model=dict)
async def search_opportunities(
    request: Request,
    query: Optional[str] = Query(None, description="Search query for title or description"),
    status: Optional[str] = Query(None, description="Filter by opportunity status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    sales_manager_id: Optional[uuid.UUID] = Query(None, description="Filter by sales manager ID"),
    customer_id: Optional[uuid.UUID] = Query(None, description="Filter by customer ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """Search for opportunities with various filters."""
    service = OpportunityServiceAdapter(db)
    
    opportunities, total_count = service.search_opportunities(
        query=query,
        status=status,
        priority=priority,
        sales_manager_id=sales_manager_id,
        customer_id=customer_id,
        page=page,
        page_size=page_size
    )
    
    response_data = [OpportunityResponse.from_orm(opp).dict() for opp in opportunities]
    
    return create_list_response(request, response_data, total_count, page, page_size)


@router.post("/{opportunity_id}/submit", response_model=dict)
async def submit_opportunity(
    request: Request,
    opportunity_id: uuid.UUID,
    submit_data: OpportunitySubmitRequest,
    db: Session = Depends(get_db)
):
    """Submit an opportunity for matching."""
    service = OpportunityServiceAdapter(db)
    
    opportunity = service.submit_opportunity(opportunity_id, submit_data.user_id)
    
    response_data = OpportunityResponse.from_orm(opportunity)
    return create_success_response(request, response_data.dict(), "Opportunity submitted successfully")


@router.post("/{opportunity_id}/cancel", response_model=dict)
async def cancel_opportunity(
    request: Request,
    opportunity_id: uuid.UUID,
    cancel_data: OpportunityCancelRequest,
    db: Session = Depends(get_db)
):
    """Cancel an opportunity."""
    service = OpportunityServiceAdapter(db)
    
    opportunity = service.cancel_opportunity(opportunity_id, cancel_data.user_id, cancel_data.reason)
    
    response_data = OpportunityResponse.from_orm(opportunity)
    return create_success_response(request, response_data.dict(), "Opportunity cancelled successfully")


@router.post("/{opportunity_id}/reactivate", response_model=dict)
async def reactivate_opportunity(
    request: Request,
    opportunity_id: uuid.UUID,
    reactivate_data: OpportunityReactivateRequest,
    db: Session = Depends(get_db)
):
    """Reactivate a cancelled opportunity."""
    service = OpportunityServiceAdapter(db)
    
    opportunity = service.reactivate_opportunity(opportunity_id, reactivate_data.user_id)
    
    response_data = OpportunityResponse.from_orm(opportunity)
    return create_success_response(request, response_data.dict(), "Opportunity reactivated successfully")


@router.post("/{opportunity_id}/problem-statement", response_model=dict, status_code=201)
async def add_problem_statement(
    request: Request,
    opportunity_id: uuid.UUID,
    problem_data: ProblemStatementCreateRequest,
    db: Session = Depends(get_db)
):
    """Add a problem statement to an opportunity."""
    service = OpportunityServiceAdapter(db)
    
    problem_statement = service.add_problem_statement(opportunity_id, problem_data.content)
    
    response_data = ProblemStatementResponse.from_orm(problem_statement)
    return create_success_response(request, response_data.dict(), "Problem statement added successfully")


@router.post("/{opportunity_id}/skill-requirements", response_model=dict, status_code=201)
async def add_skill_requirement(
    request: Request,
    opportunity_id: uuid.UUID,
    skill_data: SkillRequirementCreateRequest,
    db: Session = Depends(get_db)
):
    """Add a skill requirement to an opportunity."""
    service = OpportunityServiceAdapter(db)
    
    skill_requirement = service.add_skill_requirement(
        opportunity_id=opportunity_id,
        skill_id=skill_data.skill_id,
        skill_name=skill_data.skill_name,
        skill_type=skill_data.skill_type.value,
        importance_level=skill_data.importance_level.value,
        minimum_proficiency_level=skill_data.minimum_proficiency_level.value
    )
    
    response_data = SkillRequirementResponse.from_orm(skill_requirement)
    return create_success_response(request, response_data.dict(), "Skill requirement added successfully")


@router.post("/{opportunity_id}/timeline-requirement", response_model=dict, status_code=201)
async def add_timeline_requirement(
    request: Request,
    opportunity_id: uuid.UUID,
    timeline_data: TimelineRequirementCreateRequest,
    db: Session = Depends(get_db)
):
    """Add a timeline requirement to an opportunity."""
    service = OpportunityServiceAdapter(db)
    
    timeline_requirement = service.add_timeline_requirement(
        opportunity_id=opportunity_id,
        start_date=timeline_data.start_date,
        end_date=timeline_data.end_date,
        is_flexible=timeline_data.is_flexible,
        specific_days=timeline_data.specific_days
    )
    
    response_data = TimelineRequirementResponse.from_orm(timeline_requirement)
    return create_success_response(request, response_data.dict(), "Timeline requirement added successfully")
