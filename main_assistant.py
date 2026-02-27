import json

import sys

import os

import re

from transformers import pipeline

from intent_detector import detect_intent

from ner_extractor import extract_entities

from sentiment_analyzer import analyze_sentiment_and_urgency

from query_assistant import retrieve_chunks

from agent_policy import decide_next_step

from action_generator import generate_action_json

from clarifier import generate_clarification

from citation_enforcer import verify_and_enforce_citations

from ui_formatter import format_ui_response

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "google/flan-t5-base"  # Switched to base model for better generation
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
except Exception:
    # Fallback to small if base fails or isn't downloaded
    print("Warning: flan-t5-base failed to load, falling back to small.")
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

def generator(prompt, max_new_tokens=512, **kwargs):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return [{"generated_text": tokenizer.decode(outputs[0], skip_special_tokens=True)}]

def synthesize_answer(query, chunks):
    # ... (existing checks)
    if isinstance(query, list): query = " ".join([str(x) for x in query])
    if not isinstance(query, str): query = str(query)
    if not query or not query.strip():
        return "I'm sorry, I didn't catch that. Could you please rephrase your request?"

    if not chunks:
         return "I could not find this information in the dataset."

    top_references = []
    all_pages = set()
    for i, c in enumerate(chunks[:3]):
        top_references.append(f"[REF PAGE {c['page_number']}]:\n{c['content']}")
        all_pages.add(c['page_number'])
    
    for c in chunks[:10]:
        all_pages.add(c['page_number'])

    sorted_pages = sorted(list(all_pages))
    sources_str = " | ".join([f"Page {p}" for p in sorted_pages])

    # Limit context to top 3 chunks to prevent excessive truncation
    context = "\n\n".join([f"Page {c['page_number']}: {c['content']}" for c in chunks[:3]])

    # Optimized Prompt with Detailed Formatting Instructions
    prompt = (
        f"Instruction: Analyze the context and answer the question as a professional executive briefing.\n"
        f"1. **Headings**: Use clear headings to organize topics (e.g., Executive Insights, Key Highlights).\n"
        f"2. **Summary**: Start with a 2-3 sentence overview.\n"
        f"3. **Bullets**: Use bullet points for metrics, awards, and list items.\n"
        f"4. **Formatting**: Use **bold** for names/numbers and *italics* for reports/awards.\n"
        f"5. **Tone**: Professional and concise.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )
    
    result = generator(prompt, max_new_tokens=256, do_sample=False)
    synthesized = result[0]['generated_text'].strip()

    

    ref_block = "\n\n".join(top_references)

    

    return (
        f"{synthesized}\n\n"
        f"--- DETAILED DATA REFERENCES ---\n{ref_block}\n\n"
        f"[Annual Report 2024–25 Sources: {sources_str}]"
    )

def run_pipeline(user_query, history=None):

                                              

    if isinstance(user_query, dict):

        user_query = user_query.get("text", "")

    

    if isinstance(user_query, dict): user_query = user_query.get("text", "")
    if isinstance(user_query, list): user_query = " ".join([str(x) for x in user_query])
    if not isinstance(user_query, str): user_query = str(user_query)

    if not user_query or not user_query.strip():

        return "I'm sorry, I didn't catch that. Could you please rephrase your request?"

    print(f"\n--- PROCESSING QUERY: {user_query} ---\n")

    

    # 1. Retrieve Previous Intent from History
    previous_intent = None
    if history and len(history) > 0:
        last_user_msg = history[-2]["content"] if len(history) >= 2 else ""
        if last_user_msg:
             # Fast check for previous intent without full processing overhead
             prev_result = detect_intent(last_user_msg)
             previous_intent = prev_result["intent"]

    intent_data = detect_intent(user_query, previous_intent=previous_intent)
    intent = intent_data["intent"]

    previous_action_intent = None
    historical_entities = {}
    conversation_context = []

    
    if history:
        for msg in reversed(history[-5:]):
            if isinstance(msg, dict):
                m = msg
            elif isinstance(msg, (list, tuple)):
                m = {"role": "user", "content": msg[0]} if len(msg) > 0 else {}
            else:
                m = msg.__dict__
            
            if m.get("role") == "user":
                user_msg = m["content"]
                if isinstance(user_msg, list):
                    user_msg = " ".join([item["text"] for item in user_msg if item.get("type") == "text"])
                
                if not user_msg: continue
                conversation_context.insert(0, user_msg)
                prev_intent_data = detect_intent(user_msg)
                if prev_intent_data["intent"].startswith("action_") and not previous_action_intent:
                    previous_action_intent = prev_intent_data["intent"]
                
                prev_entities = extract_entities(user_msg)
                for k, v in prev_entities.items():
                    if v and v != "..." and v not in ["Low|Medium|High", "TBD"]:
                        if k not in historical_entities or historical_entities[k] in ["...", "TBD", "Low|Medium|High"]:
                            historical_entities[k] = v
            
    current_entities = extract_entities(user_query)
    entities = current_entities.copy()
    
    informational_keywords = ["who is", "tell me about", "what is", "where is", "how many", "revenue", "about", "goals", "policy", "sustainability", "esg", "cfo", "headcount", "strategy", "growth", "profit", "margin", "ebitda", "dividend"]
    is_informational_query = any(k in user_query.lower() for k in informational_keywords)
    
    is_simple_info_response = False
    query_words = user_query.strip().split()
    if len(query_words) <= 5 and not is_informational_query:
        has_simple_value = any(current_entities.get(key, "...") != "..." for key in ["date", "priority", "department", "employee_id", "application_name"])
        if has_simple_value and intent == "other":
            is_simple_info_response = True

    should_adopt_previous = False
    is_continuation_like = any(k in user_query.lower() for k in ["more", "detail", "elaborate", "tell me more", "go on", "what about", "and then", "yes", "confirm", "ok", "go ahead", "yep", "sure"])
    
    if (previous_action_intent or (history and len(history) > 0)) and intent == "other" and not is_informational_query:
        prev_intent = previous_action_intent
        if not prev_intent and history:
            last_user_msg = history[-2]["content"] if len(history) >= 2 else ""
            if last_user_msg:
                prev_intent = detect_intent(last_user_msg)["intent"]
        if prev_intent and (prev_intent.startswith("action_") or prev_intent.startswith("ask_")):
            continuation_keywords = ["already", "provided", "mentioned", "said", "told you", "gave you"]
            has_continuation_kws = any(k in user_query.lower() for k in continuation_keywords)
            
            if is_simple_info_response or has_continuation_kws or is_continuation_like or intent_data["confidence"] < 0.4:
                should_adopt_previous = True
                intent = prev_intent
                intent_data["intent"] = intent
                intent_data["confidence"] = 0.85

    global_entities = ["employee_id", "department"] 
    
    if should_adopt_previous or (intent.startswith("action_") and previous_action_intent == intent):
        for k, v_hist in historical_entities.items():
            v_curr = entities.get(k, "...")
            if (not v_curr or v_curr in ["...", "TBD"]) and v_hist and v_hist not in ["...", "TBD"]:
                entities[k] = v_hist
    else:
        for k in global_entities:
            v_hist = historical_entities.get(k)
            v_curr = entities.get(k, "...")
            if (not v_curr or v_curr in ["...", "TBD"]) and v_hist:
                 entities[k] = v_hist

    sentiment_data = analyze_sentiment_and_urgency(user_query)

    retrieval_score = 0.0
    retrieved_chunks = []
    rag_answer = ""

    is_policy_query = any(k in user_query.lower() for k in ["policy", "guideline", "rules", "terms", "entitlement", "duration", "leave", "holiday"])
    
    boost_kws = []
    if is_policy_query:
        boost_kws = ["policy", "eligibility", "weeks", "months", "benefit", "guidelines", "entitlement", "leave", "holiday"]
    elif any(k in user_query.lower() for k in ["cfo", "leadership", "ceo", "chairman", "shiv", "roshni"]):
        boost_kws = ["chief", "officer", "director", "leadership", "management", "founder", "chairman", "secretary"]
    elif any(k in user_query.lower() for k in ["revenue", "growth", "profit", "financial", "results"]):
        boost_kws = ["revenue", "profit", "growth", "financial", "margin", "ebitda", "consolidated", "income"]

    if intent.startswith("ask_") or is_informational_query:
        # Dynamic RAG Configuration based on Intent
        rag_config = {
            "ask_finance": {"k": 5, "section": "Financial"},
            "ask_hr": {"k": 10, "section": "Human"}, # HR policies need more context
            "ask_people": {"k": 8, "section": "Governance"},
            "ask_it_policy": {"k": 8, "section": "IT"},
            "ask_compliance": {"k": 10, "section": "Governance"}, # Compliance needs broad context
            "ask_security": {"k": 8, "section": "IT"},
            "ask_procurement": {"k": 5, "section": "Financial"}
        }
        
        config = rag_config.get(intent, {"k": 8, "section": None})
        target_section = config["section"]
        top_k = config["k"]

        # ... (rest of logic) ...
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        index_file = os.path.join(base_dir, "faq_index.faiss")
        mapping_file = os.path.join(base_dir, "chunks_mapping.json")
        
        if not os.path.exists(index_file) or not os.path.exists(mapping_file):
            retrieval_score = 0.0
            rag_answer = "Internal Error: Knowledge base not found."
        else:
            if " and " in user_query.lower() or "," in user_query:
                 # ... (complex query handling) ...
                query_parts = re.split(r' and |,', user_query.lower())
                query_parts = [p.strip() for p in query_parts if len(p.strip()) > 5]
                seen_ids = set()
                top_part_score = -10.0
                all_part_chunks = []
                for qp in query_parts:
                    part_chunks = retrieve_chunks(qp, index_file, mapping_file, k=top_k, boost_keywords=boost_kws, section_filter=target_section)
                    if part_chunks:
                        top_part_score = max(top_part_score, part_chunks[0]['score'])
                        for c in part_chunks:
                            if c['chunk_id'] not in seen_ids:
                                all_part_chunks.append(c)
                                seen_ids.add(c['chunk_id'])
                all_part_chunks.sort(key=lambda x: x.get('score', 0), reverse=True)
                retrieved_chunks = all_part_chunks
                top_score = top_part_score
            else:
                retrieved_chunks = retrieve_chunks(user_query, index_file, mapping_file, k=top_k, boost_keywords=boost_kws, section_filter=target_section)
                top_score = retrieved_chunks[0]['score'] if retrieved_chunks else -10.0
            
            # ... (retrieval scoring logic) ...
        
        if retrieved_chunks:
             # ... (scoring calculation) ...
            retrieval_score = 1.0 / (1.0 + pow(2.718, -(top_score + 2.0)))
            
             # ... (keyword validation) ...
            validation_entities = [v for k, v in entities.items() if v and v not in ["...", "TBD", "Low|Medium|High"]]
            query_keywords = [k for k in ["ceo", "cfo", "chairman", "revenue", "policy", "leave", "bonus", "roshni", "nadar", "shiv", "vijaykumar", "leader", "growth", "profit", "ebitda", "dividend", "headcount", "sustainability", "esg", "strategy", "director", "board"] if k in user_query.lower()]
            
            check_list = list(set(validation_entities + query_keywords))
            if check_list:
                found_relevant = False
                combined_content = " ".join([c['content'].lower() for c in retrieved_chunks])
                for item in check_list:
                    if item.lower() in combined_content:
                        found_relevant = True
                        break
                if not found_relevant:
                    retrieval_score *= 0.6 
                    
            if retrieval_score >= 0.05: 
                rag_answer = synthesize_answer(user_query, retrieved_chunks)
            else:
                rag_answer = "I could not find this information in the dataset."
        else:
            retrieval_score = 0.0
            rag_answer = "I could not find this information in the dataset."

    policy_decision = decide_next_step(intent_data, sentiment_data, entities, retrieval_score=retrieval_score)
    
    next_step = policy_decision["next_step"]
    final_output = ""

    # Sentiment-Aware Response Modification
    sentiment_prefix = ""
    if sentiment_data["urgency"] == "high":
        sentiment_prefix = "🚨 **Urgent Request:** I'm prioritizing this for you.\n\n"
    elif sentiment_data["sentiment"] == "negative":
        sentiment_prefix = "I understand you might be frustrated. Let me help clarify this for you.\n\n"

    if next_step == "answer":
        enforced_answer = verify_and_enforce_citations(rag_answer, retrieved_chunks)
        final_output = format_ui_response("answer", sentiment_prefix + enforced_answer)

    elif next_step == "action":

        action_json = generate_action_json(intent, entities)

        final_output = format_ui_response("action", action_json)

    elif next_step == "clarify":

        missing_entities = policy_decision.get("missing_entities", [])

        if missing_entities:

            clarification = generate_clarification(missing_entities)

            final_output = format_ui_response("clarify", clarification)

        else:

            final_output = "I'm here to help! Could you please tell me more about what you need?"

    elif next_step == "escalate":

        reason = policy_decision.get("reason", "Urgency or missing information.")

        final_output = f"I am escalating this request to a human agent. Reason: {reason}"

    

    return final_output

if __name__ == "__main__":

    query = sys.argv[1] if len(sys.argv) > 1 else "What was the revenue growth in FY25?"

    try:

        result = run_pipeline(query, history=[])

        print(f"\n--- OUTPUT ---\n{result}\n--------------\n")

    except Exception as e:

        print(f"Error: {e}")

