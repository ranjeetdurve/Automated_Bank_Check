import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

st.markdown("""
<style>
.big-text{ background-color: #f0f0f0;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


st.title('Automated Bank Check Processor')
st.sidebar.header("Project: Bank Check")
page = st.sidebar.radio("Go To:", ["Home", "Upload Check", "Data Preview", "Data Summary", "Data Plot", 'Bar Chart'])


if "df" not in st.session_state:
    st.session_state.df = None


if page == "Home":
    st.write("Welcome to the Automated Bank Check Processor")
    st.info('It works on Bank Check and describe details of Bank Check to "Bank Name\n, Account Name, Account Number, Amount and Date"')
    st.info("I am Ranjeet Kumar and I am a Passionate Software Engineer.\n I work on Shamgar Software Solution as a Data Science Intern.")
    st.write("It works with the help of friends which has data to secure in Backend")
    

    with st.form("form"):
        Rame = st.text_input("name")
        Roll = st.text_input("class")
        Contact = st.text_input("contact numbar")
        Email = st.text_input("Email")
        Subject = st.selectbox("subject", ["maths", "Science", "English"])
        st.form_submit_button("Submit")


elif page == "Upload Check":
    uploaded_file = st.file_uploader("Choose a csv file", type = ["csv"])
    if uploaded_file is not None:
        try:
            df = load_csv(uploaded_file)
            st.session_state.df = df
            st.success("File Uploaded and stored in session")
        except Exception as e:
            st.error(f"Could not read CSV: {e}")

    else:
        st.info("No file uploaded yet")


elif page =="Data Preview":
    if st.session_state.df is None:
        st.warning("Please upload a CSV file(upload Check).")
    else:
        st.subheader("Data Preview(first 100 words)")
        st.dataframe(st.session_state.df.head(100))


elif page == 'Data Summary':
    if st.session_state.df is None:
        st.warning("Please upload a CSV first (upload check).")
    else:
        st.subheader(" Data Summary")
        st.dataframe(st.session_state.df.describe(include='all').transpose())

        # 🔥 SEND DATA TO BACKEND BUTTON
        if st.button("Send to Backend"):
            import requests

            response = requests.post(
                "http://127.0.0.1:8000/process",
                json=st.session_state.df.to_dict(orient="records")
            )

            st.subheader("Response from Backend")
            st.write(response.json())


elif page == "Data Plot":
    if st.session_state.df is None:
        st.warning('Please upload a CSV first (Upload Check).')
    else:
        df = st.session_state.df.copy()
        st.subheader("Filter data (optional)")
        columns = df.columns.tolist()
        col_to_filter = st.selectbox("Select column to filter by (or pck None)", [None] + columns)
        if col_to_filter:
            unique_vals = df[col_to_filter].dropna().tolist()
            if len(unique_vals) > 100:
                filter_val = st.text_input(f"Enter the value to filter {col_to_filter} by (exact match)")
                if filter_val:
                    filtered = df[df[col_to_filter].astype(str) == filter_val]
                else:
                    filtered = df
            else:
                filter_val = st.selectbox(f"Select value in {col_to_filter}", [None] + unique_vals)
                filtered = df if filter_val is None else df[df[col_to_filter] == filter_val]
        else:
            filtered = df

        if filtered.empty:
            st.info("No rows match that filter. Try a different filter.")
        else:
            st.write(f"{len(filtered)} rows match the filter.")
            st.dataframe(filtered.head(50))

            st.subheader("Plot Data")
            x_col = st.selectbox("Select x-axis column", filtered.columns.tolist(), key = "xcol")
            numeric_cols = filtered.select_dtypes(include = 'number').columns.tolist()
            if not numeric_cols:
                st.warning("No numeric columns available for plotting. Convert a column to numeric first.")
            else:
                y_col = st.selectbox("Select y-axis column(numeric)", numeric_cols, key="ycol")
                if st.button("Generative Plot"):
                    try:
                        plot_df = filtered.copy()
                        try:
                            plot_df[x_col] = pd.to_datetime(plot_df[x_col])
                            plot_df = plot_df.sort_values(x_col)
                        except Exception:
                            pass
                        st.line_chart(plot_df.set_index(x_col)[y_col])
                    except Exception as e:
                        st.error(f"Could not create plot: {e}")


elif page == "Bar Chart":
    if st.session_state.df is None:
        st.warning('Please upload a CSV first (Upload Check).')
    else:
        df = st.session_state.df.copy()
        st.subheader("Bar Chart Visualization")

        columns = df.columns.tolist()

        # Select categorical column (X-axis)
        cat_col = st.selectbox("Select Categorical Column (X-axis)", columns)

        # Select numeric column (Y-axis)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns available.")
        else:
            num_col = st.selectbox("Select Numeric Column (Y-axis)", numeric_cols)

            agg_option = st.selectbox(
                "Select Aggregation Function",
                ["Sum", "Mean", "Count"]
            )

            if st.button("Generate Bar Chart"):

                # Aggregate using NumPy
                if agg_option == "Sum":
                    grouped = df.groupby(cat_col)[num_col].sum()
                elif agg_option == "Mean":
                    grouped = df.groupby(cat_col)[num_col].mean()
                else:
                    grouped = df.groupby(cat_col)[num_col].count()

                st.write("Aggregated Data")
                st.dataframe(grouped)

                # -------- Matplotlib --------
                st.subheader("Matplotlib Bar Chart")
                fig, ax = plt.subplots()
                ax.bar(grouped.index.astype(str), grouped.values)
                ax.set_xlabel(cat_col)
                ax.set_ylabel(f"{agg_option} of {num_col}")
                plt.xticks(rotation=45)
                st.pyplot(fig)

                # -------- Seaborn --------
                st.subheader("Seaborn Bar Chart")
                fig2, ax2 = plt.subplots()
                sns.barplot(
                    x=grouped.index.astype(str),
                    y=grouped.values,
                    ax=ax2
                )
                ax2.set_xlabel(cat_col)
                ax2.set_ylabel(f"{agg_option} of {num_col}")
                plt.xticks(rotation=45)
                st.pyplot(fig2)
                
