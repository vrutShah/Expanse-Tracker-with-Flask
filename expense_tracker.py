# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# from datetime import datetime, date
# from io import BytesIO
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors

# # --- CONFIGURATION ---
# st.set_page_config(page_title="Expense Tracker", layout="wide")
# EXPENSE_FILE = "expenses.csv"
# CATEGORY_FILE = "categories.csv"

# # --- HELPERS: DATA LOADING/SAVING ---
# def load_data():
#     if os.path.exists(EXPENSE_FILE):
#         df = pd.read_csv(EXPENSE_FILE)
#         df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y %I:%M %p", errors="coerce")
#         df = df.dropna(subset=["Date"])
#         return df
#     # FIX 1: Explicitly set dtype so .dt accessor always works on an empty DataFrame
#     df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
#     df["Date"] = pd.to_datetime(df["Date"])
#     df["Amount"] = df["Amount"].astype(float)
#     return df

# def save_data():
#     # Save with a consistent string format so load_data can re-parse it
#     df_to_save = st.session_state.expenses.copy()
#     df_to_save["Date"] = df_to_save["Date"].dt.strftime("%d-%m-%Y %I:%M %p")
#     df_to_save.to_csv(EXPENSE_FILE, index=False)

# def load_categories():
#     if os.path.exists(CATEGORY_FILE):
#         return pd.read_csv(CATEGORY_FILE)["Category"].tolist()
#     return ["Food", "Transport", "Shopping", "Utilities", "Entertainment", "Other"]

# def save_categories():
#     pd.DataFrame({"Category": st.session_state.categories}).to_csv(CATEGORY_FILE, index=False)

# # --- INITIALIZATION ---
# if "expenses" not in st.session_state:
#     st.session_state.expenses = load_data()
# if "categories" not in st.session_state:
#     st.session_state.categories = load_categories()
# if "show_form" not in st.session_state:
#     st.session_state.show_form = False

# # --- PDF GENERATION ENGINE ---
# def generate_pdf(df, fig, start, end):
#     file = "expense_report.pdf"
#     styles = getSampleStyleSheet()
#     elements = [
#         Paragraph("Expense Report", styles["Title"]),
#         Paragraph(f"Period: {start} to {end}", styles["Normal"]),
#         Spacer(1, 20),
#     ]

#     # Summary Table
#     total = df["Amount"].sum()
#     summary_data = [
#         ["Metric", "Value"],
#         ["Total Spending", f"₹{total:,.2f}"],
#         ["Transactions", str(len(df))],
#     ]
#     summary_table = Table(summary_data, colWidths=[200, 200])
#     summary_table.setStyle(
#         TableStyle([
#             ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F8BF9")),
#             ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#             ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
#             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
#         ])
#     )
#     elements.append(summary_table)
#     elements.append(Spacer(1, 20))

#     # Expense Detail Table
#     if not df.empty:
#         detail_data = [["Date", "Category", "Amount", "Description"]]
#         for _, row in df.iterrows():
#             detail_data.append([
#                 row["Date"].strftime("%d-%m-%Y"),
#                 str(row["Category"]),
#                 f"₹{row['Amount']:,.2f}",
#                 str(row["Description"]),
#             ])
#         detail_table = Table(detail_data, colWidths=[100, 100, 80, 220])
#         detail_table.setStyle(
#             TableStyle([
#                 ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F8BF9")),
#                 ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#                 ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#                 ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
#                 ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
#                 ("FONTSIZE", (0, 0), (-1, -1), 8),
#             ])
#         )
#         elements.append(Paragraph("Expense Details", styles["Heading2"]))
#         elements.append(Spacer(1, 10))
#         elements.append(detail_table)
#         elements.append(Spacer(1, 20))

