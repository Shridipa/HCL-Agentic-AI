import json

import sys

import re

from groq import Groq
import os

def get_groq_client():
    from dotenv import load_dotenv
    import pathlib
    load_dotenv(dotenv_path=pathlib.Path(__file__).parent.parent / ".env", override=True)
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_entities(query):
    if isinstance(query, list): query = " ".join([str(x) for x in query])
    if isinstance(query, dict): query = query.get("text", str(query))
    if not isinstance(query, str): query = str(query)
    
    system_prompt = (
        "You are an enterprise Named Entity Extractor for HCLTech. "
        "Extract entities from the user query. Return ONLY a JSON object with these keys: "
        "employee_id, department, policy_title, metric, date, application_name, ticket_type, description, priority, topic, participants, time, location, participant_emails. "
        "Use '...' for missing values. For participant_emails, use an array []."
    )
    
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}"},
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        entities = json.loads(response.choices[0].message.content)
        return entities
    except Exception as e:
        print(f"Groq NER Error: {e}")
        # Return empty template on failure
        return {
            "employee_id": "...", "department": "...", "policy_title": "...", "metric": "...",
            "date": "...", "application_name": "...", "ticket_type": "...", "description": "...",
            "priority": "Medium", "topic": "...", "participants": "...", "time": "...",
            "location": "Virtual", "participant_emails": []
        }

if __name__ == "__main__":

    test_query = sys.argv[1] if len(sys.argv) > 1 else "Employee EMP123 from Finance needs to reset password for SAP by tomorrow with high priority"

    try:

        results = extract_entities(test_query)

        print(json.dumps(results, indent=2))

    except Exception as e:

        print(f"Error: {e}")

