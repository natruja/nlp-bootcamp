#!/usr/bin/env python3
"""Fix syntax errors in cleaned notebooks (mismatched parentheses)."""

import json
import re

def fix_notebook(filepath):
    """Fix syntax errors in a notebook."""
    print(f"Fixing: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

            # Fix common syntax errors
            fixed = source

            # Fix: tokens = ___)  →  tokens = ___
            fixed = re.sub(r'= ___\)', '= ___', fixed)

            # Fix: = ___ (  →  = ___
            fixed = re.sub(r'= ___\s*\(', '= ___', fixed)

            # Fix standalone ___ with mismatched parens
            fixed = re.sub(r'___\)', '___', fixed)
            fixed = re.sub(r'\(___', '___', fixed)

            if fixed != source:
                cell['source'] = fixed
                print(f"  ✓ Fixed syntax errors")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

def main():
    notebooks = [
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
    print("FIXING SYNTAX ERRORS")
    print("="*60)

    for nb in notebooks:
        fix_notebook(nb)

    print("\n" + "="*60)
    print("✓ ALL NOTEBOOKS FIXED")
    print("="*60)

if __name__ == '__main__':
    main()
