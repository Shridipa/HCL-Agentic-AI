import sys
import json

def generate_clarification(missing_entities):
    """Generates a clarification prompt for missing entities."""
    if not missing_entities:
        return "No missing entities identified."

    missing_str = ", ".join(missing_entities)
    primary_missing = missing_entities[0]
    
    return (
        f"I need one detail to proceed:\n"
        f"- Missing: {missing_str}\n\n"
        f"Question: Please provide {primary_missing} to continue."
    )

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            missing = json.loads(sys.argv[1])
        else:
            missing = ["employee_id", "department"]
        print(generate_clarification(missing))
    except Exception as e:
        print(f"Error: {e}")
