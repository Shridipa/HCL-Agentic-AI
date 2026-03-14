import json

import sys

import re

_ner_classifier = None

def get_ner_classifier():
    global _ner_classifier
    if _ner_classifier is None:
        from transformers import pipeline
        _ner_classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")
    return _ner_classifier

def extract_entities(query):
    if isinstance(query, list): query = " ".join([str(x) for x in query])
    if isinstance(query, dict): query = query.get("text", str(query))
    if not isinstance(query, str): query = str(query)
    if not query or not query.strip():

        return {

            "employee_id": "...",

            "department": "...",

            "policy_title": "...",

            "metric": "...",

            "date": "...",

            "application_name": "...",

            "ticket_type": "...",

            "description": "...", 

            "priority": "Medium",

            "topic": "...",

            "participants": "..."

        }

    entities = {

        "employee_id": "...",

        "department": "...",

        "policy_title": "...",

        "metric": "...",

        "date": "...",

        "application_name": "...",

        "ticket_type": "...",

        "description": "...", 

        "priority": "Low|Medium|High",

        "topic": "...",

        "participants": "...",
        "time": "...",
        "location": "Virtual",
        "participant_emails": []   # extracted email addresses from the query

    }

    # ── Email Address Extraction ──────────────────────────────────────────
    # Extracts participant email addresses typed inline in the query
    # e.g. "schedule a meeting with alice@hcl.com and bob@company.com"
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    found_emails = re.findall(email_pattern, query)
    if found_emails:
        entities["participant_emails"] = [e.lower().strip() for e in found_emails]

    # ── Location Extraction ───────────────────────────────────────────────
    location_patterns = [
        r'(?:at|in|location[:\s]+)\s+([A-Z][a-zA-Z\s]+(?:Room|Hall|Office|Center|Centre|Lab|Conference)?)',
        r'(?:conference\s+room|meeting\s+room)\s+([\w\s-]+)'
    ]
    for pattern in location_patterns:
        loc_match = re.search(pattern, query, re.IGNORECASE)
        if loc_match:
            candidate = loc_match.group(1).strip()
            # Avoid matching generic words
            if len(candidate) > 2 and candidate.lower() not in ("the", "a", "an", "this", "that"):
                entities["location"] = candidate
                break

    # ── Time Extraction ───────────────────────────────────────────────────
    time_patterns = [
        r'\b\d{1,2}:\d{2}\s*(?:AM|PM)\b',
        r'\bat\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM)?)\b',
        r'\baround\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM)?)\b'
    ]
    for pattern in time_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            entities["time"] = match.group(0).upper().replace("AT ", "").replace("AROUND ", "").strip()
            break

    # ── Participants Name Extraction ──────────────────────────────────────
    # Extract names (non-email parts) from various patterns
    query_no_emails = re.sub(email_pattern, '', query)
    
    # 1. Names preceded by common invitation keywords
    invitation_patterns = [
        r'(?:with|between|invite|add|including)\s+([^,\.]+)',
        r'(?:meeting\s+with)\s+([^,\.]+)',
        r'([^,\.]+?)\s+(?:will\s+be\s+there|will\s+be\s+joining|is\s+attending)'
    ]
    
    found_participants = []
    for pattern in invitation_patterns:
        matches = re.finditer(pattern, query_no_emails, re.IGNORECASE)
        for match in matches:
            p_text = match.group(1).lower().replace(" and ", ", ").replace(" & ", ", ")
            # Split by comma-like separators
            names = [p.strip().title() for p in re.split(r'[,;]|\s+and\s+', p_text) if p.strip() and len(p.strip()) > 1]
            for name in names:
                # Filter out "name" / "names" prefix
                clean_name = re.sub(r'^(?:name|names|participant|participants|colleague|colleagues|employee|employees)\s+', '', name, flags=re.IGNORECASE)
                # Basic person name check (very simple proxy)
                if clean_name.lower() not in ("me", "i", "everyone", "anyone", "all", "us", "him", "her", "them", "someone"):
                    found_participants.append(clean_name)
    
    if found_participants:
        # Use a list of unique names while preserving order
        seen = set()
        entities["participants"] = [x for x in found_participants if not (x in seen or seen.add(x))]

    emp_id_match = re.search(r'\b(EMP|HCL)\d+\b', query, re.IGNORECASE)

    if emp_id_match:

        entities["employee_id"] = emp_id_match.group(0).upper()

    if re.search(r'\bhigh\b', query, re.IGNORECASE):

        entities["priority"] = "High"

    elif re.search(r'\bmedium\b', query, re.IGNORECASE):

        entities["priority"] = "Medium"

    elif re.search(r'\blow\b', query, re.IGNORECASE):

        entities["priority"] = "Low"

    else:

        entities["priority"] = "Medium"

    slots_to_fill = {

        "department": ["Finance", "HR", "Engineering", "IT", "Sales", "Marketing", "Legal"],

        "ticket_type": ["Software Issue", "Hardware Issue", "Network Issue", "Access Request"],

        "application_name": ["SAP", "Outlook", "Teams", "Jira", "Workday", "Azure", "AWS", "Salesforce", "ServiceNow", "Slack"],

        "metric": ["Revenue", "Growth", "Headcount", "Turnover", "Profit", "EBITDA", "Margin", "Dividend", "ESG", "Sustainability", "Carbon", "Retention"]

    }

    

                                                                          

    likely_slots = []

    if any(k in query.lower() for k in ["issue", "broken", "failed", "repair", "ticket", "not working"]):

        likely_slots.extend(["department", "ticket_type"])

    if any(k in query.lower() for k in ["access", "password", "login", "permission", "account"]):

        likely_slots.extend(["application_name"])

    if any(k in query.lower() for k in ["how many", "what is", "revenue", "profit", "report", "growth", "metric"]):

        likely_slots.extend(["metric"])

        

                                                                 

    slots_to_check = list(set(likely_slots)) if likely_slots else list(slots_to_fill.keys())

    for slot in slots_to_check:
        labels = slots_to_fill[slot]
        result = get_ner_classifier()(query, labels, multi_label=False)

        if result['scores'][0] > 0.65:

            entities[slot] = result['labels'][0]

    date_patterns = [

        (r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', 'DD.MM.YYYY'),

        (r'\b\d{1,2}/\d{1,2}/\d{4}\b', 'DD/MM/YYYY'),

        (r'\b\d{4}-\d{2}-\d{2}\b', 'YYYY-MM-DD'),

        (r'\b\d{1,2}-\d{1,2}-\d{4}\b', 'DD-MM-YYYY'),

        (r'\btomorrow\b', 'relative'),

        (r'\btoday\b', 'relative'),
        
        # Handles "7th March, 2026", "March 7th, 2026", "7 March", etc.
        (r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)(?:\s*,?\s*\d{4})?\b', 'Natural Date 1'),
        (r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(?:st|nd|rd|th)?(?:\s*,?\s*\d{4})?\b', 'Natural Date 2'),

        (r'\bnext week\b', 'relative'),

        (r'\bnext month\b', 'relative'),

    ]

    for pattern, format_type in date_patterns:

        match = re.search(pattern, query, re.IGNORECASE)

        if match:

            entities["date"] = match.group(0)

            break

    meeting_keywords = ['meeting', 'book', 'schedule', 'arrange']

    if any(keyword in query.lower() for keyword in meeting_keywords):

        topic_patterns = [
            r'(?:discussion|meeting|briefing|session|call|sync)\s+(?:about|on|for|regarding|to discuss)\s+([^,\.\?]+)',
            r'(?:subject|topic|title|purpose)[:\s]+([^,\.\?]+)',
            r'(?:for)\s+([^,\.\?]+?)\s+(?:on|at|scheduled|booked)'
        ]
        
        for pattern in topic_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                candidate = match.group(1).strip()
                if len(candidate.split()) <= 10: # Avoid capturing entire sentences
                    entities["topic"] = candidate
                    break
        
        # Fallback for "schedule/scheduled the 'X'"
        if entities["topic"] == "...":
            # Match quoted text after 'schedule' or 'scheduled'
            quoted_match = re.search(r"(?:schedule|scheduled)\s+(?:the\s+)?['\"]([^'\"]+)['\"]", query, re.IGNORECASE)
            if quoted_match:
                entities["topic"] = quoted_match.group(1)
            elif "schedule the " in query.lower() or "scheduled the " in query.lower():
                # Extract words after "schedule/scheduled the " until a date/time or end of sentence
                marker = "scheduled the " if "scheduled the " in query.lower() else "schedule the "
                after_sched = query.lower().split(marker)[1]
                # stop at "for", "on", "at", "."
                stop_words = ["for", "on", "at", ".", ",", "with"]
                topic_words = []
                for word in after_sched.split():
                    # Check if the word starts with a stop word or is a stop word
                    if any(s == word.rstrip('.,') for s in stop_words): break
                    topic_words.append(word)
                if topic_words:
                    entities["topic"] = " ".join(topic_words).title()

        if entities["topic"] == "..." and "meeting" in query.lower():
            words = query.strip().split()
            if len(words) > 3:
                entities["topic"] = " ".join(words[:5])
            else:
                entities["topic"] = "Business Discussion"

    it_keywords = ['broken', 'issue', 'laptop', 'access', 'failed', 'problem', 'reset', 'password', 'slow', 'flickering', 'ticket', 'hardware', 'monitor', 'screen', 'keyboard', 'mouse', 'functioning', 'working', 'help', 'repair', 'fix']

    is_action_like = any(k in query.lower() for k in it_keywords)
    

    if is_action_like and len(query.strip().split()) >= 3:

        entities["description"] = query

    elif "ticket" in query.lower() or "help" in query.lower():

        entities["description"] = "..."

    return entities

if __name__ == "__main__":

    test_query = sys.argv[1] if len(sys.argv) > 1 else "Employee EMP123 from Finance needs to reset password for SAP by tomorrow with high priority"

    try:

        results = extract_entities(test_query)

        print(json.dumps(results, indent=2))

    except Exception as e:

        print(f"Error: {e}")

