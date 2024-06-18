import os
import pandas as pd
from pandasai import Agent

# Data for employees and salaries
employees_data = {
    'EmployeeID': [1, 2, 3, 4, 5],
    'Name': ['John', 'Emma', 'Liam', 'Olivia', 'William'],
    'Department': ['HR', 'Sales', 'IT', 'Marketing', 'Finance']
}

salaries_data = {
    'EmployeeID': [1, 2, 3, 4, 5],
    'Salary': [5000, 6000, 4500, 7000, 5500]
}

# Create DataFrames
employees_df = pd.DataFrame(employees_data)
salaries_df = pd.DataFrame(salaries_data)

# Set the API key as an environment variable
os.environ["PANDASAI_API_KEY"] = "$2a$10$7IpifTqaAeEdzo3mGOSa8uzPeaQk/.XFaBKj3WwoYwkvU.DAjx8Lq"

# Initialize the Agent
try:
    agent = Agent([employees_df, salaries_df])
    response = agent.chat("Can you make Salary Graph?")
    print(response)
except Exception as e:
    print("An error occurred:", e)
