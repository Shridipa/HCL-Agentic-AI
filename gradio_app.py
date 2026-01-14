import gradio as gr
import json
import os
import datetime
import re
from main_assistant import run_pipeline

LOGO_PATH = r"C:\Users\KIIT\.gemini\antigravity\brain\a9629e95-b346-4d4d-b089-caf1bdf50c37\hcltech_assistant_logo_1767985807080.png"

CUSTOM_CSS = """
.header-area {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e5e7eb;
}
.header-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
}
.tag-badge {
    background-color: #e0f2fe;
    color: #0369a1;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 99px;
    border: 1px solid #bae6fd;
}
.section-header {
    font-weight: 600;
    color: #334155;
    margin-top: 15px;
    margin-bottom: 5px;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
}
.ticket-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 12px;
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.meeting-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 12px;
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.card-badge {
    background-color: rgba(255, 255, 255, 0.3);
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 600;
}
.card-title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 6px;
}
.card-detail {
    font-size: 0.85rem;
    opacity: 0.95;
    margin-bottom: 3px;
}
.empty-state {
    text-align: center;
    padding: 40px 20px;
    color: #94a3b8;
    font-style: italic;
}
"""

tickets_storage = []
meetings_storage = []
pending_actions = []

def format_pending_actions_display(actions):
    if not actions:
        return "<div class='empty-state'>✨ No pending actions.<br/>Ask the assistant to book something!</div>"
    
    html = ""
    for idx, action in enumerate(actions):
        action_name = action.get('action', 'Action').replace('_', ' ').title()
        html += f"""
        <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; border-radius: 12px; padding: 12px; margin-bottom: 10px;">
            <div style="font-weight: 700; color: #1e40af; font-size: 0.9rem; margin-bottom: 4px;">🎯 PENDING: {action_name}</div>
            <div style="font-size: 0.8rem; color: #475569;">
                <b>Context:</b> {action.get('topic', action.get('issue', 'General Request'))[:40]}...
            </div>
            <div style="display: flex; gap: 8px; margin-top: 8px;">
                <span style="background: #3b82f6; color: white; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem;">Action #{idx+1}</span>
            </div>
        </div>
        """
    return html

def confirm_action(index):
    try:
        idx = int(index) - 1
        if 0 <= idx < len(pending_actions):
            action = pending_actions.pop(idx)
            action_type = action.get("action", "")
            
            if action_type == "schedule_meeting":
                meetings_storage.append(action)
                msg = f"✅ Meeting '{action.get('topic')}' confirmed!"
            elif action_type == "create_ticket":
                tickets_storage.append(action)
                msg = f"✅ Ticket '{action.get('issue')}' confirmed!"
            else:
                msg = "✅ Action confirmed!"
                
            return msg, format_pending_actions_display(pending_actions), format_meetings_display(meetings_storage), format_tickets_display(tickets_storage)
        return "❌ Invalid index", format_pending_actions_display(pending_actions), format_meetings_display(meetings_storage), format_tickets_display(tickets_storage)
    except:
        return "❌ Error", format_pending_actions_display(pending_actions), format_meetings_display(meetings_storage), format_tickets_display(tickets_storage)

def clear_all_pending():
    pending_actions.clear()
    return "🗑️ Cleared.", format_pending_actions_display(pending_actions)

def format_tickets_display(tickets):
    if not tickets:
        return "<div class='empty-state'>📂 No tickets.</div>"
    
    html = ""
    for idx, ticket in enumerate(tickets):
        priority_color = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}.get(ticket.get('priority', 'Medium'), "#6b7280")
        html += f"""
        <div class="ticket-card">
            <div class="card-header">
                <span class="card-badge">#{idx + 1} - {ticket.get('department', 'IT')}</span>
                <span style="background-color: {priority_color}; padding: 3px 8px; border-radius: 8px; font-size: 0.7rem;">{ticket.get('priority', 'Medium')}</span>
            </div>
            <div class="card-title">{ticket.get('issue', 'No description')}</div>
            <div class="card-detail">📅 {ticket.get('timestamp', 'N/A')}</div>
            <div class="card-detail">Status: {ticket.get('status', 'Open')}</div>
        </div>
        """
    return html

