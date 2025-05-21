import csv
from datetime import datetime
import pandas as pd

def add_expense():
    amount = input("Enter amount: ")
    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    note = input("Enter a note (optional): ")

    if not date:
        date = datetime.today().strftime('%Y-%m-%d')

    with open('expenses.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([amount, category, date, note])
    print("✅ Expense added!")

def view_expenses():
    try:
        df = pd.read_csv('expenses.csv', names=['Amount', 'Category', 'Date', 'Note'])
        print("\n📄 All Expenses:\n", df)
    except FileNotFoundError:
        print("⚠️ No expenses found. Add some first.")

def filter_by_category():
    category = input("Enter category to filter: ")
    try:
        df = pd.read_csv('expenses.csv', names=['Amount', 'Category', 'Date', 'Note'])
        df_filtered = df[df['Category'].str.lower() == category.lower()]
        print(f"\n📄 Expenses in category '{category}':\n", df_filtered)
    except FileNotFoundError:
        print("⚠️ No data available.")

def summary_by_month():
    try:
        df = pd.read_csv('expenses.csv', names=['Amount', 'Category', 'Date', 'Note'])
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.strftime('%B %Y')
        summary = df.groupby('Month')['Amount'].sum()
        print("\n📆 Monthly Summary:\n", summary)
    except:
        print("⚠️ Error processing summary.")

def show_stats():
    try:
        df = pd.read_csv('expenses.csv', names=['Amount', 'Category', 'Date', 'Note'])
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        print("\n📊 Expense Statistics:")
        print("Total Spent:", df['Amount'].sum())
        print("Average Spend:", df['Amount'].mean())
        print("Max Spend:", df['Amount'].max())
        print("Min Spend:", df['Amount'].min())
    except:
        print("⚠️ Could not calculate statistics.")

def main():
    while True:
        print("\n==== Expense Tracker Menu ====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter by Category")
        print("4. Monthly Summary")
        print("5. Expense Statistics")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            filter_by_category()
        elif choice == '4':
            summary_by_month()
        elif choice == '5':
            show_stats()
        elif choice == '6':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
