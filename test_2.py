import sys
import re
from collections import Counter


def word_frequency_counter(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{filename}': {e}", file=sys.stderr)
        sys.exit(1)

    # Split on spaces and punctuation, similar to tr in the bash script
    words = re.split(r'[ .,();{}\[\]]', content)

    # Count all words, including empty strings
    word_counts = Counter(words)

    # Sort by count (descending) and then by word (ascending)
    # Use an empty string for the empty line to match bash script behavior
    sorted_counts = sorted(word_counts.items(), key=lambda x: (-x[1], x[0] or ""))

    # Print top 20 results
    for word, count in sorted_counts[:20]:
        print(f"{count:>7} {word}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>", file=sys.stderr)
        sys.exit(1)

    word_frequency_counter(sys.argv[1])