def format_meetings_display(meetings):
    if not meetings:
        return "<div class='empty-state'>📅 No meetings.</div>"
    
    html = ""
    for idx, meeting in enumerate(meetings):
        html += f"""
        <div class="meeting-card">
            <div class="card-header">
                <span class="card-badge">#{idx + 1}</span>
                <span style="background-color: rgba(255, 255, 255, 0.3); padding: 3px 8px; border-radius: 8px; font-size: 0.7rem;">{meeting.get('date_time', 'TBD')}</span>
            </div>
            <div class="card-title">{meeting.get('topic', 'No topic')}</div>
            <div class="card-detail">👥 {meeting.get('participants', 'N/A')}</div>
            <div class="card-detail">📍 {meeting.get('location', 'Virtual')}</div>
        </div>
        """
    return html

def book_ticket_quick(issue, department, priority):
    if not issue.strip():
        return "⚠️ Provide description", format_tickets_display(tickets_storage)
    
    ticket = {
        "action": "create_ticket",
        "department": department,
        "issue": issue,
        "priority": priority,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "status": "Open"
    }
    tickets_storage.append(ticket)
    return f"✅ Ticket booked!", format_tickets_display(tickets_storage)

def schedule_meeting_quick(topic, participants, date_time, location):
    if not topic.strip():
        return "⚠️ Provide topic", format_meetings_display(meetings_storage)
    
    meeting = {
        "action": "schedule_meeting",
        "topic": topic,
        "participants": participants,
        "date_time": date_time,
        "location": location,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    }
    meetings_storage.append(meeting)
    return f"📅 Meeting scheduled!", format_meetings_display(meetings_storage)

def delete_ticket(index):
    try:
        idx = int(index) - 1
        if 0 <= idx < len(tickets_storage):
            removed = tickets_storage.pop(idx)
            return f"🗑️ Deleted: {removed.get('issue', 'Unknown')}", format_tickets_display(tickets_storage)
        return "❌ Invalid", format_tickets_display(tickets_storage)
    except:
        return "❌ Error", format_tickets_display(tickets_storage)

def delete_meeting(index):
    try:
        idx = int(index) - 1
        if 0 <= idx < len(meetings_storage):
            removed = meetings_storage.pop(idx)
            return f"🗑️ Deleted: {removed.get('topic', 'Unknown')}", format_meetings_display(meetings_storage)
        return "❌ Invalid", format_meetings_display(meetings_storage)
    except:
        return "❌ Error", format_meetings_display(meetings_storage)

def respond(message, history):
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": ""})
    
    yield "", history, format_pending_actions_display(pending_actions)

    bot_msg_full = run_pipeline(message, history[:-2])
    
    words = bot_msg_full.split()
    streaming_msg = ""
    for i, word in enumerate(words):
        streaming_msg += word + " "
        history[-1]["content"] = streaming_msg
        if i < 5 or i % 3 == 0 or i == len(words) - 1:
            yield "", history, format_pending_actions_display(pending_actions)
    
    try:
        json_match = re.search(r'```json\s*\n(.*?)\n```', bot_msg_full, re.DOTALL)
        if json_match:
            action_json_str = json_match.group(1)
            action_data = json.loads(action_json_str)
            pending_actions.insert(0, action_data)
            yield "", history, format_pending_actions_display(pending_actions)
    except:
        pass

theme = gr.themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
    text_size="sm",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui"]
)

