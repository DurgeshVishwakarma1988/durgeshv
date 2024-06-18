import os
import pandas as pd
import streamlit as st
import plotly.express as px
from pandasai import Agent
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font

# Set the API key as an environment variable
os.environ["PANDASAI_API_KEY"] = "$2a$10$7IpifTqaAeEdzo3mGOSa8uzPeaQk/.XFaBKj3WwoYwkvU.DAjx8Lq"

# Title of the web app
st.title("Your Data and Visualization App")

# File uploader widget
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

def style_excel(writer, sheet_name):
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    
    # Define styles
    header_fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    # Apply styles to header
    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font

if uploaded_file is not None:
    # Read the uploaded CSV file
    employees_df = pd.read_csv(uploaded_file)
    
    # Adjust the index to start from 1
    employees_df.index += 1
    
    # Display the data with color
    st.write("<h2 style='color: blue;'>Your Data:</h2>", unsafe_allow_html=True)
    st.write(employees_df)
    
    # Initialize the Agent
    agent = Agent([employees_df])
    
    # Text input for user query
    user_query = st.text_input("Ask a question about the data:")
    
    # Listen for changes in the text input field (when Enter is pressed)
    if user_query:
        try:
            # Query the agent with the user's question
            response = agent.chat(user_query)
            st.write("<h2 style='color: green;'>Response:</h2>", unsafe_allow_html=True)
            st.write(response)
            
            # Check if the response is a suitable DataFrame for visualization
            if isinstance(response, pd.DataFrame):
                # Adjust the index of the response DataFrame to start from 1
                response.index += 1
                
                # Provide options to create a bar graph based on the response
                st.write("<h3 style='color: orange;'>Create a Bar Graph from the response data</h3>", unsafe_allow_html=True)
                x_axis = st.selectbox("Select X-axis column", response.columns)
                y_axis = st.selectbox("Select Y-axis column", response.columns)
                
                if st.button("Generate Bar Graph from Response"):
                    try:
                        fig = px.bar(response, x=x_axis, y=y_axis, title=f"Bar graph of {y_axis} vs {x_axis}")
                        st.plotly_chart(fig)
                    except Exception as e:
                        st.error("An error occurred while generating the bar graph: " + str(e))
                
                # Provide option to download the response DataFrame as an Excel file with styling
                if st.button("Download Response as Excel"):
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        response.to_excel(writer, sheet_name='Sheet1', index=True)
                        style_excel(writer, 'Sheet1')
                    st.download_button(label="Download Excel file", data=buffer, file_name='response.xlsx', mime='application/vnd.ms-excel')
            else:
                st.warning("The response is not suitable for a bar graph.")
            
        except Exception as e:
            st.error("An error occurred: " + str(e))
else:
    st.info("Please upload a CSV file to proceed.")
