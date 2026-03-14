import json

import sys

import os

from groq import Groq

def get_groq_client():
    from dotenv import load_dotenv
    load_dotenv()
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def detect_intent(query, context="", previous_intent=None):
    if isinstance(query, list): query = " ".join([str(x) for x in query])
    if isinstance(query, dict): query = query.get("text", str(query))
    if not isinstance(query, str): query = str(query)
    
    if not query or not query.strip():
        return {"intent": "other", "confidence": 0.0, "rationale": "Empty query."}

    system_prompt = (
        "You are an enterprise intent classifier for HCLTech AI. "
        "Classify the user query into ONE of these categories: "
        "ask_finance, ask_hr, ask_it_policy, ask_dev, ask_compliance, ask_procurement, ask_security, action_ticket, action_access, action_schedule, ask_people, other. "
        "Return ONLY a JSON object with 'intent', 'confidence' (0.0-1.0), and 'rationale'."
    )
    
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}\nPrevious Intent: {previous_intent}"},
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Groq Intent Detection Error: {e}")
        # Fallback to simple keyword logic if Groq fails
        query_lower = query.lower()
        if "revenue" in query_lower or "profit" in query_lower:
            return {"intent": "ask_finance", "confidence": 0.8, "rationale": "Keyword fallback."}
        return {"intent": "other", "confidence": 0.5, "rationale": f"Fallback due to error: {e}"}
    if isinstance(query, list): query = " ".join([str(x) for x in query])
    if isinstance(query, dict): query = query.get("text", str(query))
    if not isinstance(query, str): query = str(query)
    
    if not query or not query.strip():
        return {"intent": "other", "confidence": 0.0, "rationale": "Empty query."}

    # Expanded Enterprise Intents
    intent_map = {
        "company performance, revenue, financial numbers, annual report statistics": "ask_finance",
        "HR policy, employee benefits, headcount, leave, recruitment": "ask_hr",
        "IT guidelines, security policy, company rules, standards": "ask_it_policy",
        "technical software, code, development, engineering": "ask_dev",
        "compliance, legal, regulatory, gdpr, ethics, code of conduct": "ask_compliance",
        "procurement, vendors, suppliers, purchasing, buying": "ask_procurement",
        "security, cyber, firewall, access control, phishing": "ask_security",
        "technical issue, repair, hardware fix, create IT ticket": "action_ticket",
        "request access, permissions, reset password, login": "action_access",
        "schedule meeting, book calendar, arrange call": "action_schedule",
        "company leaders, board directors, CEO, executives, nadar, vijaykumar": "ask_people",
        "general greeting, conversation, hello, thanks": "other"
    }

    # multi-turn refinement: Check for short follow-up dictating stickiness
    is_follow_up = len(query.split()) < 5 and previous_intent and previous_intent != "other"
    
    candidate_labels = list(intent_map.keys())
    results = get_classifier()(query, candidate_labels)
    
    best_label = results['labels'][0]
    top_intent = intent_map[best_label]
    confidence = results['scores'][0]
    rationale = f"Classified as '{top_intent}' ({confidence:.2f}) via Zero-Shot."

    # Keyword Priorities & Boosting
    keyword_priorities = {
        "ask_finance": ["revenue", "profit", "ebitda", "cagr", "dividend", "fiscal", "annual report", "finances", "expenditure"],
        "ask_people": ["ceo", "chairman", "chairperson", "vijaykumar", "roshni", "nadar", "director", "executives", "founder", "board of directors"],
        "ask_hr": ["leave", "policy", "employees", "headcount", "recruitment", "payroll"],
        "action_schedule": ["schedule", "meeting", "book a", "arrange"],
        "action_ticket": ["broken", "not working", "create a ticket", "raise a ticket"],
        "ask_compliance": ["compliance", "gdpr", "legal", "ethics", "regulatory"],
        "ask_security": ["security", "firewall", "phishing", "cyber"],
        "ask_procurement": ["vendor", "supplier", "procurement", "purchase order"]
    }

    query_lower = query.lower()
    
    # Check for keyword matches to boost confidence
    for intent_key, keywords in keyword_priorities.items():
        if any(k in query_lower for k in keywords):
            if top_intent != intent_key and confidence < 0.85:
                top_intent = intent_key
                confidence = max(confidence, 0.85)
                rationale = f"Boosted to '{top_intent}' due to keyword match."
                break

    # Stickiness Logic: if ambiguous and distinct previous intent, stick to it
    if is_follow_up and confidence < 0.6:
        top_intent = previous_intent
        confidence = 0.75
        rationale = f"Contextual Stickiness: Follow-up assumed to be about '{previous_intent}'."

    return {
        "intent": top_intent,
        "confidence": confidence,
        "rationale": rationale
    }

if __name__ == "__main__":

    test_query = sys.argv[1] if len(sys.argv) > 1 else "What was HCLTech's revenue growth?"

    try:

        result = detect_intent(test_query)

        print(json.dumps(result, indent=2))

    except Exception as e:

        print(f"Error: {e}")