with gr.Blocks(title="HCLTech Assistant", theme=theme, css=CUSTOM_CSS) as demo:
    with gr.Row(elem_classes="header-area"):
        with gr.Column(scale=9):
            gr.HTML("""
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div>
                        <h1 class="header-title">HCLTech Agentic Assistant</h1>
                        <span class="tag-badge">ENTERPRISE V3.0</span>
                    </div>
                </div>
            """)

    with gr.Row():
        with gr.Column(scale=2, min_width=250):
            gr.Markdown("### 📌 Enterprise Hub", elem_classes="section-header")
            with gr.Accordion("Capabilities & Knowledge", open=True):
                gr.Markdown("""
                *   ✅ Finance & Strategy RAG
                *   ✅ IT Ticketing Automation
                *   ✅ Meeting Scheduler
                *   ✅ HR Policy Assistant
                *   ✅ Access Management
                """)
            
            gr.Markdown("### 🎯 Quick Actions", elem_classes="section-header")
            gr.Markdown("""
            - "Book a ticket for laptop repair"
            - "Schedule a meeting with HR"
            - "What's our revenue growth?"
            """)

        with gr.Column(scale=4):
            gr.Markdown("### 💬 Assistant")
            chatbot = gr.Chatbot(height=500, show_label=False)
            
            with gr.Row():
                user_input = gr.Textbox(placeholder="Ask me anything...", scale=8, show_label=False)
                submit_btn = gr.Button("Send", variant="primary", scale=1)
            
            gr.Examples(
                examples=["What is the revenue growth for FY25?", "Raise an IT ticket", "Schedule a meeting"],
                inputs=user_input
            )

        with gr.Column(scale=3, min_width=300):
            gr.Markdown("### 📊 Dashboard", elem_classes="section-header")
            with gr.Tabs():
                with gr.Tab("🎯 Pending"):
                    pending_output = gr.HTML(format_pending_actions_display(pending_actions))
                    with gr.Row():
                        pending_index = gr.Number(label="Action #", precision=0, minimum=1)
                        confirm_pending_btn = gr.Button("✅ Confirm", variant="primary")
                    action_result_msg = gr.Textbox(label="Result", interactive=False, show_label=False)
                    clear_pending_btn = gr.Button("🗑️ Clear All", size="sm")

                with gr.Tab("📂 Tickets"):
                    tickets_output = gr.HTML(format_tickets_display(tickets_storage))
                    with gr.Accordion("🎫 Quick Book", open=False):
                        ticket_issue = gr.Textbox(label="Issue")
                        ticket_dept = gr.Dropdown(choices=["IT", "HR", "Finance", "Facilities"], value="IT", label="Dept")
                        ticket_priority = gr.Radio(choices=["High", "Medium", "Low"], value="Medium", label="Priority")
                        book_ticket_btn = gr.Button("📝 Book")
                    ticket_status = gr.Textbox(interactive=False, show_label=False)
                    with gr.Row():
                        delete_ticket_index = gr.Number(label="Ticket #", precision=0, minimum=1)
                        delete_ticket_btn = gr.Button("🗑️ Delete", variant="stop", size="sm")
                
                with gr.Tab("📅 Meetings"):
                    meetings_output = gr.HTML(format_meetings_display(meetings_storage))
                    with gr.Accordion("📆 Quick Schedule", open=False):
                        meeting_topic = gr.Textbox(label="Topic")
                        meeting_participants = gr.Textbox(label="Participants")
                        meeting_datetime = gr.Textbox(label="Date & Time")
                        meeting_location = gr.Textbox(label="Location", value="Virtual")
                        schedule_meeting_btn = gr.Button("📅 Schedule")
                    meeting_status = gr.Textbox(interactive=False, show_label=False)
                    with gr.Row():
                        delete_meeting_index = gr.Number(label="Meeting #", precision=0, minimum=1)
                        delete_meeting_btn = gr.Button("🗑️ Delete", variant="stop", size="sm")

    user_input.submit(respond, [user_input, chatbot], [user_input, chatbot, pending_output])
    submit_btn.click(respond, [user_input, chatbot], [user_input, chatbot, pending_output])
    confirm_pending_btn.click(confirm_action, [pending_index], [action_result_msg, pending_output, meetings_output, tickets_output])
    clear_pending_btn.click(clear_all_pending, None, [action_result_msg, pending_output])
    book_ticket_btn.click(book_ticket_quick, [ticket_issue, ticket_dept, ticket_priority], [ticket_status, tickets_output])
    delete_ticket_btn.click(delete_ticket, delete_ticket_index, [ticket_status, tickets_output])
    schedule_meeting_btn.click(schedule_meeting_quick, [meeting_topic, meeting_participants, meeting_datetime, meeting_location], [meeting_status, meetings_output])
    delete_meeting_btn.click(delete_meeting, delete_meeting_index, [meeting_status, meetings_output])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7861, allowed_paths=["C:\\"])
