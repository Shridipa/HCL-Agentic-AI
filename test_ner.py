import json
from ner_extractor import extract_entities

queries = [
    "schedule the 'the recent tech changes in the company' for 15th March, 2026 with Sarah",
    "book a meeting about Q1 Strategy Planning for tomorrow at 3pm, Sarah will be there",
    "invite Sarah to discuss the new project on Friday",
    "Sarah is attending the sync for tech changes on 15th March"
]

for q in queries:
    print(f"\nQuery: {q}")
    entities = extract_entities(q)
    print(json.dumps(entities, indent=2))
