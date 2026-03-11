# 💰 Vrut's Smart Expense Tracker

A modern **Expense Tracking Dashboard** built using **Streamlit, Plotly, Pandas, and ReportLab**.
This application allows users to track expenses, visualize spending patterns, manage categories, and export detailed PDF reports.

---
## 📸 Screenshot

![Dashboard Preview](assets/dashboard.png)

# 🚀 Features

### 📊 Expense Management

* Add new expenses
* Update existing transactions
* Delete transactions
* View expenses in a structured table

### 🏷 Category Management

* Add new categories
* Rename categories
* Delete categories
* Automatic update of related expenses

### 📈 Analytics Dashboard

Generate visual insights using multiple chart types:

* Donut Chart
* Bar Chart
* Line Chart
* Treemap

Charts are interactive and dynamically generated from your expense data.

### 📄 Professional PDF Reports

Export a detailed report including:

* Application logo
* Export date
* Summary statistics
* Expense chart
* Full transaction table

Perfect for sharing or record keeping.

---

# 🛠 Tech Stack

| Technology         | Purpose                |
| ------------------ | ---------------------- |
| **Streamlit**      | Frontend dashboard     |
| **Pandas**         | Data manipulation      |
| **Plotly Express** | Data visualization     |
| **ReportLab**      | PDF report generation  |
| **Kaleido**        | Chart image export     |
| **CSV Storage**    | Local data persistence |

---

# 📂 Project Structure

```
expense-tracker/
│
├── app.py                # Main Streamlit application
├── expenses.csv          # Stored expense data
├── categories.csv        # Stored categories
├── expense_tracker.png   # Application logo
├── chart.png             # Generated chart for PDF
├── expense_report.pdf    # Exported report
└── README.md             # Project documentation
```

---

# ⚙️ Installation

Clone the repository:

```
git clone https://github.com/vrutShah/expense-tracker.git
cd expense-tracker
```

Install required packages:

```
pip install streamlit pandas plotly reportlab kaleido
```

---

# ▶️ Running the Application

Start the Streamlit server:

```
streamlit run app.py
```

Then open your browser and visit:

```
http://localhost:8501
```

---

# 📊 Example Workflow

1. Add expenses from the sidebar
2. Manage or edit transactions
3. Generate analytics charts
4. Export a professional PDF report

---

# 📌 Future Improvements

Potential upgrades for the project:

* SQLite database integration
* User authentication system
* Monthly spending insights
* Budget tracking system
* Cloud deployment
* Multi-user support

---

# 👨‍💻 Author

**Vrut Shah**


---

# ⭐ If you like this project

Consider giving the repository a **star ⭐ on GitHub** to support the project.
