import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Expense Tracker",layout="wide")
st.title("Expense tracker")

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "balance" not in st.session_state:
    st.session_state.balance =0.0

if "last_action" not in st.session_state:
    st.session_state.last_action = "App started"

st.subheader("Add Transaction")

col1,col2,col3,col4 =st.columns(4)

with col1:
    t_type = st.selectbox("Type",["Income","Expense"])

with col2:
    category=st.selectbox("Category",["Salary","Shopping","Food","Bills","Other"])

with col3:
    amount =st.number_input("Amount",format="%.2f")

with col4:
    description =st.text_input("Description")

if st.button("Add Transaction"):
    if amount > 0 and description.strip()!="":
        transaction ={
            "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type":t_type,
            "category":category,
            "amount":amount,
            "description":description
        }
        st.session_state.transactions.append(transaction)

        if t_type == "Income":
            st.session_state.balance += amount
        else:
            st.session_state.balance -= amount
        st.success("Transaction completed")
        st.session_state.last_action =f"{t_type} Added"
        st.rerun()
    else:
        st.warning("data is invalid")

# current balance
st.subheader("Current Balance")

if st.session_state.balance >=0:
    st.success(st.session_state.balance)
else:
    st.error(st.session_state.balance)

# filter part

st.subheader("Filter Transaction")
filter_type=st.selectbox("Filter By Transaction",["All","Income","Expense"])
filtered_transaction =[]

for t in st.session_state.transactions:
    if filter_type == "All":
        filtered_transaction.append(t)
    if t["type"] == filter_type:
        filtered_transaction.append(t)

st.subheader("Transaction history")

if filtered_transaction:
    for i, t in enumerate(filtered_transaction, start=1):
        st.write(f"{i}. {t['time']} | {t['type']} | {t['category']} | {t['amount']} | {t['description']}")


else:
    st.info("No transaction yet")

# delete and reset all
col5,col6=st.columns(2)

with col5:
    transaction_options = [
        f"{i + 1}. {t['category']} - ₹{t['amount']} ({t['description']})"
        for i, t in enumerate(st.session_state.transactions)
    ]

    selected_transaction = st.selectbox(
        "Select transaction to delete",
        transaction_options
    )

    if st.button("Delete Selected Transaction"):
        index_to_delete = transaction_options.index(selected_transaction)
        deleted = st.session_state.transactions.pop(index_to_delete)
        st.success("Transaction deleted successfully!")

    else:
     st.info("No transactions yet.")
    # if st.button("Delete Last transaction"):
    #     if st.session_state.transactions:
    #         last =st.session_state.transactions.pop()
    #         if last["type"] == "Income":
    #             st.session_state.balance -= last["amount"]
    #         else:
    #             st.session_state.balance += last["amount"]
    #
    #         st.success("last transaction deleted")
    #         st.session_state.last_action ="last transaction deleted"
    #         st.rerun()

with col6:
    if st.button("Reset all"):
        st.session_state.transactions =[]
        st.session_state.balance =0.0
        st.session_state.last_action = "Data reset"
        st.rerun()

st.subheader("last action")
st.write(st.session_state.last_action)

with st.expander("view all session"):
    st.write(st.session_state)