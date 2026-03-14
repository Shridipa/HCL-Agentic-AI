import json

import sys

import re

from groq import Groq
import os

def get_groq_client():
    from dotenv import load_dotenv
    load_dotenv()
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_sentiment_and_urgency(query):
    if isinstance(query, list): query = " ".join([str(x) for x in query])
    if isinstance(query, dict): query = query.get("text", str(query))
    if not isinstance(query, str): query = str(query)
    if not query or not query.strip():
        return {"sentiment": "neutral", "is_urgent": False, "urgency": "low", "signals": []}

    system_prompt = (
        "Analyze the sentiment and urgency of the user query for enterprise support. "
        "Return ONLY a JSON object with: "
        "'sentiment' (positive/negative/neutral), "
        "'is_urgent' (boolean), "
        "'urgency' (high/medium/low), "
        "'signals' (array of urgent keywords found)."
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
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Groq Sentiment Error: {e}")
        return {"sentiment": "neutral", "is_urgent": False, "urgency": "low", "signals": []}

if __name__ == "__main__":

    test_query = sys.argv[1] if len(sys.argv) > 1 else "My laptop is broken and I have a meeting in 5 minutes! HELP!!!"

    try:

        results = analyze_sentiment_and_urgency(test_query)

        print(json.dumps(results, indent=2))

    except Exception as e:

        print(f"Error: {e}")

