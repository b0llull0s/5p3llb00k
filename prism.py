import re
import sys
import os
from collections import namedtuple

# Define a tuple for the rule's scores
Specificity = namedtuple('Specificity', ['inline', 'id', 'class_attr_pseudo', 'element'])

def calculate_specificity(selector):
    """
    Calculate the specificity score of a given CSS selector.
    """
    inline = 0  # Inline styles are not handled in this script, but left for clarity
    id_selectors = len(re.findall(r'#\w+', selector))
    class_attr_pseudo_selectors = len(re.findall(r'\.\w+|\[\w+\]|\:\w+', selector))
    element_selectors = len(re.findall(r'\b\w+\b(?!#|\.|:|\[)', selector))

    return Specificity(inline, id_selectors, class_attr_pseudo_selectors, element_selectors)

def parse_css_file(file_path):
    """
    Parse the CSS file and calculate specificity for each rule.
    """
    with open(file_path, 'r') as file:
        css_content = file.read()

    # Match CSS selectors and their associated rules
    pattern = r'([^{]+)\s*\{[^}]*\}'
    matches = re.findall(pattern, css_content)

    specificity_scores = {}
    
    for match in matches:
        # Split selectors by commas for group selectors
        selectors = [selector.strip() for selector in match.split(',')]
        
        for selector in selectors:
            specificity_scores[selector] = calculate_specificity(selector)
    
    return specificity_scores

def display_specificity_scores(specificity_scores, file_name):
    """
    Display the specificity scores for each selector.
    """
    print(f"File: {file_name}")
    for selector, specificity in specificity_scores.items():
        print(f"Selector: {selector}")
        print(f"Specificity: (inline: {specificity.inline}, id: {specificity.id}, "
              f"class/attr/pseudo: {specificity.class_attr_pseudo}, element: {specificity.element})\n")

def process_single_file(css_file_path):
    """
    Process a single CSS file.
    """
    if not os.path.isfile(css_file_path):
        print(f"Error: The file '{css_file_path}' does not exist.")
        sys.exit(1)

    specificity_scores = parse_css_file(css_file_path)
    display_specificity_scores(specificity_scores, css_file_path)

def process_all_files():
    """
    Process all CSS files in the current directory.
    """
    css_files = [f for f in os.listdir('.') if f.endswith('.css')]

    if not css_files:
        print("No CSS files found in the current directory.")
        sys.exit(1)

    for css_file in css_files:
        specificity_scores = parse_css_file(css_file)
        display_specificity_scores(specificity_scores, css_file)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == '--all':
        process_all_files()
    elif len(sys.argv) == 2:
        css_file_path = sys.argv[1]
        process_single_file(css_file_path)
    else:
        print("Usage:")
        print("  python calculate_specificity.py <path-to-css-file>")
        print("  python calculate_specificity.py --all") # This option fill calculate the score for all the css files on the working directory for the script
        sys.exit(1)
