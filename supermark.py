
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore",page_icon=":bar_icon:",layout="wide")

st.title ( ":bar_chart: Superstore dashboard")
st.markdown('<style>div.block-container{padding-right: 1rem;}</style>',unsafe_allow_html=True)

# cd "C:\Users\jerom\Desktop\model project\webApp"

f1=st.file_uploader(":file_folder: upload a file",type=(["cssv","txt","xlsx","xls"]))
if f1 is not None:
    filename=f1.name
    st.write(filename)
    df=pd.read_csv(filename,encoding="ISO-8859-1")
    
    # read the file based on its extension
    # Check file extension and read accordingly
    if filename.endswith(".csv") or filename.endswith(".txt"):
        try:
            df = pd.read_csv(f1, encoding="ISO-8859-1")
        except pd.errors.ParserError:
            st.error("Error reading the CSV file. Check the file format or delimiter.")
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        df=pd.read_csv(f1)
    else:
        st.error("Unsupported file format.")
else:
    os.chdir(r"C:\Users\jerom\Desktop\model project\webApp")
    df = pd.read_excel("Superstoredata.xls")  # Remove encoding

col1,col2=st.columns((2))
df["Order Date"]=pd.to_datetime(df["Order Date"])

#getting the main and max date
startDate=pd.to_datetime(df["Order Date"]).min()
endDate=pd.to_datetime(df["Order Date"]).max()

# date picker
with col1:
    date1=pd.to_datetime(st.date_input("start Date", startDate))

with col2:
    date2=pd.to_datetime(st.date_input("End Date", endDate))

df=df[(df["Order Date"]>=date1) & (df["Order Date"]<=date2)].copy()

# region 
st.sidebar.header("Choose your filter: ")
region=st.sidebar.multiselect("Pick your Region: ",df["Region"].unique())
if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)].copy()

# create for state 
state=st.sidebar.multiselect("pick your state: ",df2["State"].unique())

if not state:
    df3=df2.copy()
else:
    df3=df2[df2["State"].isin(state)].copy()

# for city
city=st.sidebar.multiselect("pick your city: ",df3["City"].unique())

if not city:
    df4=df3.copy()
else:
    df4=df3[df3["City"].isin(city)].copy()

# filter the data based on region , state and city
# Start with a copy of the original DataFrame
filter_df = df.copy()

# Apply region filter if selected
if region:
    filter_df = filter_df[filter_df["Region"].isin(region)]

# Apply state filter if selected, based on already filtered data by region
if state:
    filter_df = filter_df[filter_df["State"].isin(state)]

# Apply city filter if selected, based on already filtered data by region and state
if city:
    filter_df = filter_df[filter_df["City"].isin(city)]

# Display the final filtered data
st.write("Filtered Data:", filter_df)


#  category wise filtering sales
category_df=filter_df.groupby(by=["Category"],as_index=False)["Sales"].sum()

with col1:
    st.subheader("Category-wise Sales")
    # Ensure that the column names match the DataFrame exactly (e.g., "Category" and "Sales" if case-sensitive)
    fig = px.bar(
        category_df,
        x="Category",  # Use the exact column name
        y="Sales",     # Use the exact column name
        text=[f'${x:,.2f}' for x in category_df["Sales"]],  # Fixed formatting and square brackets
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True,height=200)

with col2:
    st.subheader("Region wise Sales")
    fig=px.pie(filter_df,values="Sales",names="Region",hole=0.5)
    fig.update_traces(text=filter_df["Region"],textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# data view and download
cl1,cl2=st.columns((2))
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv=category_df.to_csv(index=False).encode('utf8')
        st.download_button("Download data",
                           data=csv,
                           file_name="Category.csv",
                           mime="text/csv",
                           help="Clickhere to download data as a CSV file")
        

with cl2:
    with st.expander("Region_ViewData"):
        region=filter_df.groupby(by="Region",as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv=region.to_csv(index=False).encode('utf8')
        st.download_button("Download data",
                           data=csv,
                           file_name="Region.csv",
                           mime="text/csv",
                           help="Clickhere to download data as a CSV file")

# time series analyse 
filter_df["month_year"]=filter_df["Order Date"].dt.to_period("M")
st.subheader("Time Series Analysis")

linechart= pd.DataFrame(filter_df.groupby(filter_df["month_year"].dt.strftime("%Y:%b"))["Sales"].sum()).reset_index()
fig2=px.line(linechart,x="month_year",y="Sales", labels={"Sales":"Amount"},height=500,width=1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Date of Time Series"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv=linechart.to_csv(index=False).encode('utf-8')
    st.download_button("Download data",
                       data=csv,
                       file_name="Time Series.csv",
                       mime="text/csv")
    
# create a tree map based on region , category, sub-category
st.subheader("Hierarchical view of sales using TreeMap")
fig3=px.treemap(filter_df,path=["Region", "Category", "Sub-Category"], values="Sales",hover_data=["Sales"],
                color="Sub-Category")
fig3.update_layout(width=800,height=650)
st.plotly_chart(fig3,use_container_width=True)
char1, char2 = st.columns((2))

with char1:
    st.subheader('Segment wise sales')
    fig = px.pie(filter_df, values="Sales", names="Segment", template="plotly_dark")
    fig.update_traces(text=filter_df["Segment"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with char2:
    st.subheader('Category wise sales')
    fig = px.pie(filter_df, values="Sales", names="Category", template="gridon")
    fig.update_traces(text=filter_df["Category"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

import plotly.figure_factory as ff

st.subheader(":point_right: Month wise Sub-Category sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month wise sub-Category Table")
    filter_df["month"] = filter_df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data=filter_df, values="Sales", index=["Sub-Category"], columns="month")
    st.write(sub_category_Year.style.background_gradient(cmap="Oranges"))

# Scatter Plot
data1 = px.scatter(filter_df, x="Sales", y="Profit", size="Quantity")
data1['layout'].update(
    title="Relationship between sales and profits using scatter plot.",
    titlefont=dict(size=10),
    xaxis=dict(title="Sales", titlefont=dict(size=19)),
    yaxis=dict(title="Profit", titlefont=dict(size=19)),
)
st.plotly_chart(data1, use_container_width=True)

# View Data
with st.expander("View data"):
    st.write(filter_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

# Download the original dataset
# Ensure all columns are Arrow-compatible
for col in filter_df.columns:
    if filter_df[col].dtype == "object":
        filter_df[col] = filter_df[col].astype(str)

csv = filter_df.to_csv(index=False).encode('utf-8')
st.download_button('Download data', data=csv, file_name="Data.csv", mime="text/csv")
