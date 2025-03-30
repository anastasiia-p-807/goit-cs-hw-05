import requests
import re
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

def get_text(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error getting text from URL: {e}")
        raise

def clean_text(text: str) -> List[str]:
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return [word for word in text.split() if word]

def map_function(word: str) -> Tuple[str, int]:
    return word, 1

def shuffle_function(mapped_values: List[Tuple[str, int]]) -> List[Tuple[str, List[int]]]:
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return list(shuffled.items())

def reduce_function(key_values: Tuple[str, List[int]]) -> Tuple[str, int]:
    key, values = key_values
    return key, sum(values)

def map_reduce(text: str) -> Dict[str, int]:
    words = clean_text(text)
    
    # Parallel Mapping
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))
    
    # Shuffle
    shuffled_values = shuffle_function(mapped_values)
    
    # Parallel Reduction
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))
    
    return dict(reduced_values)

def visualize_top_words(word_freq: Dict[str, int], top_n: int = 10) -> None:
    """Visualizes top-N most frequent words."""
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    # Split results
    words, frequencies = zip(*sorted_words)
    
    # Create plot
    plt.figure(figsize=(12, 6))
    plt.bar(words, frequencies)
    plt.title(f'Top-{top_n} Most Frequent Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    plt.savefig('word_frequency.png')
    print("Plot saved as 'word_frequency.png'")

def main():
    url = "https://docs.python.org/3/library/asyncio.html"
    top_n = 10
    
    try:
        text = get_text(url)
        
        word_freq = map_reduce(text)
        
        visualize_top_words(word_freq, top_n)
        
        print(f"Total unique words: {len(word_freq)}")
        
    except Exception as e:
        print(f"Error running program: {e}")

if __name__ == '__main__':
    main() 