from flask import Flask, render_template, request, jsonify
import pandas as pd
from itertools import combinations

app = Flask(__name__)

# Load association rules from CSV
rules = pd.read_csv('F:/Task/fp/association_rules.csv')

# Ensure the antecedents and consequents are in the correct format (frozenset)
rules['antecedents'] = rules['antecedents'].apply(lambda x: frozenset(eval(x)))
rules['consequents'] = rules['consequents'].apply(lambda x: frozenset(eval(x)))

# Store searched items
search_history = []

# Function to extract unique items from consequents
def extract_unique_items(consequent_items_set):
    return list(consequent_items_set)

# Generate suggestions based on user input
def generate_suggestions(antecedent_items, threshold=0.002):
    filtered_rules = rules[(rules['antecedents'].apply(lambda x: antecedent_items.issubset(x))) & (rules['consequent support'] > threshold)]

    consequent_items = set()
    for consequent in filtered_rules['consequents']:
        consequent_items.update(consequent)

    # Remove antecedent items from consequent items
    consequent_items.difference_update(antecedent_items)

    unique_consequent_items = extract_unique_items(consequent_items)
    
    antecedent_combinations = []
    for r in range(1, len(unique_consequent_items) + 1):
        antecedent_combinations.extend(combinations(unique_consequent_items, r))

    suggestions = set()  # Use a set to store unique suggestions
    for combination in antecedent_combinations:
        combination_set = frozenset(combination)
        filtered_rules = rules[(rules['antecedents'].apply(lambda x: combination_set.issubset(x))) & (rules['consequent support'] > threshold)]

        for consequent in filtered_rules['consequents']:
            suggestions.update(consequent)
    
    # Remove antecedent items from suggestions
    suggestions.difference_update(antecedent_items)
    
    return list(suggestions)  # Convert the set back to a list

# Define route for home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        antecedent_items = frozenset(data['antecedent_items'])
        threshold = float(data.get('threshold', 0.002))
        suggestions = generate_suggestions(antecedent_items, threshold)
        search_history.append(antecedent_items)
        
        # Check if 5 or more searches have been made
        if len(search_history) >= 10:
            all_search_items = set().union(*search_history)
            unique_suggestions = list(all_search_items.difference(antecedent_items))
            return jsonify({'suggestions': suggestions, 'recommended': unique_suggestions})
        else:
            return jsonify({'suggestions': suggestions})
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
