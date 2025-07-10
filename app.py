# app.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns 

DB_NAME = 'expenses.db'


def run_query(query):
    """Executes a SQL query and returns results as a Pandas DataFrame."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query(query, conn)
        return df
    except sqlite3.Error as e: 
        st.error(f"Database error executing query: {e}")
        return pd.DataFrame()
    except Exception as e: 
        st.error(f"An unexpected error occurred: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()


st.set_page_config(layout="wide", page_title="Personal Expense Tracker", page_icon="💰")


st.title("💰 Personal Expense Tracker Dashboard")
st.markdown("""
    Welcome to your personal expense tracker! This dashboard provides insights into your
    spending habits over a year based on simulated data.
    Navigate through the sidebar to explore different aspects of your financial data.
""")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Dashboard Overview",
    "Pre-defined Query Insights",
    "Custom Query Insights",
    "Raw Data Viewer"
])

@st.cache_data
def load_all_data():
    """Loads all expense data for initial display and filtering."""
    
    df = run_query("SELECT * FROM expenses ORDER BY Date;")
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        df['DayOfWeek'] = df['Date'].dt.day_name()
    return df

all_expenses_df = load_all_data()

if all_expenses_df.empty:
    st.error("No data found in the database. Please ensure `database_setup.py` was run correctly and the `expenses.db` file exists and is populated.")
    st.stop() 


min_date = all_expenses_df['Date'].min().date()
max_date = all_expenses_df['Date'].max().date()

st.sidebar.subheader("Filter Data")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


filtered_df = all_expenses_df
if len(date_range) == 2:
    start_date, end_date = sorted(date_range)
    filtered_df = all_expenses_df[(all_expenses_df['Date'].dt.date >= start_date) &
                                  (all_expenses_df['Date'].dt.date <= end_date)]
elif len(date_range) == 1:
    start_date = date_range[0]
    filtered_df = all_expenses_df[all_expenses_df['Date'].dt.date == start_date]


if page == "Dashboard Overview":
    st.header("📊 Overall Spending Habits")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_spent = filtered_df['Amount_Paid'].sum()
        st.metric("Total Spending", f"₹{total_spent:,.2f}")
    with col2:
        total_cashback = filtered_df['Cashback'].sum()
        st.metric("Total Cashback Received", f"₹{total_cashback:,.2f}")
    with col3:
        num_transactions = len(filtered_df)
        st.metric("Total Transactions", f"{num_transactions}")
    with col4:
        avg_transaction = filtered_df['Amount_Paid'].mean()
        st.metric("Avg. Transaction Value", f"₹{avg_transaction:,.2f}")

    st.markdown("---")

    
    st.subheader("Monthly Spending Trend")
    monthly_spending = filtered_df.groupby('Month')['Amount_Paid'].sum().reset_index()
    fig_monthly_spending = px.line(monthly_spending, x='Month', y='Amount_Paid',
                                   title='Total Spending Per Month', markers=True,
                                   labels={'Amount_Paid': 'Amount (₹)', 'Month': 'Month'},
                                   height=400)
    st.plotly_chart(fig_monthly_spending, use_container_width=True)

    st.markdown("---")

    col_vis1, col_vis2 = st.columns(2)

    with col_vis1:
        st.subheader("Spending by Category")
        category_spending = filtered_df.groupby('Category')['Amount_Paid'].sum().reset_index()
        fig_category = px.bar(category_spending.sort_values(by='Amount_Paid', ascending=False),
                              x='Amount_Paid', y='Category', orientation='h',
                              title='Total Spending Per Category',
                              labels={'Amount_Paid': 'Amount (₹)', 'Category': 'Category'},
                              height=450)
        st.plotly_chart(fig_category, use_container_width=True)

    with col_vis2:
        st.subheader("Spending by Payment Mode")
        payment_mode_spending = filtered_df.groupby('Payment_Mode')['Amount_Paid'].sum().reset_index()
        fig_payment = px.pie(payment_mode_spending, values='Amount_Paid', names='Payment_Mode',
                             title='Spending Distribution by Payment Mode',
                             hole=0.3,
                             height=450)
        st.plotly_chart(fig_payment, use_container_width=True)

    st.markdown("---")

    
    st.subheader("Monthly Cashback Trend")
    monthly_cashback = filtered_df.groupby('Month')['Cashback'].sum().reset_index()
    fig_cashback_trend = px.line(monthly_cashback, x='Month', y='Cashback',
                                 title='Total Cashback Received Per Month', markers=True,
                                 labels={'Cashback': 'Cashback (₹)', 'Month': 'Month'},
                                 height=400, color_discrete_sequence=['green'])
    st.plotly_chart(fig_cashback_trend, use_container_width=True)

elif page == "Pre-defined Query Insights":
    st.header("🎯 Pre-defined Query Insights")

    st.subheader("1. Total Amount Spent in Each Category")
    df_cat_total = run_query("SELECT Category, SUM(Amount_Paid) AS Total_Amount_Spent FROM expenses GROUP BY Category ORDER BY Total_Amount_Spent DESC;")
    st.dataframe(df_cat_total, use_container_width=True)
    fig = px.bar(df_cat_total, x='Total_Amount_Spent', y='Category', orientation='h',
                 title='Total Spending Per Category', labels={'Total_Amount_Spent': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("2. Total Amount Spent Using Each Payment Mode")
    df_payment_mode = run_query("SELECT Payment_Mode, SUM(Amount_Paid) AS Total_Amount_Spent FROM expenses GROUP BY Payment_Mode;")
    st.dataframe(df_payment_mode, use_container_width=True)
    fig = px.pie(df_payment_mode, values='Total_Amount_Spent', names='Payment_Mode',
                 title='Spending Distribution by Payment Mode', hole=0.3)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("3. Total Cashback Received Across All Transactions")
    df_total_cashback = run_query("SELECT SUM(Cashback) AS Total_Cashback_Received FROM expenses;")
    st.dataframe(df_total_cashback, use_container_width=True)
    st.info(f"**Overall Cashback Received: ₹{df_total_cashback['Total_Cashback_Received'].iloc[0]:,.2f}**")

    st.subheader("4. Top 5 Most Expensive Categories")
    df_top5_cat = run_query("SELECT Category, SUM(Amount_Paid) AS Total_Amount_Spent FROM expenses GROUP BY Category ORDER BY Total_Amount_Spent DESC LIMIT 5;")
    st.dataframe(df_top5_cat, use_container_width=True)
    fig = px.bar(df_top5_cat, x='Total_Amount_Spent', y='Category', orientation='h',
                 title='Top 5 Most Expensive Categories', color='Category',
                 labels={'Total_Amount_Spent': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("5. Spending on Transportation Using Different Payment Modes")
    df_transport_mode = run_query("SELECT Payment_Mode, SUM(Amount_Paid) AS Transportation_Spending FROM expenses WHERE Category = 'Transportation' GROUP BY Payment_Mode;")
    st.dataframe(df_transport_mode, use_container_width=True)
    fig = px.bar(df_transport_mode, x='Payment_Mode', y='Transportation_Spending',
                 title='Transportation Spending by Payment Mode',
                 labels={'Transportation_Spending': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("6. Transactions that Resulted in Cashback")
    df_cashback_txns = run_query("SELECT Date, Category, Description, Amount_Paid, Cashback FROM expenses WHERE Cashback > 0 ORDER BY Date DESC;")
    st.dataframe(df_cashback_txns, use_container_width=True)
    if not df_cashback_txns.empty:
        st.write(f"Total transactions with cashback: {len(df_cashback_txns)}")

    st.subheader("7. Total Spending in Each Month of the Year")
    df_monthly_total = run_query("SELECT STRFTIME('%Y-%m', Date) AS Month, SUM(Amount_Paid) AS Monthly_Spending FROM expenses GROUP BY Month ORDER BY Month;")
    st.dataframe(df_monthly_total, use_container_width=True)
    fig = px.line(df_monthly_total, x='Month', y='Monthly_Spending', title='Total Spending Per Month', markers=True,
                  labels={'Monthly_Spending': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("8. Months with Highest Spending in 'Travel', 'Entertainment', or 'Gifts'")
    df_peak_categories = run_query("SELECT STRFTIME('%Y-%m', Date) AS Month, Category, SUM(Amount_Paid) AS Total_Category_Spending FROM expenses WHERE Category IN ('Travel', 'Entertainment', 'Gifts') GROUP BY Month, Category ORDER BY Month, Total_Category_Spending DESC;")
    st.dataframe(df_peak_categories, use_container_width=True)
    if not df_peak_categories.empty:
        fig = px.bar(df_peak_categories, x='Month', y='Total_Category_Spending', color='Category',
                     title='Spending in Travel, Entertainment, Gifts by Month',
                     labels={'Total_Category_Spending': 'Amount (₹)'})
        st.plotly_chart(fig, use_container_width=True)


    st.subheader("9. Recurring Expenses During Specific Months (e.g., insurance premiums, property taxes)")
    df_recurring = run_query("""
        SELECT Category, STRFTIME('%m', Date) AS Month_Number, COUNT(*) AS Transaction_Count
        FROM expenses
        WHERE Category IN ('Bills', 'Subscriptions', 'Rent', 'Insurance', 'Utilities')
        GROUP BY Category, Month_Number
        HAVING COUNT(*) > 1
        ORDER BY Category, Month_Number;
    """)
    st.dataframe(df_recurring, use_container_width=True)
    st.markdown("*(Note: `HAVING COUNT(*) > 1` helps identify categories appearing multiple times in the same month number across the year, suggesting a recurring nature.)*")

    st.subheader("10. Cashback or Rewards Earned in Each Month")
    df_monthly_cashback = run_query("SELECT STRFTIME('%Y-%m', Date) AS Month, SUM(Cashback) AS Total_Cashback_Earned FROM expenses GROUP BY Month ORDER BY Month;")
    st.dataframe(df_monthly_cashback, use_container_width=True)
    fig = px.bar(df_monthly_cashback, x='Month', y='Total_Cashback_Earned',
                 title='Total Cashback Earned Per Month', labels={'Total_Cashback_Earned': 'Cashback (₹)'},
                 color_discrete_sequence=['green'])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("11. How has your overall spending changed over time?")
    st.markdown("*(See 'Total Spending Per Month' chart in Dashboard Overview or Query 7 for visualization.)*")
    st.dataframe(df_monthly_total, use_container_width=True) 
    st.markdown("Analyze the trend (increasing, decreasing, stable) from the line chart. Typically, you'd look for slopes or plateaus.")


    st.subheader("12. Typical Costs Associated with Different Types of Travel")
    df_travel_costs = run_query("""
        SELECT Category, AVG(Amount_Paid) AS Average_Cost
        FROM expenses
        WHERE Category LIKE '%Travel%' OR Category = 'Transportation'
        GROUP BY Category
        ORDER BY Average_Cost DESC;
    """)
    st.dataframe(df_travel_costs, use_container_width=True)
    if not df_travel_costs.empty:
        fig = px.bar(df_travel_costs, x='Category', y='Average_Cost',
                     title='Average Costs by Travel-Related Category',
                     labels={'Average_Cost': 'Average Amount (₹)'})
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("*(Note: If your data generation creates more specific travel sub-categories like 'Travel - Flights', the insights would be more granular.)*")

    st.subheader("13. Patterns in Grocery Spending (e.g., higher spending on weekends, increased spending during specific seasons)")
    st.markdown("### Weekly Grocery Spending Pattern")
    df_weekly_grocery = run_query("""
        SELECT CASE STRFTIME('%w', Date)
                   WHEN '0' THEN 'Sunday'
                   WHEN '1' THEN 'Monday'
                   WHEN '2' THEN 'Tuesday'
                   WHEN '3' THEN 'Wednesday'
                   WHEN '4' THEN 'Thursday'
                   WHEN '5' THEN 'Friday'
                   WHEN '6' THEN 'Saturday'
               END AS Day_of_Week,
               AVG(Amount_Paid) AS Average_Grocery_Spending
        FROM expenses
        WHERE Category = 'Groceries'
        GROUP BY Day_of_Week
        ORDER BY Day_of_Week; -- Order by day number (0-6)
    """)
    
    day_order_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    if not df_weekly_grocery.empty:
        df_weekly_grocery['Day_of_Week'] = pd.Categorical(df_weekly_grocery['Day_of_Week'], categories=day_order_names, ordered=True)
        df_weekly_grocery = df_weekly_grocery.sort_values('Day_of_Week')

    st.dataframe(df_weekly_grocery, use_container_width=True)
    if not df_weekly_grocery.empty:
        fig = px.bar(df_weekly_grocery, x='Day_of_Week', y='Average_Grocery_Spending',
                     title='Average Grocery Spending by Day of Week',
                     labels={'Average_Grocery_Spending': 'Average Amount (₹)'})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Monthly/Seasonal Grocery Spending Pattern")
    df_monthly_grocery = run_query("""
        SELECT STRFTIME('%Y-%m', Date) AS Month, SUM(Amount_Paid) AS Monthly_Grocery_Spending
        FROM expenses
        WHERE Category = 'Groceries'
        GROUP BY Month
        ORDER BY Month;
    """)
    st.dataframe(df_monthly_grocery, use_container_width=True)
    if not df_monthly_grocery.empty:
        fig = px.line(df_monthly_grocery, x='Month', y='Monthly_Grocery_Spending',
                      title='Monthly Grocery Spending Trend', markers=True,
                      labels={'Monthly_Grocery_Spending': 'Amount (₹)'})
        st.plotly_chart(fig, use_container_width=True)


    st.subheader("14. Define High and Low Priority Categories")
    st.markdown("""
        This is an interpretive insight based on overall spending and necessity.
        Based on the data, we can define:
        * **High Priority Categories (Essential/High Spend):** `Rent`, `Bills`, `Groceries`, `Transportation`, `Insurance`, `Utilities`. These are often necessary and high-cost.
        * **Low Priority Categories (Discretionary/Lower Spend):** `Entertainment`, `Shopping`, `Gifts`, `Personal Care`, `Miscellaneous`, `Food & Dining` (can be reduced). These are areas where spending cuts can be more easily made.
        *You would typically analyze your top spending categories (from query 1 or 4) to identify these.*
    """)
    df_cat_total_for_priority = run_query("SELECT Category, SUM(Amount_Paid) AS Total_Amount_Spent FROM expenses GROUP BY Category ORDER BY Total_Amount_Spent DESC;")
    st.dataframe(df_cat_total_for_priority, use_container_width=True) # Re-display query 1 for context

    st.subheader("15. Which Category Contributes the Highest Percentage of the Total Spending?")
    df_highest_percentage = run_query("""
        SELECT
            Category,
            SUM(Amount_Paid) AS Category_Spending,
            (SUM(Amount_Paid) * 100.0 / (SELECT SUM(Amount_Paid) FROM expenses)) AS Percentage_of_Total
        FROM expenses
        GROUP BY Category
        ORDER BY Percentage_of_Total DESC
        LIMIT 1;
    """)
    st.dataframe(df_highest_percentage, use_container_width=True)
    if not df_highest_percentage.empty:
        st.info(f"**Highest contributing category: {df_highest_percentage['Category'].iloc[0]} with {df_highest_percentage['Percentage_of_Total'].iloc[0]:.2f}% of total spending.**")

elif page == "Custom Query Insights":
    st.header("🔍 Custom Insightful Queries")
    st.markdown("Here are additional queries to further explore spending patterns.")

    st.subheader("1. Average Daily Spending")
    df_avg_daily = run_query("SELECT Date, SUM(Amount_Paid) AS Daily_Total_Spending FROM expenses GROUP BY Date ORDER BY Date;")
    st.dataframe(df_avg_daily, use_container_width=True)
    fig = px.line(df_avg_daily, x='Date', y='Daily_Total_Spending',
                  title='Average Daily Spending Over Time', markers=True,
                  labels={'Daily_Total_Spending': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("2. Number of Transactions Per Category")
    df_txn_count_cat = run_query("SELECT Category, COUNT(*) AS Transaction_Count FROM expenses GROUP BY Category ORDER BY Transaction_Count DESC;")
    st.dataframe(df_txn_count_cat, use_container_width=True)
    fig = px.bar(df_txn_count_cat, x='Transaction_Count', y='Category', orientation='h',
                 title='Number of Transactions Per Category',
                 labels={'Transaction_Count': 'Number of Transactions'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("3. Highest Single Transaction in Each Category")
    df_max_txn_cat = run_query("SELECT Category, MAX(Amount_Paid) AS Highest_Transaction FROM expenses GROUP BY Category ORDER BY Highest_Transaction DESC;")
    st.dataframe(df_max_txn_cat, use_container_width=True)
    fig = px.bar(df_max_txn_cat, x='Highest_Transaction', y='Category', orientation='h',
                 title='Highest Single Transaction Per Category',
                 labels={'Highest_Transaction': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("4. Days of the Week with the Highest Overall Spending")
    df_daily_spending_dow = run_query("""
        SELECT CASE STRFTIME('%w', Date)
                   WHEN '0' THEN 'Sunday'
                   WHEN '1' THEN 'Monday'
                   WHEN '2' THEN 'Tuesday'
                   WHEN '3' THEN 'Wednesday'
                   WHEN '4' THEN 'Thursday'
                   WHEN '5' THEN 'Friday'
                   WHEN '6' THEN 'Saturday'
               END AS Day_of_Week,
               SUM(Amount_Paid) AS Total_Spending
        FROM expenses
        GROUP BY Day_of_Week
        ORDER BY Total_Spending DESC;
    """)
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if not df_daily_spending_dow.empty:
        df_daily_spending_dow['Day_of_Week'] = pd.Categorical(df_daily_spending_dow['Day_of_Week'], categories=day_order, ordered=True)
        df_daily_spending_dow = df_daily_spending_dow.sort_values('Day_of_Week')

    st.dataframe(df_daily_spending_dow, use_container_width=True)
    fig = px.bar(df_daily_spending_dow, x='Day_of_Week', y='Total_Spending',
                 title='Total Spending by Day of Week', labels={'Total_Spending': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("5. Average Cashback Percentage per Transaction (where cashback > 0)")
    df_avg_cashback_pct = run_query("SELECT AVG(Cashback * 100.0 / Amount_Paid) AS Avg_Cashback_Percentage FROM expenses WHERE Cashback > 0 AND Amount_Paid > 0;")
    st.dataframe(df_avg_cashback_pct, use_container_width=True)
    if not df_avg_cashback_pct.empty and df_avg_cashback_pct['Avg_Cashback_Percentage'].iloc[0] is not None:
        st.info(f"**Average Cashback Percentage on qualifying transactions: {df_avg_cashback_pct['Avg_Cashback_Percentage'].iloc[0]:.2f}%**")
    else:
        st.info("No transactions with cashback found or amount paid was zero.")

    st.subheader("6. Top 3 Spending Days in the Year")
    df_top_spending_days = run_query("SELECT Date, SUM(Amount_Paid) AS Daily_Total FROM expenses GROUP BY Date ORDER BY Daily_Total DESC LIMIT 3;")
    st.dataframe(df_top_spending_days, use_container_width=True)
    if not df_top_spending_days.empty:
        st.info(f"**Top 3 Spending Days:**")
        for index, row in df_top_spending_days.iterrows():
            st.write(f"- {row['Date']}: ₹{row['Daily_Total']:,.2f}")

    st.subheader("7. Comparison of 'Cash' vs. 'Online' Spending Trends Over Months")
    df_cash_vs_online = run_query("""
        SELECT STRFTIME('%Y-%m', Date) AS Month, Payment_Mode, SUM(Amount_Paid) AS Monthly_Spending
        FROM expenses
        GROUP BY Month, Payment_Mode
        ORDER BY Month, Payment_Mode;
    """)
    st.dataframe(df_cash_vs_online, use_container_width=True)
    fig = px.line(df_cash_vs_online, x='Month', y='Monthly_Spending', color='Payment_Mode',
                  title='Monthly Spending: Cash vs. Online', markers=True,
                  labels={'Monthly_Spending': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("8. Categories with No Cashback Received (Potential Missed Savings)")
    df_no_cashback_cat = run_query("""
        SELECT DISTINCT Category
        FROM expenses
        WHERE Cashback = 0 AND Amount_Paid > 0;
    """)
    st.dataframe(df_no_cashback_cat, use_container_width=True)
    st.markdown("These categories might be areas where you could look for cashback offers or alternative payment methods.")

    st.subheader("9. Monthly Average Transaction Value")
    df_avg_txn_monthly = run_query("SELECT STRFTIME('%Y-%m', Date) AS Month, AVG(Amount_Paid) AS Average_Transaction_Value FROM expenses GROUP BY Month ORDER BY Month;")
    st.dataframe(df_avg_txn_monthly, use_container_width=True)
    fig = px.bar(df_avg_txn_monthly, x='Month', y='Average_Transaction_Value',
                 title='Average Transaction Value Per Month',
                 labels={'Average_Transaction_Value': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("10. Total Spending on 'Food & Dining' by Day of Week")
    df_food_dow = run_query("""
        SELECT CASE STRFTIME('%w', Date)
                   WHEN '0' THEN 'Sunday'
                   WHEN '1' THEN 'Monday'
                   WHEN '2' THEN 'Tuesday'
                   WHEN '3' THEN 'Wednesday'
                   WHEN '4' THEN 'Thursday'
                   WHEN '5' THEN 'Friday'
                   WHEN '6' THEN 'Saturday'
               END AS Day_of_Week,
               SUM(Amount_Paid) AS Total_Food_Spending
        FROM expenses
        WHERE Category = 'Food & Dining'
        GROUP BY Day_of_Week
        ORDER BY Total_Food_Spending DESC;
    """)
    
    if not df_food_dow.empty:
        df_food_dow['Day_of_Week'] = pd.Categorical(df_food_dow['Day_of_Week'], categories=day_order, ordered=True)
        df_food_dow = df_food_dow.sort_values('Day_of_Week')
    st.dataframe(df_food_dow, use_container_width=True)
    fig = px.bar(df_food_dow, x='Day_of_Week', y='Total_Food_Spending',
                 title='Total Food & Dining Spending by Day of Week',
                 labels={'Total_Food_Spending': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("11. Percentage of Transactions with Cashback")
    df_pct_cashback_txns = run_query("""
        SELECT
            CAST(SUM(CASE WHEN Cashback > 0 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS Percentage_Transactions_With_Cashback
        FROM expenses;
    """)
    st.dataframe(df_pct_cashback_txns, use_container_width=True)
    if not df_pct_cashback_txns.empty and df_pct_cashback_txns['Percentage_Transactions_With_Cashback'].iloc[0] is not None:
        st.info(f"**Percentage of transactions that received cashback: {df_pct_cashback_txns['Percentage_Transactions_With_Cashback'].iloc[0]:.2f}%**")
    else:
        st.info("No transactions found.")

    st.subheader("12. Total Spending for First 6 Months vs. Last 6 Months")
    df_h1_h2_spending = run_query("""
        SELECT
            SUM(CASE WHEN STRFTIME('%m', Date) BETWEEN '01' AND '06' THEN Amount_Paid ELSE 0 END) AS H1_Spending,
            SUM(CASE WHEN STRFTIME('%m', Date) BETWEEN '07' AND '12' THEN Amount_Paid ELSE 0 END) AS H2_Spending
        FROM expenses;
    """)
    st.dataframe(df_h1_h2_spending, use_container_width=True)
    if not df_h1_h2_spending.empty:
        h1 = df_h1_h2_spending['H1_Spending'].iloc[0]
        h2 = df_h1_h2_spending['H2_Spending'].iloc[0]
        st.info(f"**H1 (Jan-Jun) Spending:** ₹{h1:,.2f}")
        st.info(f"**H2 (Jul-Dec) Spending:** ₹{h2:,.2f}")
        if h1 > h2:
            st.warning("Spending was higher in the first half of the year.")
        elif h2 > h1:
            st.success("Spending was higher in the second half of the year.")
        else:
            st.info("Spending was roughly equal in both halves.")

    st.subheader("13. Monthly Spending by Category (Stacked Bar Chart)")
    df_monthly_category = run_query("""
        SELECT STRFTIME('%Y-%m', Date) AS Month, Category, SUM(Amount_Paid) AS Monthly_Category_Spending
        FROM expenses
        GROUP BY Month, Category
        ORDER BY Month, Category;
    """)
    st.dataframe(df_monthly_category, use_container_width=True)
    fig = px.bar(df_monthly_category, x='Month', y='Monthly_Category_Spending', color='Category',
                 title='Monthly Spending Breakdown by Category',
                 labels={'Monthly_Category_Spending': 'Amount (₹)'})
    st.plotly_chart(fig, use_container_width=True)


elif page == "Raw Data Viewer":
    st.header("📋 Raw Expense Data")
    st.markdown("Here you can view the raw simulated expense data.")


    st.dataframe(all_expenses_df, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Developed with Streamlit for Financial Insights.")