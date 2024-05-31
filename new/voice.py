from flask import Flask, request, render_template, session
import mysql.connector
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='magilhub-intern.cb60w4qgw0y3.ap-south-1.rds.amazonaws.com',
        user='Intern',
        password='Internmagil',
        database='magildb'
    )

# Fetch data from database and construct prompt
def construct_prompt():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mh_items.name AS item_name, mh_items.summary, mh_items.sell_price,
               GROUP_CONCAT(DISTINCT mh_categories.name) AS category_names,
               GROUP_CONCAT(DISTINCT mh_ingredients.ingredient_name) AS ingredient_names
        FROM mh_items
        JOIN mh_item_category ON mh_item_category.item_id = mh_items.id
        JOIN mh_categories ON mh_categories.id = mh_item_category.category_id
        JOIN mh_item_ingredients ON mh_item_ingredients.item_id = mh_items.id
        JOIN mh_ingredients ON mh_ingredients.id = mh_item_ingredients.ingredient_id
        WHERE mh_items.location_id = '7c28311e-4a3a-418d-8564-b5d86d01ef51'
        GROUP BY mh_items.id, mh_items.name;
    """)

    columns = [i[0] for i in cursor.description]
    rows = cursor.fetchall()

    prompt_with_columns = ", ".join(columns)
    prompt_with_rows = ""
    for row in rows:
        prompt_with_rows += "\t" + "\t".join(map(str, row)) + "\n"

    prompt = (
        "You're a chatbot specialized in food menus named Cheeku. Your role involves interactively responding to menu-related inquiries using an SQL database. Here's the schema of your database:\n"
        + prompt_with_columns
        + "\nSample rows:\n"
        + prompt_with_rows
        + "\nYou should answer the given questions, and your answer should be short, sweet, and very interactive, like it is to a foodie. You are a chatbot specialized in providing responses based on the data from a specific database schema. Your primary task is to answer queries related to this database accurately and efficiently. However, in cases where questions fall outside the scope of the database schema, you should respond intelligently while staying within the bounds of your specialized knowledge."
    )

    cursor.close()
    conn.close()
    return prompt

# Configure Generative AI with the API key
genai.configure(api_key='AIzaSyDrsKjXU8DyWV3DrZvdn4S0RiC47coRqAM')

# Initialize the Generative Model
model_name = "gemini-pro"
model = genai.GenerativeModel(model_name)

# Initialize chat session
def init_chat_session():
    return model.start_chat(history=[])

# Get Gemini's response
def get_gemini_response(question, chat, prompt):
    response = chat.send_message([question, prompt], stream=True)
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []
        session["gemini_chat"] = init_chat_session()
        session["prompt"] = construct_prompt()

    if request.method == "POST":
        input_text = request.form["input_text"]
        response = get_gemini_response(input_text, session["gemini_chat"], session["prompt"])
        session["chat_history"].append(("You", input_text))
        for chunk in response:
            session["chat_history"].append(("Cheeku", chunk.text))
    
    return render_template("index.html", chat_history=session["chat_history"])

if __name__ == "__main__":
    app.run(debug=True)
