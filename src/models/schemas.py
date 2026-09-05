from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PatientIntakeInput(BaseModel):
    narrative: str = Field(..., description="Everyday language description of the patient's symptoms")
    patient_name: Optional[str] = "Rajesh Patel"
    age: Optional[int] = 58
    gender: Optional[str] = "Male"
    mrn: Optional[str] = "#MRN-994-201-831"
    intake_channel: Optional[str] = "Emergency Walk-in"
    attending_clinician: Optional[str] = "Dr. Sarah Chennupati, MD"
    vitals_snapshot: Optional[Dict[str, Any]] = None


class FollowUpAnswer(BaseModel):
    question_id: str
    question_text: str
    answer: str  # "Yes", "No", "I'm not sure", or custom string
    impact: Optional[str] = "High"


class FollowUpRequest(BaseModel):
    session_id: str
    patient_narrative: str
    extracted_symptoms: List[str] = []
    answers: List[FollowUpAnswer] = []


class QuestionItem(BaseModel):
    id: str
    text: str
    options: List[str] = ["Yes", "No", "I'm not sure"]
    category: str
    target_rule_risk: str
    rationale: str


class ClarificationResponse(BaseModel):
    session_id: str
    extracted_symptoms: List[str]
    identified_category: str
    confidence_score: str
    protocol_name: str
    current_question_index: int
    total_questions: int
    questions: List[QuestionItem]
    is_ready_for_evaluation: bool


class EvidenceItem(BaseModel):
    label: str
    value: str
    status: Optional[str] = None  # e.g., "Critical Indicator", "Patient Reported", "Pending"


class TriageEvaluationRequest(BaseModel):
    session_id: str
    patient_narrative: str
    patient_name: Optional[str] = "Rajesh Patel"
    age: Optional[int] = 58
    gender: Optional[str] = "Male"
    mrn: Optional[str] = "#MRN-994-201-831"
    answers: List[FollowUpAnswer] = []
    vitals: Optional[Dict[str, Any]] = None


class TriageNote(BaseModel):
    case_id: str
    timestamp: str
    patient_name: str
    age: int
    gender: str
    mrn: str
    attending_physician: str
    intake_channel: str
    
    # Recommendation
    urgency_level: str  # "Immediate", "Urgent", "Routine"
    acuity_badge: str   # "Level 1 - Resuscitation", "Level 2 - Urgent", etc.
    target_department: str
    escalation_sla: str
    required_staffing: str
    human_review_required: bool
    routing_instructions: str
    
    # Verbatim and NLP
    chief_complaint: str
    original_description: str
    
    # Auditable Evidence Breakdown
    patient_reported: List[EvidenceItem]
    follow_up_established: List[EvidenceItem]
    still_unknown: List[EvidenceItem]
    
    # Deterministic Rule Citation
    rule_id: str
    rule_title: str
    rule_category: str
    deterministic_logic: str
    symptom_cluster: str
    decision_basis: str
    compliance_guarantee: str
    audit_trail: Dict[str, Any]


class TriageRule(BaseModel):
    id: str
    category: str
    title: str
    priority: str
    acuity_level: str
    action: str
    target_department: str
    escalation_sla: str
    required_staffing: str
    deterministic_logic: str
    criteria: Dict[str, Any]
    symptom_cluster: str
    description: str
    approved_by: str
    last_revision: str
    triggers_30d: int
