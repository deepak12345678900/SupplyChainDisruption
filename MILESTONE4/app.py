import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load Data (Replace with actual CSV or DataFrame)
df = pd.read_csv("C:/Users/DEEPAK SANTHOSH/Documents/SupplyChainDisruption/MILESTONE4/Diesel_warehouse_data.csv")

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
# Calculate additional columns
df['Remaining Inventory'] = df['Diesel Capacity'] + df['Monthly Incoming'] - df['Monthly Outgoing']
df['Utilization (%)'] = (df['Monthly Incoming'] / df['Diesel Capacity']) * 100

def send_slack_notification(message, webhook_url):
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("Slack notification sent successfully.")
    else:
        print(f"Failed to send Slack notification. Error: {response.status_code}")
# Streamlit Dashboard Setup
st.set_page_config(page_title="Diesel Inventory Dashboard", layout="wide")

# Title
st.title("📊 Diesel Inventory Dashboard")

# Metrics at a Glance
st.markdown("## Key Insights")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💧 Total Incoming Diesel", f"{df['Monthly Incoming'].sum()} liters")
with col2:
    st.metric("🚚 Total Outgoing Diesel", f"{df['Monthly Outgoing'].sum()} liters")
with col3:
    st.metric("📦 Remaining Inventory", f"{df['Remaining Inventory'].sum()} liters")
with col4:
    st.metric("⚠️ High-Risk Entries", f"{df[df['Risk'] == 'High'].shape[0]}")

# Actionable Insights
st.markdown("## 🚀 Actionable Insights")
remaining_inventory = df['Remaining Inventory'].sum()
high_risk_count = df[df['Risk'] == 'High'].shape[0]
positive_sentiment_count = df['sentiment'].value_counts().get('Positive', 0)
negative_sentiment_count = df['sentiment'].value_counts().get('Negative', 0)

if remaining_inventory < 0.2 * df['Diesel Capacity'].sum():
    message = "⚠️ **Inventory is critically low!** Consider restocking immediately to avoid disruptions."
    st.warning(message)
    send_slack_notification(message, SLACK_WEBHOOK_URL)

elif high_risk_count > 0:
    message="⚠️ **High-risk entries detected!** Monitor operations closely and adjust the supply chain."
    st.error(message)
    send_slack_notification(message, SLACK_WEBHOOK_URL)

elif positive_sentiment_count > negative_sentiment_count:
    message = "✅ **Positive sentiment dominates.** You can sell diesel at a higher margin."
    st.success(message)
    send_slack_notification(message,SLACK_WEBHOOK_URL)
else:
    st.info("ℹ️ **Operations are stable.** Keep monitoring for future trends.")

# Tabs for Detailed Analysis
st.markdown("## 📈 Detailed Analysis")
tab1, tab2, tab3= st.tabs(["Risk Analysis", "Utilization Distribution", "Risk vs Sentiment"])

# Tab 1: Risk Analysis
with tab1:
    st.subheader("Risk Distribution")
    fig1 = px.pie(df, names='Risk', color='Risk', color_discrete_sequence=px.colors.sequential.Plasma)
    fig1.update_layout(width=600, height=300)  # Adjust size for better visualization
    st.plotly_chart(fig1)



# Tab 3: Utilization Distribution
with tab2:
    st.subheader("Diesel Utilization")
    fig3 = px.histogram(df, x='Utilization (%)', nbins=10, title="Diesel Utilization (%)", color_discrete_sequence=["skyblue"])
    fig3.update_layout(width=600, height=400)
    st.plotly_chart(fig3)

# Tab 4: Risk vs Sentiment
with tab3:
    st.subheader("Risk vs Sentiment")
    risk_sentiment_data = df.groupby(['sentiment', 'Risk']).size().reset_index(name='Count')
    fig4 = px.bar(risk_sentiment_data, x='sentiment', y='Count', color='Risk', 
                  title="Risk Levels by Sentiment", barmode='stack', color_discrete_map={'High': 'red', 'Low': 'green'})
    fig4.update_layout(width=600, height=400)
    st.plotly_chart(fig4)

# Interactive Data Table
st.markdown("## 📋 Data Overview")
st.dataframe(df, width=800, height=400)


