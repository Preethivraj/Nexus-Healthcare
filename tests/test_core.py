import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from src.engine.triage_engine import DeterministicTriageEngine
from src.rag.local_retriever import LocalRuleRetriever
from src.llm.gemini_triage import GeminiTriageClient
from src.models.schemas import FollowUpAnswer

def test_all():
    print("Testing Engine...")
    engine = DeterministicTriageEngine()
    print(f"[PASS] Rules loaded: {len(engine.rules)}")
    assert len(engine.rules) == 24, "Expected 24 rules"

    print("Testing Local Retriever...")
    retriever = LocalRuleRetriever()
    results = retriever.query("chest pain breathlessness", top_k=2)
    print(f"[PASS] Top query match: {results[0]['rule']['id']} - {results[0]['rule']['title']}")

    print("Testing Deterministic Triage Evaluation (CP-01 High Risk)...")
    sample_answers = [
        FollowUpAnswer(question_id="q_cp_br", question_text="Are you having difficulty breathing right now?", answer="Yes"),
        FollowUpAnswer(question_id="q_cp_sudden", question_text="Did the chest pain begin suddenly?", answer="Yes")
    ]
    note = engine.evaluate(
        narrative="My chest has been hurting since this morning and I feel like I cannot breathe properly.",
        extracted_entities={"symptoms": ["Chest Discomfort", "Shortness of Breath"]},
        answers=sample_answers,
        vitals={"spo2": 95}
    )
    print(f"[PASS] Evaluated Acuity: {note.urgency_level} | Rule: {note.rule_id} | Escalation: {note.human_review_required}")
    assert note.rule_id == "CP-01", f"Expected CP-01, got {note.rule_id}"
    assert note.human_review_required is True, "Expected human review required for CP-01"

    print("Testing Routine Presentation (FE-04)...")
    routine_note = engine.evaluate(
        narrative="I have had a mild runny nose and low fever for two days.",
        extracted_entities={"symptoms": ["Fever"]},
        answers=[FollowUpAnswer(question_id="q_fe_neck", question_text="Stiff neck?", answer="No")]
    )
    print(f"[PASS] Routine Acuity: {routine_note.urgency_level} | Rule: {routine_note.rule_id}")
    assert routine_note.urgency_level in ["Standard", "Routine"], f"Expected Standard/Routine, got {routine_note.urgency_level}"

    print("Testing LLM Client / Fallback extraction...")
    client = GeminiTriageClient()
    q_data = client.extract_and_generate_questions("I tripped and hurt my ankle, it is swollen")
    print(f"[PASS] Category: {q_data['category']} | Questions generated: {len(q_data['questions'])}")
    assert q_data['category'] == "Injury", f"Expected Injury, got {q_data['category']}"

    print("ALL CORE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_all()
