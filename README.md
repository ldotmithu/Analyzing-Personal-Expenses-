# Personal Expense Tracker & Financial Insights

## Project Overview

This project simulates a personal expense tracker for an individual, leveraging the Faker library to generate realistic monthly expense data. The data is processed, stored in a SQL (SQLite) database, and then analyzed using SQL queries to derive insights into spending behavior. A Streamlit web application visualizes these insights, offering a comprehensive overview of financial habits over a simulated year.

The tracker highlights expenses across various categories such as bills, groceries, subscriptions, and personal spending, aiming to provide a clear picture of financial patterns.

## Business Use Cases

* **Automated Expense Tracking:** Simulates the tracking of personal or small business expenses.
* **Spending Habit Analysis:** Categorizes and analyzes spending to identify trends and inform savings plans.
* **Financial Dashboards:** Serves as a foundation for building dashboards that visualize income and expenditure trends.

## Technical Stack

* **Python:** The core programming language.
* **Faker:** For generating synthetic, realistic data.
* **pandas:** For data manipulation and initial data handling.
* **sqlite3:** For creating and interacting with the SQL database.
* **Streamlit:** For building the interactive web application.
* **Plotly Express:** For creating dynamic and interactive visualizations.

## Project Structure
```bash 
├── app.py                      # Streamlit web application
├── database_setup.py           # Script to create DB and load data
├── generate_data.py            # Script to generate synthetic expense data
├── expenses.db                 # SQLite database file (generated after running database_setup.py)
├── requirements.txt            # Python dependencies
└── sql_queries.sql             # All SQL queries used in the project
```

## How to Run the Project

Follow these steps to set up and run the Personal Expense Tracker:

### 1. Clone the Repository (if applicable)

- If this project is in a Git repository, start by cloning it:

```bash
git clone https://github.com/ldotmithu/Analyzing-Personal-Expenses-.git
cd Analyzing-Personal-Expenses-

```    
### 2.Create a Virtual Environment (Recommended)
```bash
python -m venv venv

#activate the env
venv\Scripts\activate
```
### 3.Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Generate Data and Setup Database
- Run the database_setup.py script. This will first generate the synthetic expense data and then create the expenses.db SQLite database, populating it with the generated data.

```bash
python database_setup.py
```

### 5. Run the Streamlit Application
```bash
streamlit run app.py
```