#     # FIX 2: kaleido is required for fig.write_image; wrap in try/except gracefully
#     try:
#         img_data = BytesIO()
#         fig.write_image(img_data, format="png", width=700, height=350)
#         img_data.seek(0)
#         elements.append(Paragraph("Spending Chart", styles["Heading2"]))
#         elements.append(Spacer(1, 10))
#         elements.append(Image(img_data, width=450, height=225))
#     except Exception:
#         elements.append(
#             Paragraph(
#                 "⚠ Chart image could not be embedded. Install 'kaleido' via pip to enable this.",
#                 styles["Normal"],
#             )
#         )

#     doc = SimpleDocTemplate(file, pagesize=A4)
#     doc.build(elements)
#     return file

# # --- UI: SIDEBAR ---
# with st.sidebar:
#     st.title("⚙️ Settings")

#     # FIX 3: Working Add Expense form using session_state toggle
#     if st.button("➕ Add Expense"):
#         st.session_state.show_form = not st.session_state.show_form

#     if st.session_state.show_form:
#         with st.form("add_expense_form", clear_on_submit=True):
#             st.subheader("New Expense")
#             exp_date = st.date_input("Date", value=date.today())
#             exp_time = st.time_input("Time", value=datetime.now().time())
#             exp_category = st.selectbox("Category", st.session_state.categories)
#             exp_amount = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
#             exp_description = st.text_input("Description")
#             submitted = st.form_submit_button("Save Expense")

#             if submitted:
#                 exp_datetime = datetime.combine(exp_date, exp_time)
#                 new_row = pd.DataFrame([{
#                     "Date": exp_datetime,
#                     "Category": exp_category,
#                     "Amount": float(exp_amount),
#                     "Description": exp_description,
#                 }])
#                 new_row["Date"] = pd.to_datetime(new_row["Date"])
#                 st.session_state.expenses = pd.concat(
#                     [st.session_state.expenses, new_row], ignore_index=True
#                 )
#                 save_data()
#                 st.session_state.show_form = False
#                 st.success("Expense added!")
#                 st.rerun()

#     st.divider()
#     st.subheader("Manage Categories")
#     cat_to_add = st.text_input("New Category")
#     if st.button("Add Category"):
#         if cat_to_add and cat_to_add not in st.session_state.categories:
#             st.session_state.categories.append(cat_to_add)
#             save_categories()
#             st.success(f"Category '{cat_to_add}' added!")
#         elif not cat_to_add:
#             st.warning("Please enter a category name.")
#         else:
#             st.warning("Category already exists.")

#     st.divider()
#     st.subheader("Danger Zone")
#     if st.button("🗑️ Clear All Expenses", type="primary"):
#         st.session_state.expenses = load_data().__class__(
#             columns=["Date", "Category", "Amount", "Description"]
#         )
#         st.session_state.expenses["Date"] = pd.to_datetime(st.session_state.expenses["Date"])
#         st.session_state.expenses["Amount"] = st.session_state.expenses["Amount"].astype(float)
#         save_data()
#         st.rerun()

# # --- UI: MAIN DASHBOARD ---
# st.title("💸 Expense Dashboard")

# col1, col2 = st.columns(2)
# with col1:
#     start_date = st.date_input("Start Date", value=date(date.today().year, date.today().month, 1))
# with col2:
#     end_date = st.date_input("End Date", value=date.today())

# # FIX 4: Safe filtering — .dt accessor is always valid now due to FIX 1
# df = st.session_state.expenses
# if not df.empty:
#     mask = (df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)
#     filtered_df = df.loc[mask].copy()
# else:
#     filtered_df = df.copy()

# # KPI metrics
# total_spend = filtered_df["Amount"].sum()
# num_txns = len(filtered_df)
# avg_spend = filtered_df["Amount"].mean() if num_txns > 0 else 0.0
# top_category = (
#     filtered_df.groupby("Category")["Amount"].sum().idxmax()
#     if num_txns > 0 else "N/A"
# )

