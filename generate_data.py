import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

def generate_expense_data(num_months=12, start_year=2024):
    
    fake = Faker('en_IN') 
    data = []

    categories = [
        'Groceries', 'Food & Dining', 'Transportation', 'Bills', 'Subscriptions',
        'Personal Care', 'Entertainment', 'Shopping', 'Health', 'Education',
        'Travel', 'Gifts', 'Rent', 'Utilities', 'Insurance', 'Miscellaneous'
    ]


    category_amount_ranges = {
        'Groceries': (500, 3000),
        'Food & Dining': (200, 1500),
        'Transportation': (50, 1000),
        'Bills': (1000, 8000), 
        'Subscriptions': (100, 500),
        'Personal Care': (100, 700),
        'Entertainment': (300, 1500),
        'Shopping': (500, 5000),
        'Health': (200, 2500),
        'Education': (500, 10000),
        'Travel': (1000, 15000),
        'Gifts': (200, 2000),
        'Rent': (5000, 30000), 
        'Utilities': (500, 2500), 
        'Insurance': (1000, 5000),
        'Miscellaneous': (50, 1000)
    }


    category_descriptions = {
        'Groceries': ['Supermarket run', 'Daily essentials', 'Weekly groceries', 'Vegetables & fruits'],
        'Food & Dining': ['Restaurant dinner', 'Cafe latte', 'Lunch with colleagues', 'Takeaway food', 'Snacks'],
        'Transportation': ['Bus fare', 'Fuel refill', 'Train ticket', 'Cab ride', 'Metro travel'],
        'Bills': ['Electricity bill', 'Internet bill', 'Phone bill', 'Water bill'],
        'Subscriptions': ['Netflix subscription', 'Spotify premium', 'Gym membership', 'Software license'],
        'Personal Care': ['Haircut', 'Salon visit', 'Cosmetics', 'Pharmacy purchase'],
        'Entertainment': ['Movie tickets', 'Concert entry', 'Gaming purchase', 'Books'],
        'Shopping': ['Clothes shopping', 'Electronics', 'Home decor', 'Online purchase'],
        'Health': ['Doctor visit', 'Medicines', 'Health check-up'],
        'Education': ['Course fees', 'Books for study', 'Tuition'],
        'Travel': ['Flight ticket', 'Hotel booking', 'Local sight-seeing', 'Travel insurance'],
        'Gifts': ['Birthday gift', 'Anniversary present', 'Festival gift'],
        'Rent': ['Monthly rent payment'],
        'Utilities': ['Gas bill', 'Sewage bill'],
        'Insurance': ['Health insurance premium', 'Vehicle insurance']
    }

    current_date = datetime(start_year, 1, 1)

    for _ in range(num_months):
        days_in_month = (current_date.replace(month=current_date.month % 12 + 1, day=1) - timedelta(days=1)).day \
                        if current_date.month < 12 else (current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)).day

        for day in range(1, days_in_month + 1):
            date = current_date.replace(day=day)
            num_transactions = random.choices([0, 1, 2, 3], weights=[0.1, 0.4, 0.3, 0.2], k=1)[0] 

            for _ in range(num_transactions):
                category = random.choice(categories)
                payment_mode = random.choices(['Cash', 'Online'], weights=[0.3, 0.7], k=1)[0]

                min_amt, max_amt = category_amount_ranges.get(category, (50, 2000))
                amount_paid = round(random.uniform(min_amt, max_amt), 2)

                description_list = category_descriptions.get(category, [fake.sentence(nb_words=4)])
                description = random.choice(description_list)

                cashback = 0.0
                if payment_mode == 'Online' and random.random() < 0.3: 
                    cashback_percentage = random.uniform(0.005, 0.02) 
                    cashback = round(amount_paid * cashback_percentage, 2)
                    description += f" (with {int(cashback_percentage*100)}% cashback offer)" 

                data.append([date.strftime('%Y-%m-%d'), category, payment_mode, description, amount_paid, cashback])

        current_date = current_date.replace(day=1) + timedelta(days=days_in_month) 

    df = pd.DataFrame(data, columns=['Date', 'Category', 'Payment_Mode', 'Description', 'Amount_Paid', 'Cashback'])
    return df

if __name__ == "__main__":
    print("Generating expense data for 12 months...")
    expense_df = generate_expense_data(num_months=12, start_year=2024)
    print(f"Generated {len(expense_df)} expense records.")
    print(expense_df.head())
    print(expense_df.tail())
    expense_df.to_csv('generated_expenses.csv', index=False)
    print("Data saved to generated_expenses.csv (for inspection).")