#!/usr/bin/env python3
"""
Clean NLP notebooks by removing answers from exercise cells.
Replace completed code with ___ blanks for students to fill in.
"""

import json
import os
import re

def clean_exercise_cell(cell_source):
    """Replace filled-in answers with ___ blanks."""

    # Common patterns to replace with ___
    patterns = [
        # Variable assignments
        (r'tokens = word_tokenize\([^)]+\)', 'tokens = ___'),
        (r'sentences = sent_tokenize\([^)]+\)', 'sentences = ___'),
        (r'filtered_tokens = \[.*?\]', 'filtered_tokens = ___'),
        (r'cleaned_tokens = \[.*?\]', 'cleaned_tokens = ___'),
        (r'text_lower = .*', 'text_lower = ___'),
        (r'stop_words = .*stopwords.*', 'stop_words = ___'),

        # Function calls on single lines
        (r'^([a-z_]+) = ([a-z_]+)\([^)]*\)$', r'\1 = ___'),

        # List comprehensions
        (r'\[.*? for .*? in .*?\]', '___'),

        # Stemmer/Lemmatizer
        (r'ps\.stem\([^)]+\)', '___'),
        (r'lem\.lemmatize\([^)]+\)', '___'),
        (r'stemmed = .*', 'stemmed = ___'),
        (r'lemmatized = ___', 'lemmatized = ___'),

        # spaCy
        (r'doc = nlp\([^)]+\)', 'doc = ___'),
        (r'\[.*?token\..*? for .*?\]', '___'),
        (r'\[.*?ent\..*? for .*?\]', '___'),

        # Regex
        (r're\.sub\([^)]+\)', '___'),
        (r're\.findall\([^)]+\)', '___'),

        # Sentiment
        (r'TextBlob\([^)]+\)', '___'),
        (r'sia\.polarity_scores\([^)]+\)', '___'),
        (r'blob\.sentiment', '___'),

        # Vectorization
        (r'cv\.fit_transform\([^)]+\)', '___'),
        (r'tfidf\.fit_transform\([^)]+\)', '___'),
        (r'lda\.fit\([^)]+\)', '___'),

        # Classification
        (r'train_test_split\([^)]+\)', '___'),
        (r'clf\.fit\([^)]+\)', '___'),
        (r'pipe\.predict\([^)]+\)', '___'),
    ]

    cleaned = cell_source
    for pattern, replacement in patterns:
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.MULTILINE)

    return cleaned

def clean_notebook(filepath):
    """Clean a single notebook file."""
    print(f"Processing: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cleaned_cells = []
    is_exercise_cell = False

    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            # Check if next cells are exercises
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            if 'YOUR TURN' in source or 'Exercise' in source:
                is_exercise_cell = True
            elif 'EXAMPLE' in source or 'CHALLENGE' in source or '##' in source:
                is_exercise_cell = False

        elif cell['cell_type'] == 'code' and is_exercise_cell:
            # Clean this exercise cell
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

            # Skip if it's just TODO comments
            if 'TODO' in source and source.count('\n') <= 3:
                cleaned_cells.append(cell)
                continue

            # Clean the code
            cleaned_source = clean_exercise_cell(source)

            # Update cell
            cell['source'] = cleaned_source
            cell['outputs'] = []  # Clear outputs
            cell['execution_count'] = None

        cleaned_cells.append(cell)

    nb['cells'] = cleaned_cells

    # Write cleaned notebook
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"  ✓ Cleaned: {filepath}")

def main():
    """Clean all NLP notebooks."""
    notebook_files = [
        'NLP_Day1_Intro_Tokenization.ipynb',
        'NLP_Day2_Stemming_Lemmatization.ipynb',
        'NLP_Day3_POS_NER.ipynb',
        'NLP_Day4_Sentiment_Analysis.ipynb',
        'NLP_Day5_Vectorization_TopicModeling.ipynb',
        'NLP_Day6_TextClassifier.ipynb',
        'NLP_Day7_FakeNewsDetection.ipynb',
        'NLP_Day8_Review_ModernNLP.ipynb',
    ]

    print("="*60)
    print("CLEANING NLP NOTEBOOKS")
    print("="*60)

    for notebook in notebook_files:
        if os.path.exists(notebook):
            clean_notebook(notebook)
        else:
            print(f"  ✗ Not found: {notebook}")

    print("\n" + "="*60)
    print("✓ ALL NOTEBOOKS CLEANED")
    print("="*60)
    print("\nNext steps:")
    print("1. Review the cleaned notebooks")
    print("2. git add .")
    print("3. git commit -m 'Remove answers from exercises'")
    print("4. git push")

if __name__ == '__main__':
    main()