# k1, k2, k3, k4 = st.columns(4)
# k1.metric("Total Spending", f"₹{total_spend:,.2f}")
# k2.metric("Transactions", num_txns)
# k3.metric("Avg per Transaction", f"₹{avg_spend:,.2f}")
# k4.metric("Top Category", top_category)

# st.divider()
# st.subheader("📋 Expenses")
# st.dataframe(
#     filtered_df.assign(Date=filtered_df["Date"].dt.strftime("%d-%m-%Y %I:%M %p")),
#     use_container_width=True,
# )

# # --- Analytics Engine ---
# st.divider()
# st.subheader("📊 Analytics")

# CHART_TYPES = ["Donut", "Bar", "Line", "Treemap", "Box Plot", "Sunburst"]
# chart_type = st.selectbox("Select Graph", CHART_TYPES)

# def get_fig(df, ctype):
#     if df.empty:
#         return px.scatter(title="No data available for the selected period.")
#     if ctype == "Donut":
#         return px.pie(df, values="Amount", names="Category", hole=0.4, title="Spending by Category")
#     if ctype == "Bar":
#         return px.bar(df, x="Category", y="Amount", color="Category", title="Spending by Category")
#     if ctype == "Line":
#         return px.line(df.sort_values("Date"), x="Date", y="Amount", color="Category", title="Spending Over Time")
#     if ctype == "Treemap":
#         return px.treemap(df, path=["Category", "Description"], values="Amount", title="Expense Treemap")
#     if ctype == "Box Plot":
#         return px.box(df, x="Category", y="Amount", title="Spending Distribution by Category")
#     if ctype == "Sunburst":
#         return px.sunburst(df, path=["Category", "Description"], values="Amount", title="Expense Sunburst")
#     return px.scatter(title="Unknown chart type")

# fig = get_fig(filtered_df, chart_type)
# st.plotly_chart(fig, use_container_width=True)

# # --- PDF Report ---
# st.divider()
# if st.button("📄 Generate PDF Report"):
#     if filtered_df.empty:
#         st.warning("No data in the selected date range to generate a report.")
#     else:
#         with st.spinner("Generating PDF..."):
#             pdf_path = generate_pdf(filtered_df, fig, start_date, end_date)
#         with open(pdf_path, "rb") as f:
#             st.download_button(
#                 label="⬇️ Download PDF",
#                 data=f,
#                 file_name=f"expense_report_{start_date}_{end_date}.pdf",
#                 mime="application/pdf",
#             )
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os
from datetime import datetime, date
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# --- CONFIGURATION ---
st.set_page_config(page_title="Expense Tracker", layout="wide")
EXPENSE_FILE = "expenses.csv"
CATEGORY_FILE = "categories.csv"

