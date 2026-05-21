import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="DataKnife UI", layout="wide")
st.title("🔪 DataKnife: The Python Swiss Army Knife")

# Initialize session state to store our dataframes
if 'dfs' not in st.session_state:
    st.session_state.dfs = {}

# --- SIDEBAR: LOADING DATA ---
with st.sidebar:
    st.header("1. Load Files")
    uploaded_files = st.file_uploader("Upload CSV or Excel files",
                                      type=["csv", "xlsx"],
                                      accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.dfs:
                if file.name.endswith('.csv'):
                    st.session_state.dfs[file.name] = pd.read_csv(file)
                else:
                    st.session_state.dfs[file.name] = pd.read_excel(file)
        st.success(f"Loaded {len(st.session_state.dfs)} files.")

# --- MAIN AREA: OPERATIONS ---
if not st.session_state.dfs:
    st.info("Upload files in the sidebar to get started!")
else:
    tab1, tab2, tab3, tab4 = st.tabs(["👀 View Data", "🔗 Join/Stack", "➕ Calculate", "💾 Export"])

    with tab1:
        selected_df = st.selectbox("Select a dataset to view:", list(st.session_state.dfs.keys()))
        st.dataframe(st.session_state.dfs[selected_df].head(20))
        st.write(f"**Shape:** {st.session_state.dfs[selected_df].shape}")

    with tab2:
        st.subheader("SQL-style Join")
        col1, col2 = st.columns(2)
        with col1:
            left_df = st.selectbox("Left Dataset", list(st.session_state.dfs.keys()), key="left")
            left_on = st.selectbox("Left Column (Key)", st.session_state.dfs[left_df].columns)
        with col2:
            right_df = st.selectbox("Right Dataset", list(st.session_state.dfs.keys()), key="right")
            right_on = st.selectbox("Right Column (Key)", st.session_state.dfs[right_df].columns)

        join_type = st.radio("Join Type", ["inner", "left", "right", "outer"], horizontal=True)
        new_name = st.text_input("Name for new dataset", value="joined_result")

        if st.button("Perform Join"):
            res = pd.merge(st.session_state.dfs[left_df],
                           st.session_state.dfs[right_df],
                           left_on=left_on, right_on=right_on, how=join_type)
            st.session_state.dfs[new_name] = res
            st.success(f"Created '{new_name}' with {len(res)} rows!")

    with tab3:
        st.subheader("🧮 Column Math & Comparisons")
        target_df_name = st.selectbox("Select Dataset", list(st.session_state.dfs.keys()), key="calc_target")
        df = st.session_state.dfs[target_df_name]

        operation = st.selectbox("Operation", [
            "Sum Multiple Columns (A + B + C...)",
            "Subtract Two Columns (A - B)",
            "Compare Two Columns (Are they equal?)",
            "Delta Percentage ((A - B) / B)"
        ])

        col1, col2 = st.columns(2)

        if operation == "Sum Multiple Columns (A + B + C...)":
            cols = st.multiselect("Select columns to add together", df.columns)
            new_col_name = st.text_input("New Column Name", value="total_sum")
            if st.button("Calculate Sum") and cols:
                df[new_col_name] = df[cols].sum(axis=1)
                st.success(f"✅ Added {new_col_name}")

        elif operation == "Subtract Two Columns (A - B)":
            with col1:
                col_a = st.selectbox("Column A (Source)", df.columns)
            with col2:
                col_b = st.selectbox("Column B (Subtract this)", df.columns)
            new_col_name = st.text_input("New Column Name", value="difference")
            if st.button("Calculate Difference"):
                df[new_col_name] = df[col_a] - df[col_b]
                st.success(f"✅ Added {new_col_name}")

        elif operation == "Compare Two Columns (Are they equal?)":
            with col1:
                col_a = st.selectbox("First Column", df.columns)
            with col2:
                col_b = st.selectbox("Second Column", df.columns)
            new_col_name = st.text_input("New Column Name", value="match_check")
            if st.button("Run Comparison"):
                # Returns True if they match, False if they don't
                df[new_col_name] = df[col_a] == df[col_b]
                st.success(f"✅ Comparison complete in column: {new_col_name}")

        elif operation == "Delta Percentage ((A - B) / B)":
            with col1:
                col_a = st.selectbox("Current Value (A)", df.columns)
            with col2:
                col_b = st.selectbox("Baseline Value (B)", df.columns)
            new_col_name = st.text_input("New Column Name", value="pct_change")
            if st.button("Calculate % Change"):
                df[new_col_name] = ((df[col_a] - df[col_b]) / df[col_b]) * 100
                st.success(f"✅ Added {new_col_name}")

        # Show a preview of the changes
        st.divider()
        st.write("### Preview of results:")
        st.dataframe(df.head(10))

    with tab4:
        st.subheader("Save Results")
        save_df_name = st.selectbox("Select Dataset to Save", list(st.session_state.dfs.keys()), key="save")
        save_df = st.session_state.dfs[save_df_name]

        csv = save_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"{save_df_name}.csv",
            mime='text/csv',
        )