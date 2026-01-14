import json
import random
from transformers import pipeline

def generate_questions():
    print("Loading chunks...")
    try:
        with open('chunks.json', 'r', encoding='utf-8') as f:
            chunks = json.load(f)
    except FileNotFoundError:
        print("chunks.json not found. Please run process_pdf.py first.")
        return

    print(f"Loaded {len(chunks)} chunks. Selecting 100 for question generation...")
    
    # Select 100 random chunks (or all if less than 100)
    sample_chunks = random.sample(chunks, min(100, len(chunks)))
    
    print("Loading question generation model (google/flan-t5-small)...")
    # Using flan-t5-small for question generation
    qg_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")
    
    test_dataset = []
    
    for i, chunk in enumerate(sample_chunks):
        content = chunk['content']
        # Truncate content if too long for the model
        context = content[:800]
        
        prompt = f"Given the following corporate text, generate a specific, factual question that can be answered using this text:\n\n{context}\n\nQuestion:"
        
        try:
            result = qg_pipeline(prompt, max_new_tokens=60, do_sample=False, truncation=True)
            question = result[0]['generated_text']
            
            # Simple ground truth is the chunk itself or a summary
            # For evaluation, we'll use keywords from the chunk
            test_dataset.append({
                "id": i + 1,
                "question": question,
                "ground_truth": content,
                "page": chunk['page_number'],
                "section": chunk.get('section', 'Unknown')
            })
            if (i + 1) % 10 == 0:
                print(f"Generated {i + 1} questions...")
        except Exception as e:
            print(f"Error generating question for chunk {i}: {e}")

    print(f"Saving {len(test_dataset)} questions to test_dataset.json...")
    with open('test_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(test_dataset, f, indent=2)
    print("Done!")

if __name__ == "__main__":
    generate_questions()