# --- HELPERS: DATA LOADING/SAVING ---
def load_data():
    if os.path.exists(EXPENSE_FILE):
        df = pd.read_csv(EXPENSE_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y %I:%M %p", errors="coerce")
        df = df.dropna(subset=["Date"])
        return df
    # FIX 1: Explicitly set dtype so .dt accessor always works on an empty DataFrame
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df["Date"] = pd.to_datetime(df["Date"])
    df["Amount"] = df["Amount"].astype(float)
    return df

def save_data():
    # Save with a consistent string format so load_data can re-parse it
    df_to_save = st.session_state.expenses.copy()
    df_to_save["Date"] = df_to_save["Date"].dt.strftime("%d-%m-%Y %I:%M %p")
    df_to_save.to_csv(EXPENSE_FILE, index=False)

def load_categories():
    if os.path.exists(CATEGORY_FILE):
        return pd.read_csv(CATEGORY_FILE)["Category"].tolist()
    return ["Food", "Transport", "Shopping", "Utilities", "Entertainment", "Other"]

def save_categories():
    pd.DataFrame({"Category": st.session_state.categories}).to_csv(CATEGORY_FILE, index=False)

# --- INITIALIZATION ---
if "expenses" not in st.session_state:
    st.session_state.expenses = load_data()
if "categories" not in st.session_state:
    st.session_state.categories = load_categories()
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# --- PDF GENERATION ENGINE ---
def generate_pdf(df, fig, start, end):
    file = "expense_report.pdf"
    styles = getSampleStyleSheet()
    elements = [
        Paragraph("Expense Report", styles["Title"]),
        Paragraph(f"Period: {start} to {end}", styles["Normal"]),
        Spacer(1, 20),
    ]

    # Summary Table
    total = df["Amount"].sum()
    summary_data = [
        ["Metric", "Value"],
        ["Total Spending", f"₹{total:,.2f}"],
        ["Transactions", str(len(df))],
    ]
    summary_table = Table(summary_data, colWidths=[200, 200])
    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F8BF9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
        ])
    )
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # Expense Detail Table
    if not df.empty:
        detail_data = [["Date", "Category", "Amount", "Description"]]
        for _, row in df.iterrows():
            detail_data.append([
                row["Date"].strftime("%d-%m-%Y"),
                str(row["Category"]),
                f"₹{row['Amount']:,.2f}",
                str(row["Description"]),
            ])
        detail_table = Table(detail_data, colWidths=[100, 100, 80, 220])
        detail_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F8BF9")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ])
        )
        elements.append(Paragraph("Expense Details", styles["Heading2"]))
        elements.append(Spacer(1, 10))
        elements.append(detail_table)
        elements.append(Spacer(1, 20))

    # Force full-color rendering: set white template + explicit colorway before export
    try:
        color_fig = fig
        color_fig.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="black"),
            colorway=[
                "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
                "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52",
            ],
        )
        img_data = BytesIO()
        pio.write_image(color_fig, img_data, format="png", width=900, height=450, scale=2)
        img_data.seek(0)
        elements.append(Paragraph("Spending Chart", styles["Heading2"]))
        elements.append(Spacer(1, 10))
        elements.append(Image(img_data, width=480, height=240))
    except Exception as e:
        elements.append(
            Paragraph(
                f"Chart image could not be embedded ({e}). Install kaleido via pip to enable this.",
                styles["Normal"],
            )
        )

    doc = SimpleDocTemplate(file, pagesize=A4)
    doc.build(elements)
    return file

# --- UI: SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")

    # FIX 3: Working Add Expense form using session_state toggle
    if st.button("➕ Add Expense"):
        st.session_state.show_form = not st.session_state.show_form

    if st.session_state.show_form:
        with st.form("add_expense_form", clear_on_submit=True):
            st.subheader("New Expense")
            exp_date = st.date_input("Date", value=date.today())
            exp_time = st.time_input("Time", value=datetime.now().time())
            exp_category = st.selectbox("Category", st.session_state.categories)
            exp_amount = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
            exp_description = st.text_input("Description")
            submitted = st.form_submit_button("Save Expense")

            if submitted:
                exp_datetime = datetime.combine(exp_date, exp_time)
                new_row = pd.DataFrame([{
                    "Date": exp_datetime,
                    "Category": exp_category,
                    "Amount": float(exp_amount),
                    "Description": exp_description,
                }])
                new_row["Date"] = pd.to_datetime(new_row["Date"])
                st.session_state.expenses = pd.concat(
                    [st.session_state.expenses, new_row], ignore_index=True
                )
                save_data()
                st.session_state.show_form = False
                st.success("Expense added!")
                st.rerun()

    st.divider()
    st.subheader("Manage Categories")
    cat_to_add = st.text_input("New Category")
    if st.button("Add Category"):
        if cat_to_add and cat_to_add not in st.session_state.categories:
            st.session_state.categories.append(cat_to_add)
            save_categories()
            st.success(f"Category '{cat_to_add}' added!")
        elif not cat_to_add:
            st.warning("Please enter a category name.")
        else:
            st.warning("Category already exists.")

    st.divider()
    st.subheader("Danger Zone")
    if st.button("🗑️ Clear All Expenses", type="primary"):
        st.session_state.expenses = load_data().__class__(
            columns=["Date", "Category", "Amount", "Description"]
        )
        st.session_state.expenses["Date"] = pd.to_datetime(st.session_state.expenses["Date"])
        st.session_state.expenses["Amount"] = st.session_state.expenses["Amount"].astype(float)
        save_data()
        st.rerun()

