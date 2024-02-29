import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

from sklearn.ensemble import RandomForestClassifier
import joblib
from io import StringIO
import altair as alt


def preprocess(input_data):
    # change the headers to ease of use
    header_map = {
        "How likely are you to recommend WSO2 to a friend_ or colleague on a scale from 0 to 10? [0 being not at all likely and 10 being extremely likely]":'likely_to_recomend',
        "How satisfied are you with the support given by the WSO2 team?":'satisfaction',
        "Which response best captures the main impact of our product?":'product_impact',
        "How responsive have we been to your questions or concerns about our products?":'responsiveness'
    }
    input_data.rename(columns=header_map,inplace=True)

    # select the necessary features
    input_data = input_data[['ResponseID','likely_to_recomend','satisfaction','responsiveness','product_impact','Account Name','Sales Region','Sub Region','ARR']]
    input_data.dropna(inplace=True)

    # ordinal encoding on features
    h1_map = {"Excellent":5,"Good":4,"Okay":3,"Bad":2,"Terrible":1}
    h2_map = {"Excellent":4,"Good":3,"OK":2,"Slow":1}
    h3_map = {"Many of the above":9,"High Quality":8,"Scalable":7,"Value for Money":6,"Useful":5,"Reliable":4,"Secure":3,"Unique":2,"None of the above":1}
    # --- satisfaction ----
    input_data['encoded_satisfaction'] = input_data.satisfaction.map(h1_map)
    input_data = input_data.drop(['satisfaction'],axis=1)
    # --- responsiveness ---
    input_data['encoded_responsiveness'] = input_data.responsiveness.map(h2_map)
    input_data = input_data.drop(['responsiveness'],axis=1)
    # --- product_impact ----
    input_data['encoded_product_impact'] = input_data.product_impact.map(h3_map)
    input_data = input_data.drop(['product_impact'],axis=1)

    # one-hot encoding for string values
    encoded_new_d = pd.get_dummies(input_data,columns=['encoded_product_impact'],dtype=int)
    input_data = encoded_new_d
    return input_data



def aggregate_Health(output_data):
    output = output_data
    health_val_map = {"Good":4,"Need improvement":3,"Need more attention":2,"At risk":1}
    output['-        Health        -'] = output['-        Health        -'].map(health_val_map)

    account_names = output['Account Name'].unique()  # unique account names
    df_temp = pd.DataFrame()       # create an empty dataframe
    health = []                    # create empty array to assign health
    sales_region = []


    for account in account_names:
        mean_of_health = output[output['Account Name']==account]['-        Health        -'].mean()
        mean_of_health = round(mean_of_health,0)
        health.append(mean_of_health)

        region = output[output['Account Name'] == account]['Sales Region'].unique()[0]
        sales_region.append(region)

    df_temp['Account Name'] = account_names
    df_temp['-        Health        -'] = health
    df_temp['Sales_Region'] = sales_region


    output = df_temp
    health_val_map = {4:"Good",3:"Need improvement",2:"Need more attention",1:"At risk"}
    output['-        Health        -'] = output['-        Health        -'].map(health_val_map)
    return output



def getFinaldataset(input_data):
    # preprocess
    input_data = preprocess(input_data)

    # Scale the data
    features = input_data[['likely_to_recomend','encoded_satisfaction','encoded_responsiveness']].columns
    for feature in features:
        input_data[feature] = (input_data[feature]/input_data[feature].max())*20

    # load the model
    rfc = joblib.load('E:/Research/Models/Classifiers/random_forest_classifier_model.pkl')

    # prediction
    input = input_data.drop(['ResponseID','Account Name','Sales Region','Sub Region','ARR'],axis=1)
    y_pred = rfc.predict(input)

    # assign prediction to dataset
    input_data['-        Health        -'] = y_pred 


    ##### Aggregate the outputs ######
    output_data = input_data[['Account Name','-        Health        -','Sales Region']]
    agg_data = aggregate_Health(output_data)
    return agg_data



def dashborad():
    # Title
    st.header('Customer Health')
    
    ### --- LOAD DATAFRAME
    # get the input dataset
    input_data = pd.read_csv('E:/Research/WebApp/input.csv')

    input0 = st.file_uploader(' Upload your file here... ')
    if input0 is not None:
        input_data = pd.read_csv(input0)
        # st.write(input_data)

    ##### Visualization #####
    tab1,tab2 = st.tabs(['Health Level','Churn Risk'])

    # --- DISPLAY CHART & DATAFRAME
    agg_data = getFinaldataset(input_data)

    # ---DISPLAY bar-chart of each category
    with tab1:
        Region = input_data['Sales Region'].unique().tolist()
        region_selection = st.multiselect('Sales Region:',
                                        Region,
                                        default=Region)
        mask =  (agg_data['Sales_Region'].isin(region_selection))
        number_of_result = agg_data[mask].shape[0]
        st.markdown(f'*Available Results: {number_of_result}*')

        col1,col2 = st.columns(spec=[0.6,0.4],gap="small")

        df_grouped = pd.DataFrame(agg_data[mask].groupby(by=['-        Health        -']).count()[['Account Name']])
        df_grouped = df_grouped.rename(columns={'Account Name': 'Count'})
        df_grouped = pd.DataFrame(df_grouped.reset_index())

        col1.dataframe(agg_data[mask],width=600)
        col2.bar_chart(df_grouped,x='-        Health        -',y='Count',color=["#ffaa0088"],width=500,height=500)
