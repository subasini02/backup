# # import streamlit as st
# # import pandas as pd
# # import google.generativeai as genai
# # from io import StringIO

# # # Function to read data from uploaded CSV file
# # def read_csv_file(uploaded_file):
# #     try:
# #         df = pd.read_csv(uploaded_file)
# #         return df
# #     except Exception as e:
# #         st.error(f"Error: {e}")
# #         return None

# # # Function to display prompt
# # def display_prompt(df):
# #     if df is not None:
# #         # Fetch column names
# #         columns = df.columns.tolist()
       
# #         # Fetch a limited number of rows for preview
# #         rows = df.head(10).values.tolist()
       
# #         # Construct the prompt including column names and sample rows
# #         prompt_with_columns = ", ".join(columns)
# #         prompt_with_sample_rows = ""
# #         for row in rows:
# #             prompt_with_sample_rows += "\t" + "\t".join(map(str, row)) + "\n"
       
# #         # Combine all components into the final prompt
# #         prompt = (
# #             "You're an expert in giving similarity scores for names. You will get a db which contains names of persons. The columns are first_name, last_name, agg_first_name, and agg_last_name. You should give similarity scores based on first_name vs. agg_first_name, last_name vs. agg_last_name, and full_name vs aggr_full_name . In total, you should give 3 scores for each row. Here is your db:\n"
# #             + prompt_with_columns
# #             + "\n"
# #             + prompt_with_sample_rows
# #             + "Your answer should be like:\nfull_name\naggr_full_name\nfirst_name\tlast_name\tagg_first_name\tagg_last_name\tsim_sco_full_name\tsim_sco_first_name\tsim_sco_last_name\nashish\tb\tashish\tb\tthe score you get out of 100\tthe score you get out of 100\tthe score you get out of 100.Please give it as a table and give the output for all the rows in the given db."
# #         )
# #         return prompt
# #     else:
# #         return ""

# # # Configure Generative AI
# # genai.configure(api_key='AIzaSyD8nnaAkfuzwm9KOSGygYsxqZnZ58G8_qs')

# # # Initialize Generative Model
# # model_name = "gemini-pro"
# # model = genai.GenerativeModel(model_name)

# # # Function to get Gemini's response
# # def get_gemini_response(prompt):
# #     response = model.generate_content(prompt)
# #     return response.text

# # # Function to save response to CSV and generate download link
# # def save_response_to_csv(response):
# #     try:
# #         df = pd.read_csv(StringIO(response), sep='\t')
# #         return df
# #     except Exception as e:
# #         st.error(f"Error parsing the response: {e}")
# #         return None

# # # Initialize Streamlit app
# # st.header("Chatbot")

# # # Upload CSV file
# # uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# # # If file uploaded
# # if uploaded_file is not None:
# #     # Read data from CSV file
# #     df = read_csv_file(uploaded_file)
   
# #     # Display prompt
# #     prompt = display_prompt(df)
# #     print(df)
   
# #     # Display conversation history
# #     st.subheader("The Chat History")
   
# #     # Display prompt and get Gemini response
# #     if prompt:
# #         response = get_gemini_response(prompt)
# #         st.write(response)
        
# #         # Save response to CSV and provide download link
# #         # response_df = save_response_to_csv(response)
# #         # if response_df is not None:
# #         #     csv = response_df.to_csv(index=False).encode('utf-8')
# #         #     st.download_button(
# #         #         label="Download data as CSV",
# #         #         data=csv,
# #         #         file_name='response.csv',
# #         #         mime='text/csv',
# #         #     )

# import streamlit as st
# import pandas as pd
# import google.generativeai as genai
# from io import StringIO

# # Function to read data from uploaded CSV file
# def read_csv_file(uploaded_file):
#     try:
#         df = pd.read_csv(uploaded_file)
#         return df
#     except Exception as e:
#         st.error(f"Error: {e}")
#         return None

# # Function to display prompt
# def display_prompt(df):
#     if df is not None:
#         # Fetch column names
#         columns = df.columns.tolist()
       
#         # Fetch all rows for preview
#         rows = df.values.tolist()
       
#         # Construct the prompt including column names and all rows
#         prompt_with_columns = ", ".join(columns)
#         prompt_with_all_rows = ""
#         for row in rows:
#             prompt_with_all_rows += "\t" + "\t".join(map(str, row)) + "\n"
       
#         # Combine all components into the final prompt
#         prompt = (
#             "You're an expert in giving similarity scores for names. You will get a db which contains names of persons. The columns are first_name, last_name, agg_first_name, and agg_last_name. You should give similarity scores based on first_name vs. agg_first_name, last_name vs. agg_last_name, and full_name vs aggr_full_name. In total, you should give 3 scores for each row. Here is your db:\n"
#             + prompt_with_columns
#             + "\n"
#             + prompt_with_all_rows
#             + "Your answer should be like:\nfull_name\naggr_full_name\nfirst_name\tlast_name\tagg_first_name\tagg_last_name\tsim_sco_full_name\tsim_sco_first_name\tsim_sco_last_name\nashish\tb\tashish\tb\tthe score you get out of 100\tthe score you get out of 100\tthe score you get out of 100. Please give it as a table and give the output for all the rows in the given db."
#         )
#         return prompt
#     else:
#         return ""

