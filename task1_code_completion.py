import time
import random
from typing import List, Dict, Any

def sort_dictionaries_ai_suggested(dict_list: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:
    return sorted(dict_list, key=lambda x: x.get(key, 0), reverse=reverse)

def sort_dictionaries_manual(dict_list: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:
    from operator import itemgetter
    
    valid_items = []
    for item in dict_list:
        if key in item:
            valid_items.append(item)
        else:
            item_copy = item.copy()
            item_copy[key] = 0
            valid_items.append(item_copy)
    
    return sorted(valid_items, key=itemgetter(key), reverse=reverse)

def performance_comparison():
    test_data = []
    for i in range(10000):
        test_data.append({
            'name': f'item_{i}',
            'score': random.randint(1, 100),
            'priority': random.choice(['high', 'medium', 'low']),
            'timestamp': random.randint(1000000, 9999999)
        })
    
    start_time = time.time()
    result_ai = sort_dictionaries_ai_suggested(test_data.copy(), 'score')
    ai_time = time.time() - start_time
    
    start_time = time.time()
    result_manual = sort_dictionaries_manual(test_data.copy(), 'score')
    manual_time = time.time() - start_time
    
    print("Performance Comparison Results:")
    print(f"AI-Suggested Implementation: {ai_time:.6f} seconds")
    print(f"Manual Implementation: {manual_time:.6f} seconds")
    print(f"Results match: {result_ai == result_manual}")
    
    return ai_time, manual_time

if __name__ == "__main__":
    sample_data = [
        {'name': 'Alice', 'score': 85, 'department': 'Engineering'},
        {'name': 'Bob', 'score': 92, 'department': 'Sales'},
        {'name': 'Charlie', 'score': 78, 'department': 'Marketing'},
        {'name': 'Diana', 'score': 96, 'department': 'Engineering'}
    ]
    
    print("Original data:")
    for item in sample_data:
        print(item)
    
    print("\nSorted by score (AI-suggested):")
    sorted_ai = sort_dictionaries_ai_suggested(sample_data, 'score', reverse=True)
    for item in sorted_ai:
        print(item)
    
    print("\nSorted by score (Manual):")
    sorted_manual = sort_dictionaries_manual(sample_data, 'score', reverse=True)
    for item in sorted_manual:
        print(item)
    
    print("\n" + "="*50)
    performance_comparison() 