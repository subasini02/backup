import streamlit as st
import spacy
from collections import defaultdict, Counter
import random
import pandas as pd

corpus_list = ['Cheese Pasta', 'Crab Lollipop', 'Mexican Veggie', 'Cheese Chilly', 'Butter Naan', 'Chicken Stripes', 'Fruit Halwa', 'Onion Rava Dosai', 'Ginger Chicken Gravy', 'Full Court', 'Resistance Bands', 'White Rice', 'Paneer Makhani', 'Cauliflower Chilli Fries', 'Paneer Pasanda', 'Half Court', 'Garlic Prawn Noodles', 'Mango Kulfi ', 'Dal Mixture', 'Dal Makhani', 'Hariyali Tikka', 'Peri Peri Shawarma', 'Kara Boondi', 'Diwali Spl Thali', 'Chilli Bajji', 'Assorted Sweets 1 lb', 'Podi Dosai', 'Dragon Chicken', '6 Session (Other Coach)', "Choice of Pulao's", 'Bisi Bele Bhath', 'Paneer Masala Dosai', 'Nei Podi Idli', 'Veg Hot & Sour Soup', 'Szechwan Noodles', 'sample', 'Chilli Parotta', 'Chilli Garlic Potato Pops', 'Rava Dosai', 'Vanilla Ice Cream', 'Thala & Thalapathy Combo', 'Impossible Vegetable Omelette', 'Impossible Veg Fried Rice', 'Cheese Corn Pizza', 'Masala', 'Schezwan Chicken Fried Rice', 'Cheese Dosai', 'Buffalo Chicken Wings', '6 Session', 'hbh', 'Butterscotch', 'South Indian Thali', 'Prawn Tom Yum Soup', 'Panner Pizza', 'Popcorn Shrimp', 'Masala Dosai', 'test', 'Bubble Gum', 'Chicken Wings', 'Motichoor Laddu', 'Royal Falooda', 'Pepper-N-Lime', 'Farmers Vegetable Salad', 'Dal Pancharangi', 'Pasta', 'Paruppu Urundai', 'Aloo Kulcha', 'Prawn Manchurian', 'Chicken Thighs', 'Idli', 'Paneer 65', 'Impossible Vegetable Laba', 'Cauliflower 65', 'Mini Thenkuzhal', 'Butter Corn', 'Mushroom Pulao', 'Ribbon Pakkoda', 'Idiyappam one', 'Mysore Rava Dosai', 'Karuveppilai Poondu Kuzhambu', 'Idli Vadai Combo', 'Open Item', 'Free Range Organic Burger', 'Ceylon Parotta', 'Chicken Clear Soup', 'Pepper Tikka', 'Orange', 'Black Current', 'Head Coach', 'Peri Peri Chicken Noodles', 'RJM Kara Sev', 'Oven Roasted Free Range Chicken', 'Peas Pulao', 'Cream Of Tomato Soup', 'Idly', 'French Fries', 'Veg Olive Pizza', 'Mili Juli Sabzi', 'Ellu Murukku', 'Sweet Corn Maggi', '1 Session (Other Coach)', 'Single Cheeze Topping', 'Onion Dosai', 'Aloo Matar', 'Dragon Prawns', 'Chicken Lollipop', 'Mini Tiffin', 'Mutton nihari Test', 'Veg-Grilled', 'Impossible Veg Kothu Parotta', 'Adhirasam', 'Hand Muruku', 'Corn & Cheese Sandwich', 'Chicken Manjurian Gravy', 'South Indian Rush Lunch', 'Garlic Naan', 'Rajapalayam Thattai', 'Blue Curacao', 'Smilyes', 'Rasam Vadai', 'Garlic Chicken Pizza', 'Chapati Kurma', 'Mysore Masala Dosai', 'Plantain Bajji', 'Chicken', 'Mexican Shawarma', 'Veg Ball Manchurian', 'Masala Tea', 'Madras Filter Coffee', 'Chicken Pineapple Pizza', 'Veg Classic Burger', 'Pan Roasted Salmon Burger', 'Paneer Chilli Fries', 'Paneer Khurchan Curry', 'Chana Masala', 'Puri', 'Vegetable Dum Biriyani', 'à®¸à¯\x8dà®\x95à¯\x86à®¸à¯\x8dà®µà®¾à®©à¯\x8d à®\x9aà®¿à®\x95à¯\x8dà®\x95à®©à¯\x8d', 'Ice Cream', 'Roti', 'Bottled Water', 'Strawberry Milkshake', 'Malai Kofta Curry', 'Pepper Bbq', 'Koon Curry', 'Badusha', 'Red Chilli Bbq', 'Fried Chicken Pizza', 'Chicken Fried Rice', 'Hawaiian Mojito', 'Milagu Saaru', 'Summer course', 'Margarita Pizza', 'Fish Finger', 'Garlic Chicken Fried Rice', 'Gongura Palaakaai Curry', 'Mixed Veg. Pakoda', 'Mango Lassi', 'Mysore Rava Masala Dosa', 'Mysore Dosai', 'Chilli Mushroom', 'Mexican Pizza', 'Open Food', 'Cheese Chilli Corn', 'Almond Crusted Salmon', "Chicken Momo'S", 'Choice of Noodles', 'Veggie Mania', 'Paneer Shawarma', 'Chocolate', 'Chinese Chicken Salad', 'Cheese Fries', 'Fresh Pineapple Juices', 'Paneer Tikka Pizza', 'Apple Mayo Cheese Sandwich', 'Omapodi', 'Mushroom/Paneer', 'Learn To Swim-Infant Coaching', 'Papad', 'Cream of Tomato Soup', 'Fanta', 'Ghee Roast', 'Poori Masala', 'Paneer Butter Masala', 'Curd', 'BBQ Wings Briyani', 'Event Section', 'Babycorn Pepper Fries', 'Spaghetti and Meatballs', 'Rasmalai', 'Butter Milk', 'Honey Chilli Chicken', 'Cheese Maggi', 'Poondu Dosai (Garlic)', 'Dal Tadka', '1 Session', 'Dahi Vadai', 'Veg Kothu Parotta', 'Andhra Muruku', 'Dahi Vadai(Only On Fri / Weekend)', 'Perrier', 'Special Jack Fruit Biriyani - Saturday Lunch only', 'Sambar Vadai', 'Ken', 'Parotta Kurma', 'Avacado Milkshake', 'Chole Bhature', 'Hand Cut Fettuccini Pasta', 'Onion Bajji', 'Pongal Vadai', 'Chilly - Paneer/Gobi.', 'Kal Dosai', 'Watermelon', 'Potato Bajji ', '12 Session', 'Karuvepillai Podi Dosai (Curry Leaves powder)', 'Spicy Chicken Pasta', 'Ghee Pongal', 'Set Dosai Vadacurry (Dinner only)', 'Paneer Tikka', 'Thattai', 'Ginger Mint Soda', 'Alfaham Tikka', '9 Months', 'Rose Milk', 'Peri Peri Maggi', 'Mushroom Chilli', 'Loaded Paneer Burger', 'Regular Shawarma', 'Pepper Chicken Gravy', 'Mushroom Pepper Fries', 'Paneer Fried Rice', 'Mullu Murukku', 'Chocolate Falooda', 'Paal Katti Kurma', 'Spicy Meatball Pizza', 'Veg Clear Soup', 'Spzhezaan Paneer Pizza', 'Arabian Bbq', 'Pepper Thattai', 'Garden Fresh Corn Salad', 'Kadai Paneer Curry', 'Onion Pakoda', 'Dosa', 'Vaazhaipoo Vadai', 'Kids Burger', 'Fresh Apple Juice', 'Chilli Bajji ', 'veg rice', 'Roasted Turkey on Sourdough', 'Ever Fresh Pizza', 'Coke', 'Badam Katli', 'Veg Soup', 'Heat Pizza (Very Spicy)', 'Methi Malai Matar', 'Jeera Rice', 'Mango', 'Mini Shawarma', 'Chicken Hot & Sour Soup', 'Kaju Katli', 'Cocktail Sambar Idli', 'Chilly Idly', 'Four Cheese Ravioli', 'Pongal Vaazhai Ilai Virundhu', '10oz Ribeye Steak', 'Chicken Manchurian', 'Chilli Chicken Lollipop', 'Onion Uthappam', 'Impossible Dosai', 'Rava Masala Dosai', 'Pina Colada', 'Paper Roast', 'Cricket Balls', 'Double Cheese Pizza', 'Schezwan Mushroom', 'Chocolate Pizza', 'Butter Chicken Gravy', 'Loaded Chicken Olive Pizza', 'Kids Special Chocolate Dosai', 'Peri Peri Chicken Fried Rice', 'Butter Murukku', 'Mixed Veg ', 'Veg. Mixed Chilli', 'Appam', 'Madras Mixture', 'Cheese Corn Burger', 'Idli Vadai', 'Cream of Vegetable Soup', 'Schezwan Shawarma', 'Medhu Vadai', 'Crispy Buttermilk Chicken Sandwhich', 'Navadhanya Mixture', 'Bombay Halwa', 'Paneer Kulcha', 'Mushroom 65', 'Veg Finger', 'Mirchi Ka Salan', 'Veg Dum Biryani', 'Fried Paneer Pizza', 'Chicken Briyani (1/2)', 'Variety Rice - Bisi Bele Bhath', 'Cheesy Tomato Twist', 'BBQ Spl Briyani', 'Sweet Corn Veg. Soup', 'Tofu Tempura Dipped In Fresh Garlic Basil Sauce', 'Cheese Shawarma', 'Day', 'Sweet Paan', 'Egg Fried Rice', 'Mushroom Pizza', 'Supreme Falooda ', 'Clear Soup', 'Cream Of Vegetable Soup', 'Kuzhi Paniyaram', 'Kashmiri Pulao', 'Keerai Vadai', 'Fried Corn & Cheese Momos', '9 months', 'Naan', 'Classic Veg Pizza', 'Ennai Kathirikai', 'Steak Salad', 'Super Star Combo', 'Ginger Ale', 'methuvadai', 'Hot & Sour Soup', 'Crispy Applewood Smoked Bacon Sandwhich', 'Falooda Royal ', 'Chicken Pizza', 'Szechwan Fried Rice', 'Cheese Olive', 'Cheese Corn Nuggets', 'Chicken Shawarma', 'Vanilla', 'Ribbon Pakoda', 'Diet Coke', 'Chikku Milkshake', 'Onion Bajji ', 'Plate Shawarma', 'Chapati', 'Gulab Jamun', 'Hot & Sour Veg. Soup', 'CornÂ\xa0&Â\xa0CheeseÂ\xa0Sandwich', 'Mushroom Fried Rice', 'Small Onion Uthappam', 'Lamb Sausages', 'Chicken Paneer Kheema', 'Hariyali Bbq', 'Lime & Mint', 'Spl Mysore Pak', 'Mirapakaya Paneer', 'Idiyappam', 'Mexican Tomato Paneer', 'Plain Dosa', 'Chiili Chicken', 'Rava Kichadi', 'Brown Sugar Kesari', 'Masala Uthappam', 'Alfaham Bbq', 'Sprite', 'Liver', 'Vegetable Kothu Parotta', 'Baby Corn - Salt& Pepper', 'House Sliders', 'Matar Paneer', 'Rasam', 'Chicken Layer Pizza', 'Green Tea', 'Mexican Vanilla Shake', 'Water Melon Juice', 'CKV Special Shawarma', 'Cricket', 'Bats', 'Chilli Chicken Gravy', 'Set Dosai Vada curry', 'Loaded Chicken Burger', 'Bhindi Masala', 'Kulfi Falooda', 'Navratan Korma', 'Kadai Paneer', 'Idiyappam ', 'Schezwan Paneer', 'Green Apple', 'Hot & Sour', 'Paneer Sandwich', 'Bhel Puri', 'Sweet Corn Veg Soup', 'Caramel Pudding', 'dosa', 'Mixed Veg Pakoda', 'Dragon Paneer', 'Special Mixture', 'French Fries Pizza', 'Adai Aviyal', 'Idiyappam (Weekday Dinner and Weekends)', '3 Months', 'Assorted Ice Cream', 'Milkshare', 'Aloo Bonda', 'Bonda', 'Chilli idli', 'Malai Kofta', 'Vegetable Samosa', 'Paneer Pepper Fries', 'Paneer Egg Toast', 'Soan Papadi', 'Cheesy Fries', 'Helmets', "Veg Momo'S", 'Tikka Shawarma', 'Chicken Lallypops', 'Vegetable Jalfrezi', 'Soda', 'Pepper Sev', 'Manchurian - Mushroom/Gobi', 'Pineapple Pizza', 'Impossible Schezwan Fried Rice', 'Green Forest ', 'Chilli Fish', 'Chowk Ki Tikki', 'Jumbo Shawarma', 'Veg Fried Rice', 'Chicken Popcorn', 'Hot & Sour Veg Soup', 'Bbq Pizza', 'Paneer Maggi', 'Olive Pizza', 'Masala Vadai', 'Cutlet Chana', 'Masala Sandwich', 'Variety Rice - Curd Rice', 'Chana Samosa', 'Jumbo Sandwich', 'Prawn Chilli', 'Chicken Ball Manchurian', 'Single Court', 'Moto Sev'] # Drop NaN values and convert to list
# Function to preprocess and tokenize a list of strings

