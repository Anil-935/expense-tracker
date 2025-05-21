import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    try:
        df = pd.read_csv('expenses.csv', names=["Amount", "Category", "Date", "Note"])
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Amount', 'Date', 'Category'])
        return df
    except FileNotFoundError:
        print("⚠️ 'expenses.csv' not found. Run main.py to add expenses first.")
        return pd.DataFrame()

def plot_by_category(df):
    category_totals = df.groupby('Category')['Amount'].sum()
    category_totals.plot.pie(autopct='%1.1f%%', startangle=90)
    plt.title('Spending by Category')
    plt.ylabel('')
    plt.show()

def plot_by_date(df):
    date_totals = df.groupby('Date')['Amount'].sum()
    date_totals.plot(kind='line', marker='o')
    plt.title('Spending Over Time')
    plt.xlabel('Date')
    plt.ylabel('Amount Spent')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("📊 Generating your expense dashboard...")
    df = load_data()
    if not df.empty:
        plot_by_category(df)
        plot_by_date(df)
