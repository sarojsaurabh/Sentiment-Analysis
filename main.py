import streamlit as st
import mysql.connector
import plotly.express as px
from io import StringIO
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
st.set_page_config(page_title="Sentiment Analysis",page_icon="https://cdn.iconscout.com/icon/premium/png-256-thumb/expression-3118033-2607314.png")
mymodel=SentimentIntensityAnalyzer()
st.title("SENTIMENT ANALYSIS SYSTEM")
st.sidebar.image("https://i1.wp.com/turbolab.in/wp-content/uploads/2021/09/sentiment.png")
choice=st.sidebar.selectbox("My Menu",("Home","Text","CSV","Database"))
if(choice=="Home"):
    st.header("WELCOME")
    st.image("https://www.mentionlytics.com/wp-content/uploads/2021/01/sentiment-analysis-icons-1-540x319.jpg")
elif(choice=="Text"):
    a=st.text_input("Enter your Opinion Here")
    btn=st.button("Analyze")
    if btn:
        pred=mymodel.polarity_scores("The tast of Dominoes Pizza is very bad ")
        if(pred['compound']>0.5):
            st.subheader("Sentiment is Positive")
        elif(pred['compound']<-0.5):
            st.subheader("Sentiment is Negative")
        else:
            st.subheader("Sentiment is Neutral")
elif(choice=="CSV"):
    st.header("Upload your CSV here")
    file=st.file_uploader("CSV File")
    cname=st.text_input("Column name")
    btn4=st.button("Analyze")
    if btn4:
        b=file.getvalue()
        p=b.decode('utf-8')
        data=StringIO(p)
        df=pd.read_csv(data)
        pos=0
        neg=0
        neu=0
        for i in range(0,len(df)):
            k=df._get_value(i,cname)
            pred=mymodel.polarity_scores(k)
            if(pred['compound']>0.5):
                pos=pos+1
            elif(pred['compound']<-0.5):
                neg=neg+1
            else:
                neu=neu+1
        pos_per=pos/len(df)
        neg_per=neg/len(df)
        neu_per=neu/len(df)
        fig=px.pie(values=[pos_per,neg_per,neu_per],names=["Positive","Negative","Neutral"])
        st.plotly_chart(fig)

elif(choice=="Database"):
    user=st.text_input("Enter User")
    pwd=st.text_input("Enter Password")
    db=st.text_input("Enter Database")
    t=st.text_input("Enter table name")    
    btn2=st.button("connect")
    if btn2:
        mydb=mysql.connector.connect(host="localhost",user=user,password=pwd,database=db)
        c=mydb.cursor()
        b="select * from "+t
        c.execute(b)
        pos=0
        neg=0
        neu=0
        l=0        
        for i in c:            
            pred=mymodel.polarity_scores(i[1])
            if(pred['compound']>0.5):
                pos=pos+1
            elif(pred['compound']<-0.5):
                neg=neg+1
            else:
                neu=neu+1
            l=l+1
        pos_per=pos/l
        neg_per=neg/l
        neu_per=neu/l
        fig=px.pie(values=[pos_per,neg_per,neu_per],names=["Positive","Negative","Neutral"])
        st.plotly_chart(fig)
