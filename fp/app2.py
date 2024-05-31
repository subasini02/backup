from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load association rules from CSV
rules = pd.read_csv('C:/Users/Bharathy(Accountant)/Downloads/SubasiniK/apriori/association_rules.csv')

# Ensure the antecedents and consequents are in the correct format (frozenset)
rules['antecedents'] = rules['antecedents'].apply(lambda x: frozenset(eval(x)))
rules['consequents'] = rules['consequents'].apply(lambda x: frozenset(eval(x)))

# Store searched items
search_history = []

# Function to extract unique items from consequents
def extract_unique_items(consequent_items_set):
    return list(consequent_items_set)

# Generate suggestions based on user input
def generate_suggestions(antecedent_items, threshold=0.0001, limit=4):
    suggestions = []
    for item in antecedent_items:
        filtered_rules = rules[(rules['antecedents'].apply(lambda x: {item}.issubset(x))) & (rules['support'] > threshold)]

        consequent_items = set()
        for consequent in filtered_rules['consequents']:
            consequent_items.update(consequent)

        # Remove antecedent item from consequent items
        consequent_items.difference_update({item})

        unique_consequent_items = extract_unique_items(consequent_items)

        # Sort unique consequent items by support value in descending order
        unique_consequent_items.sort(key=lambda item: filtered_rules[filtered_rules['consequents'].apply(lambda x: item in x)]['support'].values[0], reverse=True)

        # Limit the number of suggestions based on the limit parameter
        suggestions.extend(unique_consequent_items[:limit])
    
    return suggestions

# Generate top two recommendations for each item in the search history
def generate_top_recommendations():
    top_recommendations = {}
    for items in search_history:
        for item in items:
            suggestions = generate_suggestions(frozenset([item]))
            top_recommendations[str(item)] = suggestions[:1] if suggestions else []
    return top_recommendations


# Define route for home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        antecedent_items = frozenset(data['antecedent_items'])
        threshold = float(data.get('threshold', 0.0001))
        suggestions = generate_suggestions(antecedent_items, threshold)
        
        # Append to search history regardless of suggestions
        search_history.append(antecedent_items)
        
        # Generate top two recommendations for each item in search history
        top_recommendations = generate_top_recommendations()
        
        # Convert frozenset objects in search history to lists
        search_history_serializable = [list(item) for item in search_history]
        
        # Check if 5 or more searches have been made
        if len(search_history) >= 3:
            all_search_items = set().union(*search_history)
            unique_suggestions = list(all_search_items.difference(antecedent_items))
            return jsonify({'suggestions': suggestions, 'recommended': unique_suggestions, 'search_history': search_history_serializable, 'top_recommendations': top_recommendations})
        else:
            return jsonify({'suggestions': suggestions, 'search_history': search_history_serializable, 'top_recommendations': top_recommendations})
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