nlp = spacy.load('en_core_web_sm')

def preprocess_corpus(corpus_list):
    tokens = []
    for sentence in corpus_list:
        doc = nlp(sentence.lower())
        tokens.extend([token.text for token in doc if not token.is_punct and not token.is_space])
    return tokens

# Preprocess the corpus
tokens = preprocess_corpus(corpus_list)

# Build the Markov Chain model
markov_chain = defaultdict(Counter)

for i in range(len(tokens) - 1):
    current_word = tokens[i]
    next_word = tokens[i + 1]
    markov_chain[current_word][next_word] += 1

# Function to predict the next word using Markov Chain
def predict_next_word_markov(context, markov_chain):
    context_words = context.lower().split()
    last_word = context_words[-1]
    
    if last_word in markov_chain:
        possible_words = markov_chain[last_word]
        total = sum(possible_words.values())
        rand_val = random.randint(1, total)
        
        cumulative = 0
        for word, count in possible_words.items():
            cumulative += count
            if rand_val <= cumulative:
                return word
    return None

# Streamlit application
st.title('Next Word Prediction')
st.write('Enter a context and get the next word prediction.')

context = st.text_input('Enter context:')

if st.button('Predict Next Word'):
    if context:
        next_word = predict_next_word_markov(context, markov_chain)
        if next_word:
            st.write(f"Context: '{context}', Predicted next word: '{next_word}'")
        else:
            st.write(f"No prediction available for the context: '{context}'")
    else:
        st.write('Please enter a context to get a prediction.')