# # Configure Generative AI
# genai.configure(api_key='AIzaSyD8nnaAkfuzwm9KOSGygYsxqZnZ58G8_qs')

# # Initialize Generative Model
# model_name = "gemini-pro"
# model = genai.GenerativeModel(model_name)

# # Function to get Gemini's response
# def get_gemini_response(prompt):
#     response = model.generate_content(prompt)
#     return response.text

# # Function to save response to CSV and generate download link
# def save_response_to_csv(response):
#     try:
#         df = pd.read_csv(StringIO(response), sep='\t')
#         return df
#     except Exception as e:
#         st.error(f"Error parsing the response: {e}")
#         return None

# # Initialize Streamlit app
# st.header("Chatbot")

# # Upload CSV file
# uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# # If file uploaded
# if uploaded_file is not None:
#     # Read data from CSV file
#     df = read_csv_file(uploaded_file)
   
#     # Display prompt
#     prompt = display_prompt(df)
   
#     # Display conversation history
#     st.subheader("The Chat History")
   
#     # Display prompt and get Gemini response
#     if prompt:
#         response = get_gemini_response(prompt)
#         st.write(response.head(5))
        
#         # Save response to CSV and provide download link
#         response_df = save_response_to_csv(response)
#         if response_df is not None:
#             csv = response_df.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="Download data as CSV",
#                 data=csv,
#                 file_name='response.csv',
#                 mime='text/csv',
#             )

import streamlit as st
import pandas as pd
import google.generativeai as genai
from io import StringIO
import time
from google.api_core.exceptions import InternalServerError

# Function to read data from uploaded CSV file
def read_csv_file(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to chunk data
def chunk_data(df, chunk_size):
    return [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]

# Function to display prompt for a chunk of data
def display_prompt(df_chunk):
    if df_chunk is not None:
        # Fetch column names
        columns = df_chunk.columns.tolist()
        
        # Fetch rows in the chunk
        rows = df_chunk.values.tolist()
        
        # Construct the prompt including column names and rows in the chunk
        prompt_with_columns = ", ".join(columns)
        prompt_with_rows = ""
        for row in rows:
            prompt_with_rows += "\t" + "\t".join(map(str, row)) + "\n"
        
        # Combine all components into the final prompt
        prompt = (
            "You're an expert in giving similarity scores for names. You will get a db which contains names of persons. The columns are first_name, last_name, agg_first_name, and agg_last_name. You should give similarity scores based on first_name vs. agg_first_name, last_name vs. agg_last_name, and full_name vs aggr_full_name. In total, you should give 3 scores for each row. Here is your db:\n"
            + prompt_with_columns
            + "\n"
            + prompt_with_rows
            + "Your answer should be like:\nfull_name\naggr_full_name\nfirst_name\tlast_name\tagg_first_name\tagg_last_name\tsim_sco_full_name\tsim_sco_first_name\tsim_sco_last_name\nashish\tb\tashish\tb\tthe score you get out of 100\tthe score you get out of 100\tthe score you get out of 100. Please give it as a table and give the output for all the rows in the given db."
        )
        return prompt
    else:
        return ""

# Configure Generative AI
genai.configure(api_key='AIzaSyChrZHlPjSkDh1MQcHrODIqUAo5_cpfM6U')
0
# Initialize Generative Model
model_name = "gemini-pro"
model = genai.GenerativeModel(model_name)

# Function to get Gemini's response with retry logic
def get_gemini_response(prompt, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except InternalServerError as e:
            st.warning(f"Internal server error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            break
    return None

# Function to save response to CSV and generate download link
def save_response_to_csv(response):
    try:
        df = pd.read_csv(StringIO(response), sep='\t')
        return df
    except Exception as e:
        st.error(f"Error parsing the response: {e}")
        return None

# Initialize Streamlit app
st.header("Chatbot")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# If file uploaded
if uploaded_file is not None:
    # Read data from CSV file
    df = read_csv_file(uploaded_file)
    
    # Chunk the data
    chunk_size = 100  # Adjust chunk size as needed
    df_chunks = chunk_data(df, chunk_size)
    
    # Display conversation history
    st.subheader("The Chat History")
    
    all_responses = []
    
    # Process each chunk
    for df_chunk in df_chunks:
        # Display prompt for the current chunk
        prompt = display_prompt(df_chunk)
        
        if prompt:
            response = get_gemini_response(prompt)
            if response:
                st.write(response)
                all_responses.append(response)
            else:
                st.error("Failed to get a response from the API.")
    
    # Combine all responses and save to CSV
    if all_responses:
        combined_response = "\n".join(all_responses)
        response_df = save_response_to_csv(combined_response)
        if response_df is not None:
            csv = response_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='response.csv',
                mime='text/csv',
            )

