import re
import random

def find_bracket_ranges(line):
    matches = re.finditer(r'(\[.*?\]|\(.*?\))', line)
    bracket_ranges = []
    for match in matches:
        bracket_ranges.append((match.start(), match.end()))
    return bracket_ranges

def generate_variations_outside_brackets(line):
    bracket_ranges = find_bracket_ranges(line)
    words = re.split(r'(\W+)', line)
    words_to_modify = [word for word in words if not re.search(r'\[.*?\]|\(.*?\)', word)]

    modified_line = words.copy()
    changes_count = 0

    for _ in range(2):  # Ustawiamy limit na 2 zmiany dla każdej linii
        if changes_count >= 2:
            break

        for i in random.sample(range(len(words_to_modify)), min(len(words_to_modify), 2)):
            word = words_to_modify[i]
            if word.isalpha():
                modified_word = word
                for j in range(len(word)):
                    char = word[j]
                    if char.isalpha():
                        replacement = random.choice([c for c in map(chr, range(97, 97+26)) if c != char])
                        modified_word = modified_word[:j] + replacement + modified_word[j+1:]
                if all(word_start < start or word_end > end for start, end in bracket_ranges for word_start, word_end in [(line.find(word), line.find(word) + len(word))]):
                    modified_line[words.index(word)] = modified_word
                    changes_count += 1

        if changes_count >= 2:
            break

    return ''.join(modified_line)

def modify_lines(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        variations = [generate_variations_outside_brackets(line) for _ in range(10)]  # Generowanie 10 wariantów dla każdej linii
        modified_lines.extend(variations)

    with open(output_file, 'w') as file:
        file.write(''.join(modified_lines))

input_file = 'genInput.txt'
output_file = 'genOutput.txt'
modify_lines(input_file, output_file)
