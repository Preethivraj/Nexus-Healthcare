TRACK_ID=PS01
# Healthcare: Clinical Patient Intake Triage Assistant

An auditable, clinical-grade patient intake triage assistant engineered for emergency department and ambulatory walk-in intake. The system takes everyday, incomplete descriptions of patient discomfort, executes adaptive clarifying follow-up questions, deterministically checks the presentation against auditable clinical triage protocols across 5 core complaint tracks, and produces a tamper-evident triage note with explicit rule citations, clear human escalation, and zero autonomous diagnosis.

---

## 📋 What the System Does

1. **Natural Language Intake ("Understand")**:
   - Ingests free-text, unstructured, and colloquial patient narratives (e.g. *"My chest has been hurting since this morning and I feel like I can't breathe properly"*).
   - Extracts chief symptoms, duration, and clinical presentation track.
2. **Adaptive Clarification ("Clarify")**:
   - Generates structured, high-priority follow-up questions targeting red-flag indicators (e.g., anginal radiation, dyspnea, diaphoresis, limb deformities, peritoneal signs).
   - Provides single-click choice prompts (*Yes / No / I'm not sure*).
3. **Evidence Synthesis ("Synthesis & Review")**:
   - Explicitly segregates:
     - **Patient Reported**: What the patient described in their own words.
     - **Follow-up Established**: Verified parameters from interactive prompts.
     - **Still Unknown**: Information unverified or pending bedside diagnostic tests (e.g. 12-lead ECG, vitals).
4. **Deterministic Rule Engine & Governance ("Evaluate & Triage Note")**:
   - Evaluates evidence against 24 auditable, board-approved clinical triage rules.
   - Assigns standard acuity tiers: **Immediate** (Level 1 - Resuscitation), **Urgent** (Level 2/3), or **Routine** (Level 4/5).
   - Recommends the specific target department (e.g. *Emergency Triage Unit*, *Trauma Resuscitation Bay*, *General Medicine*).
5. **Strict Clinical Guardrails & Human Escalation**:
   - **Zero Black-Box / Never Diagnoses**: Adheres strictly to triage categorization; no disease diagnoses or drug prescriptions.
   - **Rule Traceability**: Every acuity score cites the exact Rule ID (e.g. `CP-01`, `BR-02`) and its algorithmic logic.
   - **Safe Escalation**: Automatically alerts and transfers uncertain, ambiguous, or high-risk presentations to an attending emergency physician (`Dr. Sarah Chennupati, MD`).

---

## 📂 Data & Documents Generated

- **`data/rules.json`**: 24 auditable clinical governance rules across all 5 mandatory walk-in complaint tracks:
  - **Chest Pain**: Rules `CP-01` to `CP-05` (Cardiopulmonary distress, atypical discomfort, radiating anginal pattern, diaphoresis/syncope, pleuritic pain).
  - **Breathing Difficulty**: Rules `BR-01` to `BR-05` (Upper airway stridor/cyanosis, hypoxemia SpO2 < 92%, acute bronchospasm/COPD, word dyspnea, mild exertional).
  - **Fever**: Rules `FE-01` to `FE-04` (CNS meningism, septic shock red flags, pediatric hyperpyrexia, uncomplicated viral).
  - **Injury**: Rules `IN-01` to `IN-06` (High-velocity polytrauma, active arterial hemorrhage, limb deformity/fracture, head trauma with LOC, minor lacerations, ankle sprains).
  - **Abdominal Pain**: Rules `AB-01` to `AB-04` (Tearing aortic catastrophe, peritonism/board-like rigidity, acute appendicitis RLQ, functional cramping).
- **`data/sample_cases.json`**: Pre-seeded active patient queue (14 cases) and historical intake records with Indian patient profiles (e.g., *Sunita Patel, Aarav Mehta, Priya Sharma, Vikram Malhotra, Kavita Krishnan*).
- **`data/embeddings_cache.json`**: Pre-computed local semantic vectors for instant startup (< 1 sec) with zero external network dependency.

---


## 🏗️ Architecture & Sound Engineering

```
Healthcare/
├── app.py                      # Starts FastAPI & static frontend on port 8000
├── requirements.txt            # Python 3.11 dependencies
├── README.md                   # TRACK_ID=PS01 documentation & demo link
├── src/
│   ├── api/routes.py           # REST endpoints for intake, clarification, rules, escalation
│   ├── engine/triage_engine.py # Deterministic clinical rule evaluator & audit builder
│   ├── llm/gemini_triage.py    # Gemini API client with fallback question banks
│   ├── models/schemas.py       # Pydantic schemas for data validation
│   └── rag/local_retriever.py  # Local vector search & embedding indexer
├── data/
│   ├── rules.json              # 24 auditable triage rules
│   ├── sample_cases.json       # Live queue and clinician telemetry
│   └── embeddings_cache.json   # Pre-computed local vectors
└── frontend/
    ├── dist/                   # Production-built, zero-config static bundle served by app.py
    └── src/                    # React + Tailwind + Lucide UI source components
```
