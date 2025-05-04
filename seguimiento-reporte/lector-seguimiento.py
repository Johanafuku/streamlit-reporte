import streamlit as st
import pandas as pd
import copy

def get_values(col):
    return sorted(st.session_state["user"][col].dropna().unique())

def update_report():
    filters = {
        "MBL": st.session_state.get("MBL"),
        "HBL": st.session_state.get("HBL"),
        "TN": st.session_state.get("TN"),
        "CLIENTE": st.session_state.get("CLIENTE"),
    }

    filtered_data = st.session_state["user"]
    for col, values in filters.items():
        if values:
            filtered_data = filtered_data[filtered_data[col].isin(values)]

    st.session_state["user-fil"] = filtered_data

st.set_page_config(
    page_title="Seguimiento embarques",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "user" not in st.session_state:
    st.session_state["user"] = pd.DataFrame()

if "user-fil" not in st.session_state:
    st.session_state["user-fil"] = pd.DataFrame()

st.header("INFORME DE SEGUIMIENTO EMBARQUES EMPRESA XXX")

# Load and merge sheets
datos = "./PRUEBA-SEGUIMIENTO.xlsx"
sheets = pd.read_excel(datos, sheet_name=["MSC", "HAPAG"])
st.session_state["user"] = pd.concat(sheets.values(), ignore_index=True)

with st.sidebar:
    with st.expander("Filters"):
        with st.form(key="filter-report"):

            client_values = get_values("CLIENTE")
            select_client = st.multiselect("CLIENTE", options=client_values, help="nombre del cliente", default=None, key="CLIENTE")
            mbl_values = get_values("MBL")
            select_mbl = st.multiselect("MBL", options=mbl_values, help="número de MBL", default=None, key="MBL")

            bal_values = get_values("HBL")
            select_bal = st.multiselect("HBL", options=bal_values, help="número de HBL", default=None, key="BAL")

            tn_values = get_values("TN")
            select_tn = st.multiselect("TN", options=tn_values, help="número de file", default=None, key="TN")

            submit = st.form_submit_button("Update")

            if submit:
                update_report()


with st.expander("Report"):
    if not st.session_state["user-fil"].empty:
        columns_to_display = ["MBL", "HBL", "CLIENTE", "COMENTARIOS"]
        filtered_columns = st.session_state["user-fil"][columns_to_display]
        st.table(filtered_columns)
    else:
        st.write("No data to display. Apply filters or load the data.")
