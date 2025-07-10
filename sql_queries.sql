

-- 1. What is the total amount spent in each category?
SELECT Category, SUM(Amount_Paid) AS Total_Amount_Spent
FROM expenses
GROUP BY Category
ORDER BY Total_Amount_Spent DESC;

-- 2. What is the total amount spent using each payment mode?
SELECT Payment_Mode, SUM(Amount_Paid) AS Total_Amount_Spent
FROM expenses
GROUP BY Payment_Mode;

-- 3. What is the total cashback received across all transactions?
SELECT SUM(Cashback) AS Total_Cashback_Received
FROM expenses;

-- 4. Which are the top 5 most expensive categories in terms of spending?
SELECT Category, SUM(Amount_Paid) AS Total_Amount_Spent
FROM expenses
GROUP BY Category
ORDER BY Total_Amount_Spent DESC
LIMIT 5;

-- 5. How much was spent on transportation using different payment modes?
SELECT Payment_Mode, SUM(Amount_Paid) AS Transportation_Spending
FROM expenses
WHERE Category = 'Transportation'
GROUP BY Payment_Mode;

-- 6. Which transactions resulted in cashback?
SELECT Date, Category, Description, Amount_Paid, Cashback
FROM expenses
WHERE Cashback > 0
ORDER BY Date DESC;

-- 7. What is the total spending in each month of the year?
SELECT STRFTIME('%Y-%m', Date) AS Month, SUM(Amount_Paid) AS Monthly_Spending
FROM expenses
GROUP BY Month
ORDER BY Month;

-- 8. Which months have the highest spending in categories like "Travel," "Entertainment," or "Gifts"?
SELECT STRFTIME('%Y-%m', Date) AS Month, Category, SUM(Amount_Paid) AS Total_Category_Spending
FROM expenses
WHERE Category IN ('Travel', 'Entertainment', 'Gifts')
GROUP BY Month, Category
ORDER BY Month, Total_Category_Spending DESC;

-- 9. Are there any recurring expenses that occur during specific months of the year (e.g., insurance premiums, property taxes)?
-- This query identifies if specific categories appear in consistent months across the year, suggesting a recurring nature.
SELECT Category, STRFTIME('%m', Date) AS Month_Number, COUNT(*) AS Transaction_Count
FROM expenses
WHERE Category IN ('Bills', 'Subscriptions', 'Rent', 'Insurance', 'Utilities')
GROUP BY Category, Month_Number
HAVING COUNT(*) > 1 -- Indicates multiple occurrences in a month number
ORDER BY Category, Month_Number;

-- 10. How much cashback or rewards were earned in each month?
SELECT STRFTIME('%Y-%m', Date) AS Month, SUM(Cashback) AS Total_Cashback_Earned
FROM expenses
GROUP BY Month
ORDER BY Month;

-- 11. How has your overall spending changed over time (e.g., increasing, decreasing, remaining stable)?
-- (This is best visualized as a line chart using the results of Query 7 or a similar query)
SELECT STRFTIME('%Y-%m', Date) AS Month, SUM(Amount_Paid) AS Total_Monthly_Spending
FROM expenses
GROUP BY Month
ORDER BY Month;

-- 12. What are the typical costs associated with different types of travel (e.g., flights, accommodation, transportation)?
-- Note: This assumes 'Travel' or 'Transportation' categories. More granular sub-categories would improve insight.
SELECT Category, AVG(Amount_Paid) AS Average_Cost
FROM expenses
WHERE Category LIKE '%Travel%' OR Category = 'Transportation'
GROUP BY Category
ORDER BY Average_Cost DESC;

-- 13. Are there any patterns in grocery spending (e.g., higher spending on weekends, increased spending during specific seasons)?
-- Weekly Pattern (0=Sunday, 6=Saturday)
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
ORDER BY Day_of_Week; -- Order by day number (0-6) for consistency in charts