# --- UI: MAIN DASHBOARD ---
st.title("💸 Expense Dashboard")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=date(date.today().year, date.today().month, 1))
with col2:
    end_date = st.date_input("End Date", value=date.today())

# FIX 4: Safe filtering — .dt accessor is always valid now due to FIX 1
df = st.session_state.expenses
if not df.empty:
    mask = (df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)
    filtered_df = df.loc[mask].copy()
else:
    filtered_df = df.copy()

# KPI metrics
total_spend = filtered_df["Amount"].sum()
num_txns = len(filtered_df)
avg_spend = filtered_df["Amount"].mean() if num_txns > 0 else 0.0
top_category = (
    filtered_df.groupby("Category")["Amount"].sum().idxmax()
    if num_txns > 0 else "N/A"
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Spending", f"₹{total_spend:,.2f}")
k2.metric("Transactions", num_txns)
k3.metric("Avg per Transaction", f"₹{avg_spend:,.2f}")
k4.metric("Top Category", top_category)

st.divider()
st.subheader("📋 Expenses")
st.dataframe(
    filtered_df.assign(Date=filtered_df["Date"].dt.strftime("%d-%m-%Y %I:%M %p")),
    use_container_width=True,
)

# --- Analytics Engine ---
st.divider()
st.subheader("📊 Analytics")

CHART_TYPES = ["Donut", "Bar", "Line", "Treemap", "Box Plot", "Sunburst"]
chart_type = st.selectbox("Select Graph", CHART_TYPES)

CHART_COLORS = ["#636EFA","#EF553B","#00CC96","#AB63FA","#FFA15A","#19D3F3","#FF6692","#B6E880","#FF97FF","#FECB52"]

def get_fig(df, ctype):
    if df.empty:
        return px.scatter(title="No data available for the selected period.")
    if ctype == "Donut":
        return px.pie(df, values="Amount", names="Category", hole=0.4, title="Spending by Category", color_discrete_sequence=CHART_COLORS)
    if ctype == "Bar":
        return px.bar(df, x="Category", y="Amount", color="Category", title="Spending by Category", color_discrete_sequence=CHART_COLORS)
    if ctype == "Line":
        return px.line(df.sort_values("Date"), x="Date", y="Amount", color="Category", title="Spending Over Time", color_discrete_sequence=CHART_COLORS)
    if ctype == "Treemap":
        return px.treemap(df, path=["Category", "Description"], values="Amount", title="Expense Treemap", color_discrete_sequence=CHART_COLORS)
    if ctype == "Box Plot":
        return px.box(df, x="Category", y="Amount", title="Spending Distribution by Category", color_discrete_sequence=CHART_COLORS)
    if ctype == "Sunburst":
        return px.sunburst(df, path=["Category", "Description"], values="Amount", title="Expense Sunburst", color_discrete_sequence=CHART_COLORS)
    return px.scatter(title="Unknown chart type")

fig = get_fig(filtered_df, chart_type)
st.plotly_chart(fig, use_container_width=True)

# --- PDF Report ---
st.divider()
if st.button("📄 Generate PDF Report"):
    if filtered_df.empty:
        st.warning("No data in the selected date range to generate a report.")
    else:
        with st.spinner("Generating PDF..."):
            pdf_path = generate_pdf(filtered_df, fig, start_date, end_date)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name=f"expense_report_{start_date}_{end_date}.pdf",
                mime="application/pdf",
            )