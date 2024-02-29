import streamlit as st
import pandas as pd
from dashboard import preprocess,aggregate_Health,getFinaldataset
import numpy as np
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
from healthscoreInferencing import gethealthscoreDataset



def piechart(df):
    # Create some sample data
    data = {'Category': ['Positive', 'Negative'],
            'Values': [30, 30]}
    df = pd.DataFrame(data)

    color = ['lightgreen','red']

    fig = px.pie(df, values='Values', names='Category', title='Sentiment Meter',color_discrete_sequence=color)
    fig.update_layout(title_font_size=30)
    st.plotly_chart(fig, use_container_width=True)


def drawCharts(df):
    arr = df['ARR']
    year = df['dateTime']

    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        piechart(df)
    with fig_col2:
        st.markdown("#### Health Chart")
        st.scatter_chart(data=df,x='dateTime',y='Health_Score')
        # st.write(fig2)
    
    with st.container(border=True):
        st.markdown("#### Anual Recurring Revenue")
        st.line_chart(data=df,x='dateTime',y='ARR')



def individual_dashboard():
    # read csv from a github repo
    input = pd.read_csv("E:/Research/WebApp/input.csv")

    # Get the  datasets
    healthscore_df = gethealthscoreDataset()
    segmented_dataset = getFinaldataset(input)

    # dashboard title
    st.title("Customer Health Dashboard")

    # top-level filters 
    col1,col2 = st.columns([0.5,0.5])

    region_filter = col2.selectbox("Select the Region",pd.unique(healthscore_df['Sales Region']))
    acc_filter = col1.selectbox("Select the Account Name", pd.unique(healthscore_df[(healthscore_df['Sales Region']==region_filter)]['Account Name']))

    # creating a single-element container.
    placeholder = st.empty()

    # dataframe filter 
    df1 = healthscore_df[(healthscore_df['Account Name']==acc_filter) & (healthscore_df['Sales Region']==region_filter)]
    df2 = segmented_dataset[(segmented_dataset['Account Name']==acc_filter) & (segmented_dataset['Sales_Region']==region_filter)]


    ######### Display health  ###########
    c1,c2,c3 = st.columns([0.4,0.3,0.3])

    c1.container(border=True).header(df2['-        Health        -'].values[0])
    c2.container(border=True).header(round(df1['Health_Score'].mean()))
    c3.container(border=True).header('Sentiment')
    # c3.container(border=True).metric(label="Sentiment ", value="Sentiment")

    with st.container(height=60,border=False):
        st.markdown("")
    drawCharts(df1)





















    # # near real-time / live feed simulation 
    # for seconds in range(200):
    # #while True: 

    #     # creating KPIs 
    #     arr = df['ARR'] 

    #     year = df['dateTime']
        
    #     balance = np.mean(df['balance_new'])

    #     with placeholder.container():
    #         # create three columns
    #         kpi1, kpi2, kpi3 = st.columns(3)

    #         # fill in those three columns with respective metrics or KPIs 
    #         kpi1.metric(label="Account Name ", value=round(arr))
    #         kpi2.metric(label=" Count ", value= int(count_married), delta= - 10 + count_married)
    #         kpi3.metric(label="A/C Balance ＄", value= f"$ {round(balance,2)} ", delta= - round(balance/count_married) * 100)

    #         # create two columns for charts 

    #         fig_col1, fig_col2 = st.columns(2)
    #         with fig_col1:
    #             st.markdown("### First Chart")
    #             fig = px.density_heatmap(data_frame=df, y = 'arr', x = 'year')
    #             st.write(fig)
    #         with fig_col2:
    #             st.markdown("### Second Chart")
    #             fig2 = px.histogram(data_frame = df, x = 'age_new')
    #             st.write(fig2)
    #         st.markdown("### Detailed Data View")
    #         st.dataframe(df)
    #         time.sleep(1)
    # #placeholder.empty()