-- Monthly/Seasonal Pattern
SELECT STRFTIME('%Y-%m', Date) AS Month, SUM(Amount_Paid) AS Monthly_Grocery_Spending
FROM expenses
WHERE Category = 'Groceries'
GROUP BY Month
ORDER BY Month;

-- 14. Define High and Low Priority Categories
-- (This is an interpretive insight, not a direct query. Based on analysis of spending, essential vs. discretionary).
-- High Priority (Essential/High Spend): Rent, Bills, Groceries, Transportation, Insurance, Utilities.
-- Low Priority (Discretionary/Lower Spend): Entertainment, Shopping, Gifts, Personal Care, Miscellaneous, Food & Dining.

-- 15. Which category contributes the highest percentage of the total spending?
SELECT
    Category,
    SUM(Amount_Paid) AS Category_Spending,
    (SUM(Amount_Paid) * 100.0 / (SELECT SUM(Amount_Paid) FROM expenses)) AS Percentage_of_Total
FROM expenses
GROUP BY Category
ORDER BY Percentage_of_Total DESC
LIMIT 1;

-- -------------------------------------------------------------
-- Custom Insightful Queries (1-13)
-- -------------------------------------------------------------

-- 1. Average daily spending
SELECT Date, SUM(Amount_Paid) AS Daily_Total_Spending
FROM expenses
GROUP BY Date
ORDER BY Date;

-- 2. Number of transactions per category
SELECT Category, COUNT(*) AS Transaction_Count
FROM expenses
GROUP BY Category
ORDER BY Transaction_Count DESC;

-- 3. Highest single transaction in each category
SELECT Category, MAX(Amount_Paid) AS Highest_Transaction
FROM expenses
GROUP BY Category
ORDER BY Highest_Transaction DESC;

-- 4. Days of the week with the highest overall spending
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

-- 5. Average cashback percentage per transaction (where cashback > 0)
SELECT AVG(Cashback * 100.0 / Amount_Paid) AS Avg_Cashback_Percentage
FROM expenses
WHERE Cashback > 0 AND Amount_Paid > 0;

-- 6. Top 3 spending days in the year
SELECT Date, SUM(Amount_Paid) AS Daily_Total
FROM expenses
GROUP BY Date
ORDER BY Daily_Total DESC
LIMIT 3;

-- 7. Comparison of 'Cash' vs. 'Online' spending trends over months
SELECT STRFTIME('%Y-%m', Date) AS Month, Payment_Mode, SUM(Amount_Paid) AS Monthly_Spending
FROM expenses
GROUP BY Month, Payment_Mode
ORDER BY Month, Payment_Mode;

-- 8. Categories with no cashback received (to identify potential missed savings)
SELECT DISTINCT Category
FROM expenses
WHERE Cashback = 0 AND Amount_Paid > 0;

-- 9. Monthly average transaction value
SELECT STRFTIME('%Y-%m', Date) AS Month, AVG(Amount_Paid) AS Average_Transaction_Value
FROM expenses
GROUP BY Month
ORDER BY Month;

-- 10. Total Spending on 'Food & Dining' by Day of Week
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

-- 11. Percentage of transactions with cashback
SELECT
    CAST(SUM(CASE WHEN Cashback > 0 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS Percentage_Transactions_With_Cashback
FROM expenses;

-- 12. Total spending for the first 6 months vs. last 6 months
SELECT
    SUM(CASE WHEN STRFTIME('%m', Date) BETWEEN '01' AND '06' THEN Amount_Paid ELSE 0 END) AS H1_Spending,
    SUM(CASE WHEN STRFTIME('%m', Date) BETWEEN '07' AND '12' THEN Amount_Paid ELSE 0 END) AS H2_Spending
FROM expenses;

-- 13. Monthly Spending by Category (for stacked bar chart visualization)
SELECT STRFTIME('%Y-%m', Date) AS Month, Category, SUM(Amount_Paid) AS Monthly_Category_Spending
FROM expenses
GROUP BY Month, Category
ORDER BY Month, Category;