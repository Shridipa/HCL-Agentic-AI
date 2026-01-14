import json
import re
from main_assistant import run_pipeline

def calculate_metrics(results):
    total = len(results)
    if total == 0:
        return 0, 0, 0, 0

    retrieval_hits = sum(1 for r in results if r['retrieval_hit'])
    precision_scores = [r['precision'] for r in results]
    recall_scores = [r['recall'] for r in results]
    
    avg_precision = sum(precision_scores) / total
    avg_recall = sum(recall_scores) / total
    f1 = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0
    retrieval_accuracy = retrieval_hits / total

    return retrieval_accuracy, avg_precision, avg_recall, f1

def evaluate():
    print("Loading test dataset...")
    try:
        with open('test_dataset.json', 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
    except FileNotFoundError:
        print("test_dataset.json not found. Please run generate_test_data.py first.")
        return

    results = []
    print(f"{'ID':<4} | {'Query':<40} | {'Hit':<4} | {'P':<5} | {'R':<5} | {'F1':<5}")
    print("-" * 80)
    
    for case in test_cases:
        query = case["question"]
        ground_truth = case["ground_truth"]
        expected_page = case["page"]
        
        output = run_pipeline(query)
        
        # 1. Retrieval Hit (Check if expected page is cited with exact word boundary)
        retrieval_hit = re.search(r'Page ' + str(expected_page) + r'\b', output) is not None
        
        # 2. Precision/Recall based on keyword overlap (more lenient 3-char match)
        gt_words = set(re.findall(r'\w{3,}', ground_truth.lower()))
        output_words = set(re.findall(r'\w{3,}', output.lower()))
        
        intersection = gt_words.intersection(output_words)
        
        precision = len(intersection) / len(output_words) if output_words else 0
        recall = len(intersection) / len(gt_words) if gt_words else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"{case['id']:<4} | {query[:40]:<40} | {str(retrieval_hit):<4} | {precision:.2f} | {recall:.2f} | {f1:.2f}")
        
        results.append({
            "id": case["id"],
            "query": query,
            "output": output,
            "retrieval_hit": retrieval_hit,
            "precision": precision,
            "recall": recall,
            "f1": f1
        })

    ret_acc, avg_p, avg_r, avg_f1 = calculate_metrics(results)
    
    summary = {
        "total_cases": len(results),
        "retrieval_accuracy": ret_acc,
        "average_precision": avg_p,
        "average_recall": avg_r,
        "average_f1": avg_f1
    }
    
    print("\n" + "="*30)
    print("EVALUATION SUMMARY")
    print("="*30)
    print(f"Total Cases:        {summary['total_cases']}")
    print(f"Retrieval Accuracy: {summary['retrieval_accuracy']:.2%}")
    print(f"Average Precision:  {summary['average_precision']:.2%}")
    print(f"Average Recall:     {summary['average_recall']:.2%}")
    print(f"Average F1 Score:   {summary['average_f1']:.2%}")
    print("="*30)

    with open("evaluation_results.json", "w") as f:
        json.dump({"summary": summary, "details": results}, f, indent=2)
    print("\nResults saved to evaluation_results.json")

if __name__ == "__main__":
    evaluate()
