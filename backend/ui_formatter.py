import json
import sys
import re

def format_ui_response(response_type, content):
    if response_type == "answer":
        parts = content.split("--- DETAILED DATA REFERENCES ---")
        main_text = parts[0].strip()
        
        # Extract sources from the end if they exist
        sources = ""
        if "[" in main_text and "Sources:" in main_text:
            s_parts = main_text.split("[Annual Report 2024–25 Sources:")
            if len(s_parts) > 1:
                main_text = s_parts[0].strip()
                sources = f"Annual Report 2024–25 Sources: {s_parts[1].replace(']', '').strip()}"
        
        # Remove redundant Question prefix
        main_text = re.sub(r'(?i)Question \d+:.*?\?', '', main_text, flags=re.DOTALL).strip()
        main_text = main_text.replace("Answer:", "").strip()
        
        # If it's a list from synthesized output, ensure it's properly formatted for Markdown
        if "*" not in main_text and len(main_text) > 100:
            sentences = [s.strip() for s in main_text.split(". ") if len(s.strip()) > 10]
            if len(sentences) > 1:
                main_text = "\n".join([f"* {s}" for s in sentences])

        # Return a structured Markdown response
        formatted = f"### 📊 INSIGHT\n\n{main_text}"
        
        if sources:
            formatted += f"\n\n---\n**Sources:** {sources}"
            
        if len(parts) > 1:
            details = parts[1].strip()
            details = re.split(r'\[Annual Report 2024–25 Sources:.*\]', details)[0].strip()
            formatted += f"\n\n<details>\n<summary>🔍 Data References</summary>\n\n{details}\n</details>"
            
        return formatted
    elif response_type == "action":
        try:
            if isinstance(content, str):
                json_data = json.loads(content)
            else:
                json_data = content
            action = json_data.get("action", "unknown")
            formatted_json = json.dumps(json_data, indent=2)
            
            summary = f"### ✅ {action.replace('_', ' ').title()} Initialized\n"
            if action == "schedule_meeting":
                summary += f"* **Topic:** {json_data.get('topic')}\n* **Date:** {json_data.get('date')}\n* **With:** {json_data.get('participants')}"
            elif action == "create_ticket":
                summary += f"* **Issue:** {json_data.get('issue')}\n* **Priority:** {json_data.get('priority')}\n* **Dept:** {json_data.get('department')}"
            
            return f"{summary}\n\n```json\n{formatted_json}\n```"
        except Exception:
            return str(content)
    elif response_type == "clarify":
        return f"💡 **Clarification Needed:** {content}"
    else:
        return content

if __name__ == "__main__":
    pass
