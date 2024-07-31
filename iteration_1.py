import sys
from preprocess import preprocess_text_to_list


def merge_sort(array: list[str]) -> list[str]:
    if len(array) <= 1:
        return array
    mid_point = len(array) // 2
    left = merge_sort(array[:mid_point])
    right = merge_sort(array[mid_point:])
    return merge(left, right)


def merge(left_array: list[str], right_array: list[str]) -> list[str]:
    result = []
    i, j = 0, 0

    while i < len(left_array) and j < len(right_array):
        if left_array[i] <= right_array[j]:
            result.append(left_array[i])
            i += 1
        else:
            result.append(right_array[j])
            j += 1

    result.extend(left_array[i:])
    result.extend(right_array[j:])
    return result


# Bucket sort
def word_count_sort(word_counts: list[tuple[int, str]]) -> list[tuple[int, str]]:
    if not word_counts:
        return []

    max_count = max(count for count, _ in word_counts)
    count_array = [[] for _ in range(max_count + 1)]
    for count, word in word_counts:
        count_array[count].append(word)
    result = []
    for count in range(max_count, 0, -1):  # Could reduce this by only iterating over top 20
        for word in count_array[count]:
            result.append((count, word))
    return result


if __name__ == "__main__":
    # Read file name by argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    # Read file content (simple reading inefficiently first, we'll use readlines() next time)
    try:
        with open(filename) as file:
            text = file.read()
    except Exception as e:
        print(f"Could not read file {filename}: {e}")

    words = preprocess_text_to_list(text)

    """
    At this point my first thought is to use merge sort algorithm on first characters
    """
    sorted_words = merge_sort(words)

    # We then count the number of consecutive lines for line counts
    counted_words = []
    current_word = sorted_words[0]
    current_word_count = 1
    for w in sorted_words[1:]:
        if w != current_word:
            counted_words.append((current_word_count, current_word))
            current_word = w
            current_word_count = 1
        else:
            current_word_count += 1

    # Sort counted words using a counting sort
    sorted_words = word_count_sort(counted_words)
    for count, word in sorted_words[:20]:
        print(f"{count} {word}")
