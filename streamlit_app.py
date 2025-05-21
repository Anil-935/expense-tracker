import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import csv

# ✅ Must come first
st.set_page_config(page_title="Expense Tracker", layout="wide")

# --- Add Expense Form ---
st.sidebar.header("➕ Add New Expense")

with st.sidebar.form("expense_form"):
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    category = st.text_input("Category (e.g. Food, Travel)")
    date = st.date_input("Date", value=datetime.today())
    note = st.text_input("Note (optional)")
    submit = st.form_submit_button("Add Expense")

if submit:
    new_expense = [amount, category, date.strftime('%Y-%m-%d'), note]
    with open("expenses.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(new_expense)
    st.success("✅ Expense added successfully!")

# --- Title ---
st.title("💸 Personal Expense Tracker")
st.write("Track, view, and visualize your expenses in a clean interface.")

# --- Load Data ---
try:
    df = pd.read_csv("expenses.csv", names=["Amount", "Category", "Date", "Note"])
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
except FileNotFoundError:
    st.error("No data found. Add expenses using the form.")
    st.stop()

# --- Filters ---
st.sidebar.header("🔎 Filter Expenses")
category_filter = st.sidebar.selectbox("Filter by Category", options=["All"] + sorted(df["Category"].dropna().unique().tolist()))
date_range = st.sidebar.date_input("Date Range", [])

filtered_df = df.copy()
if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]
if len(date_range) == 2:
    filtered_df = filtered_df[(filtered_df["Date"] >= pd.to_datetime(date_range[0])) &
                              (filtered_df["Date"] <= pd.to_datetime(date_range[1]))]

# --- View Filtered Data ---
st.subheader("📄 Filtered Expenses")
st.dataframe(filtered_df)

# --- Edit/Delete Entries ---
st.subheader("✏️ Edit or 🗑️ Delete Expense Entry")
edit_df = pd.read_csv("expenses.csv", names=["Amount", "Category", "Date", "Note"])
edit_df = edit_df.reset_index().rename(columns={"index": "Row"})
st.dataframe(edit_df)

selected_row = st.number_input("Select Row Number to Edit/Delete", min_value=0, max_value=len(edit_df)-1, step=1)
edit_mode = st.radio("Action", ["Edit", "Delete"])

if edit_mode == "Edit":
    st.markdown("### 📝 Edit Selected Entry")
    new_amount = st.number_input("Amount", value=float(edit_df.loc[selected_row, "Amount"]))
    new_category = st.text_input("Category", value=edit_df.loc[selected_row, "Category"])
    new_date = st.date_input("Date", pd.to_datetime(edit_df.loc[selected_row, "Date"]))
    new_note = st.text_input("Note", value=edit_df.loc[selected_row, "Note"])

    if st.button("✅ Save Changes"):
        edit_df.at[selected_row, "Amount"] = new_amount
        edit_df.at[selected_row, "Category"] = new_category
        edit_df.at[selected_row, "Date"] = new_date.strftime('%Y-%m-%d')
        edit_df.at[selected_row, "Note"] = new_note
        edit_df.drop("Row", axis=1).to_csv("expenses.csv", index=False, header=False)
        st.success("✔️ Entry updated successfully!")

elif edit_mode == "Delete":
    if st.button("🗑️ Confirm Delete"):
        deleted_row = edit_df.loc[[selected_row]].drop("Row", axis=1)
        deleted_row["Deleted_At"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Append to deleted_expenses.csv
        try:
            pd.read_csv("deleted_expenses.csv")  # check if file exists
        except FileNotFoundError:
            deleted_row.to_csv("deleted_expenses.csv", index=False)
        else:
            deleted_row.to_csv("deleted_expenses.csv", mode='a', header=False, index=False)

        # Remove from original
        edit_df = edit_df.drop(selected_row)
        edit_df.drop("Row", axis=1).to_csv("expenses.csv", index=False, header=False)
        st.warning("❌ Entry deleted and logged to 'deleted_expenses.csv'")

# --- Restore Deleted Entries ---
with st.expander("♻️ Restore Deleted Entry"):
    try:
        deleted_df = pd.read_csv("deleted_expenses.csv")
        deleted_df = deleted_df.reset_index().rename(columns={"index": "Row"})
        st.dataframe(deleted_df)

        if not deleted_df.empty:
            row_to_restore = st.number_input(
                "Select Row Number to Restore",
                min_value=0,
                max_value=len(deleted_df) - 1,
                step=1,
                key="restore_row"
            )

            if st.button("♻️ Restore Selected Entry"):
                # Extract and clean the row
                restored_entry = deleted_df.loc[row_to_restore].drop(labels=["Row", "Deleted_At"])

                # Append to main expense log
                with open("expenses.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(restored_entry)

                # Remove restored row from deleted_expenses.csv
                deleted_df = deleted_df.drop(row_to_restore)
                deleted_df.drop("Row", axis=1).to_csv("deleted_expenses.csv", index=False)

                st.success("✅ Entry restored to expenses!")
    except FileNotFoundError:
        st.info("No deleted entries found.")

# --- Stats ---
st.subheader("📊 Summary Stats")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spent", f"₹{filtered_df['Amount'].sum():,.2f}")
col2.metric("Average Spend", f"₹{filtered_df['Amount'].mean():,.2f}")
col3.metric("Max Spend", f"₹{filtered_df['Amount'].max():,.2f}")
col4.metric("Min Spend", f"₹{filtered_df['Amount'].min():,.2f}")

# --- Visualizations ---
st.subheader("📈 Visualizations")
if not filtered_df.empty:
    category_sum = filtered_df.groupby("Category")["Amount"].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    daily_sum = filtered_df.groupby("Date")["Amount"].sum()
    daily_sum.plot(kind="line", marker='o', ax=ax2)
    ax2.set_title("Daily Spending Trend")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Amount")
    plt.xticks(rotation=45)
    st.pyplot(fig2)
else:
    st.warning("No data to show graphs for the selected filters.")

# --- Export to Excel ---
st.subheader("📤 Export Expenses to Excel")

if st.button("📥 Download as Excel"):
    export_df = df.copy()
    export_df.to_excel("exported_expenses.xlsx", index=False)
    with open("exported_expenses.xlsx", "rb") as f:
        st.download_button("📥 Click to Download", f, file_name="expenses.xlsx")
