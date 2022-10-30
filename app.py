import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple Stock Price App

Shown are the stock closing pice and volume of stock
""")

input = "Type something here and click"

## Let's try adding an input text field
test_input = st.text_area("What ticker are you interested in?", input, height=10)

test_input

# adds a page break line
st.write("""
***
""")

ticker = 'GOOGL'
#tickerData = yf.Ticker(ticker)
tickerData = yf.Ticker(test_input)

tickerDF = tickerData.history(period='id', start='2010-05-31', end='2020-05-31')

st.line_chart(tickerDF.Close)
st.line_chart(tickerDF.Volume)

print(tickerData)