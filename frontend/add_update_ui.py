import streamlit as st
import requests
from datetime import date

API_BASE_URL = "https://expense-tracker-api-8b9m.onrender.com/"  # change port if your backend runs on another one
CATEGORIES = ["Rent", "Food", "Shopping", "Entertainment", "Other"]
NUM_ROWS = 5


def fetch_expenses_for_date(selected_date: date):
    """Call GET /expenses/{date} and return a list of expenses."""
    try:
        url = f"{API_BASE_URL}/expenses/{selected_date.isoformat()}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        return []
    except requests.RequestException as exc:
        st.error(f"Failed to load expenses for {selected_date}: {exc}")
        return []


def save_expenses_for_date(selected_date: date, expenses: list):
    """Call POST /expenses/{date} to save expense rows."""
    try:
        url = f"{API_BASE_URL}/expenses/{selected_date.isoformat()}"
        resp = requests.post(url, json=expenses, timeout=10)
        resp.raise_for_status()
        return True, "Expenses saved successfully."
    except requests.RequestException as exc:
        return False, f"Failed to save expenses: {exc}"


def init_expense_row_state():
    """Ensure expense row widget state exists."""
    if not st.session_state.get("expense_rows_initialized"):
        for i in range(NUM_ROWS):
            st.session_state[f"amount_{i}"] = 0.0
            st.session_state[f"category_{i}"] = CATEGORIES[0]
            st.session_state[f"notes_{i}"] = ""
        st.session_state["expense_rows_initialized"] = True


def populate_expense_rows_from_backend(expenses: list):
    """Populate up to NUM_ROWS rows from backend data into session_state."""
    for i in range(NUM_ROWS):
        if i < len(expenses):
            row = expenses[i] or {}
            st.session_state[f"amount_{i}"] = float(row.get("amount", 0.0) or 0.0)
            st.session_state[f"category_{i}"] = row.get("category", CATEGORIES[0])
            st.session_state[f"notes_{i}"] = row.get("notes", "") or ""
        else:
            st.session_state[f"amount_{i}"] = 0.0
            st.session_state[f"category_{i}"] = CATEGORIES[0]
            st.session_state[f"notes_{i}"] = ""


def show_add_update_section():
    """Add / update expenses for a specific date."""
    st.markdown(
        """
        <div style='text-align:center;'>
            <h3 style='font-weight:800;'>➕ Add / Update Expenses</h3>
            <p class='section-subtitle'>
                Pick a day and jot down what you spent.
                Rows with amount <strong>0</strong> will be ignored when you save.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    init_expense_row_state()

    today = date.today()
    selected_date = st.date_input(
        "Select date to edit", value=today, key="add_update_date"
    )

    # Load existing expenses when the date changes
    if (
        "loaded_date" not in st.session_state
        or st.session_state["loaded_date"] != selected_date
    ):
        with st.spinner("Loading expenses for selected date..."):
            existing_expenses = fetch_expenses_for_date(selected_date)
        populate_expense_rows_from_backend(existing_expenses)
        st.session_state["loaded_date"] = selected_date

    st.write("")

    st.markdown("#### Expenses for the day")

    st.write("")



    header_cols = st.columns([1, 1, 2])
    header_cols[0].markdown("**Amount**")
    header_cols[1].markdown("**Category**")
    header_cols[2].markdown("**Notes**")

    for i in range(NUM_ROWS):
        col1, col2, col3 = st.columns([1, 1, 2])
        col1.number_input(
            "Amount",
            key=f"amount_{i}",
            min_value=0.0,
            step=10.0,
            label_visibility="collapsed",
        )
        col2.selectbox(
            "Category",
            options=CATEGORIES,
            key=f"category_{i}",
            label_visibility="collapsed",
        )
        col3.text_input(
            "Notes",
            key=f"notes_{i}",
            placeholder="Optional",
            label_visibility="collapsed",
        )

    st.markdown("")
    if st.button("Save expenses for this date"):
        expenses_to_save = []
        for i in range(NUM_ROWS):
            amount = st.session_state.get(f"amount_{i}", 0.0) or 0.0
            if amount > 0:
                cat = st.session_state.get(f"category_{i}", CATEGORIES[0])
                notes = st.session_state.get(f"notes_{i}", "") or ""
                expenses_to_save.append(
                    {"amount": float(amount), "category": cat, "notes": notes}
                )

        if not expenses_to_save:
            st.warning(
                "No rows with a positive amount. "
                "Enter at least one expense before saving."
            )
        else:
            with st.spinner("Saving expenses..."):
                ok, msg = save_expenses_for_date(selected_date, expenses_to_save)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)
