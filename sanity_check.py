import sys
import re
from collections import Counter


def word_frequency(filename):
    # Read the file
    with open(filename, 'r') as file:
        text = file.read()

    text = re.sub(r'[.,();{}\[\]]', "\n", text)
    words = [word for word in text.split() if word]
    word_counts = Counter(words)
    sorted_words = sorted(word_counts.items(), key=lambda x: -x[1])

    for word, count in sorted_words[:20]:
        print(f"{count:>7} {word}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    word_frequency(sys.argv[1])