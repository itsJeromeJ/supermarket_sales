# Superstore Sales Dashboard

A dynamic and interactive dashboard built using **Streamlit** and **Plotly** that enables users to explore Superstore sales data across multiple dimensions like region, state, city, category, and time. The app supports file uploads and includes download options for all visualized datasets.

---

##  Project Objective

The main goal of this project is to provide a **risk-free, insightful visualization** tool for business stakeholders to:
- Analyze sales trends over time
- Identify high and low-performing regions and categories
- Detect relationships between profit, sales, and quantity
- Download custom, filtered datasets for further use

---

##  Features

1 File Upload (CSV, XLS, XLSX, TXT)  
2 Date Filtering (Start Date – End Date)  
3 Multilevel Filtering: Region ➝ State ➝ City  
4 Interactive Visualizations:
- Bar charts (Category-wise Sales)
- Pie charts (Region-wise, Segment-wise, Category-wise)
- Line chart (Time Series Sales)
- TreeMap (Region → Category → Sub-Category)
- Scatter Plot (Sales vs Profit)  
5 Pivot Table (Month-wise Sub-Category Sales)  
6 Data Previews and CSV Downloads

---

##  Technologies & Libraries Used

| Library        | Purpose                                             |
|----------------|-----------------------------------------------------|
| `streamlit`    | Web framework for creating the interactive dashboard |
| `plotly`       | Visualization (Bar, Pie, Line, TreeMap, Scatter, Table) |
| `pandas`       | Data manipulation, cleaning, and aggregation         |
| `warnings`     | To suppress unwanted warnings                        |
| `os`           | Directory operations (fallback file loading)         |

---

##  Techniques Implemented

- **File Handling**: Auto-detects and reads files based on extension.
- **Date-Based Filtering**: Uses `st.date_input` to allow dynamic time range selection.
- **Multilevel Filtering Logic**: Applies cascading filters for Region, State, and City.
- **Groupby Operations**: For summarizing sales by Category, Region, etc.
- **Pivot Table**: Created using `pandas.pivot_table()` for month-wise sales analysis.
- **Dynamic Plotting**: Generated via Plotly with interactive tooltips and styling.
- **Hierarchical TreeMap**: Visualizes nested sales data (Region > Category > Sub-Category).
- **Data Export**: Enables users to download any chart/table data as CSV.

---


