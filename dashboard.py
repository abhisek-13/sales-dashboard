from fileinput import filename

import streamlit as st  # used to create web dashboard
import plotly.express as  pt # USED FOR DATA VISUALIZATION I.E, BAR CHART ETC
import pandas as pd #USED FOR DATA MANIPULATION
import os #USED FOR DATA MANIPULATION
import warnings

from streamlit import file_uploader

warnings.filterwarnings('ignore')


st.set_page_config(page_title="Superstore!!!",page_icon=":bar_chart",layout="wide")
st.title(" :bar_chart: Sample Superstore EDA")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

#Flie Upload and data loading
fl = None
with st.sidebar:
    with st.expander(":file_folder: Upload a file "):
        fl=st.file_uploader("",type=(["csv","txt","xlsv","xls"]))  #:file_folder: is for the folder emoji
if fl is not None:
    filename=fl.name
    st.write(filename)
    df=pd.read_csv(filename,encoding = "ISO-8859-1")
else:
    # os.chdir(r"D:\Dashboard Project")
    df=pd.read_csv("Sample - Superstore.csv",encoding = "ISO-8859-1")


start,end=st.columns(2)
# Automatically infers the format
df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False, errors='coerce')
#converts the data in order date column in dataset into date format

#Getting the max and min date
startDate= pd.to_datetime(df['Order Date']).min()
endDate= pd.to_datetime(df['Order Date']).max()
with start:
    date1=pd.to_datetime(st.date_input("Start Date",startDate))
with end:
    date2=pd.to_datetime(st.date_input("End Date",endDate))

df=df[(df['Order Date']>=date1) & (df['Order Date']<=date2)].copy()
#Create the sidebar(Region)
st.sidebar.header("Choose your filter  :")
region=st.sidebar.multiselect("Pick your region",df["Region"].unique())
if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)]

#Create the sidebar(State)
state=st.sidebar.multiselect("Pick your state",df2['State'].unique())
if not state:
    df3=df.copy()
else:
    df3=df[df["State"].isin(state)]

#Create the sidebar(City)

city=st.sidebar.multiselect("Pick your city",df3['City'].unique())

#Filter the data based on Region,state,city
if not region and not state and not city:
    filtered_df=df
elif not state and not city:
    filtered_df=df[df['Region'].isin(region)]
elif not city and not region:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
   filtered_df=df[df['State'].isin(state) & df3['City'].isin(city)]
elif region and city:
    filtered_df=df[df['Region'].isin(region) & df3['City'].isin(city)]
elif state and region:
    filtered_df=df[df['Region'].isin(region) & df['State'].isin(state)]
elif city:
    filtered_df=df3[df3['City'].inin(city)]
else:
    filtered_df=df3[df["Region"].isin(region) & df3[df3['State'].isin(state) & df3['City'].inin(city)]]
catogory_df = filtered_df.groupby(by=['Category'],as_index=False)["Sales"].sum()
with start:
    st.subheader("Category wise sales")
    fig = pt.bar(catogory_df,x = "Category",y = "Sales",text = ['${:,.2f}'.format(x) for x in catogory_df["Sales"]],template="seaborn")
    st.plotly_chart(fig,use_container_width=True,height = 200)

with end:
    st.subheader("Region wise sales")
    fig=pt.pie(filtered_df,values="Sales",names="Region",hole=0.5)
    fig.update_traces(text=filtered_df["Region"],textposition="outside")
    st.plotly_chart(fig,use_container_width=True)

start,end = st.columns(2)
with start:
    with st.expander("Category_ViewData"):
        st.write(catogory_df.style.background_gradient(cmap="Blues"))
        csv = catogory_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data = csv,file_name= "Category.csv",mime="text/csv",help='Click here to download the data as a CSV file')
with end:
    with st.expander("Region_ViewData"):
        region=filtered_df.groupby(by="Region",as_index = False)["Sales"].sum()
        st.write(catogory_df.style.background_gradient(cmap="Oranges"))
        csv = catogory_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

filtered_df["month_year"]=filtered_df["Order Date"].dt.to_period("M")
st.subheader("Time Series Analysis")

linechart=pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y :%b"))["Sales"].sum()).reset_index()
fig2=pt.line(linechart,x="month_year",y="Sales",labels={"Sales":"Amount"},height=500,width=1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)
with st.expander("View Data of Timeseries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv=linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download data",data=csv,file_name="Timeseries.csv",mime="text/csv")
st.subheader("Hierarchial veiw of Sales using TreeMap")
fig3=pt.treemap(filtered_df,path=["Region","Category","Sub-Category"],values="Sales",hover_name="Sales",color="Sub-Category")
fig3.update_layout(width=800,height=650)
st.plotly_chart(fig3,use_container_width=True)



chart1,chart2=st.columns(2)
with chart1:
    st.subheader("Segment wise Sales")
    fig=pt.pie(filtered_df,values="Sales",names="Segment",template="plotly_dark")
    fig.update_traces(text=filtered_df['Segment'],textposition="inside")
    st.plotly_chart(fig,use_container_width=True)
with chart2:
    st.subheader("Category wise Sales")
    fig = pt.pie(filtered_df, values="Sales", names="Category", template="plotly_dark")
    fig.update_traces(text=filtered_df['Segment'], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)



import plotly.figure_factory as ff
st.subheader(": point_right : Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample=df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig=ff.create_table(df_sample,colorscale="Cividis")
    st.plotly_chart(fig,use_container_width=True)


    st.markdown("Month wise sub-Category Table")
    filtered_df["month"]=filtered_df["Order Date"].dt.month_name()
    sub_category_Year=pd.pivot_table(data=filtered_df,values="Sales",index=["Sub-Category"],columns="month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

#Scatter Plot
d1=pt.scatter(filtered_df,x="Sales", y="Profit",size="Quantity")
d1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot",xaxis=dict(title="Sales"),yaxis=dict(title="Profit"))
st.plotly_chart(d1,use_container_width=True)

with st.expander("View Data:"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))
csv=df.to_csv(index=False).encode('utf-8')
st.download_button("Download Data",data=csv,file_name="Data.csv",mime="text/csv")
