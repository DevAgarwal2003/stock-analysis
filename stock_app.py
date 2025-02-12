import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from backend import import_html, get_tables, pnl_growth_graphs, plot_interest_coverage, plot_eps, plot_sales_operating_profit, plot_operating_expense_ratio, plot_debt_to_equity, plot_debt_to_total_assets, plot_reserves_to_equity, plot_roa, plot_roe, plot_roce


# Set page layout
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        /* Set the background color of the entire page */
        body {
            background-color: #121212;
            color: white;
        }

        /* Remove white spots */
        .block-container {
            background-color: #121212;
        }

        /* Center title */
        .title-container {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: white;
        }

        /* Style metric cards */
        .stMetric {
            background-color: #1e1e1e !important;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            box-shadow: none;
            color: white !important;
        }

        /* Box styling for charts */
        .chart-box {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("📊 Fundamental Trend Analysis of Stock Market Dashboard")
ticker_list = tickers = [
    "TCS", "HINDUNILVR", "RELIANCE", "INFY", "LT", "MARUTI", "ASIANPAINT",
    "HAL", "NESTLEIND", "SIEMENS", "BAJAJ-AUTO", "COALINDIA", "PIDILITIND",
    "EICHERMOT", "CIPLA", "ABB", "MCDOWELL-N", "VBL", "LTIM"
]

c1, c2 = st.columns(2)
with c1:
    ticker = st.selectbox("Enter the stock ticker", ['Select a Ticker'] + ticker_list)
    
with c2:
    option = st.selectbox("Enter consolidated or standalone", ['consolidated', 'standalone'])
    
if ticker != 'Select a Ticker' and option:
    pnl, sales_growth, profit_growth, stock_cagr, roe, balance_sheet, cash_flow, ratios, shareholding = get_tables(ticker, option)

    fig_growth = pnl_growth_graphs(pnl)
    fig_sales_profit = plot_sales_operating_profit(pnl)
    
    fig_interest_coverage = plot_interest_coverage(pnl)
    fig_eps = plot_eps(pnl)
    fig_operating_expense_ratio = plot_operating_expense_ratio(pnl)
    
    fig_debt_to_eq = plot_debt_to_equity(balance_sheet)
    fig_debt_to_assets = plot_debt_to_total_assets(balance_sheet)
    fig_reserves_to_equity = plot_reserves_to_equity(balance_sheet)
    
    fig_roa = plot_roa(balance_sheet, pnl)
    fig_roe = plot_roe(balance_sheet, pnl)
    fig_roce = plot_roce(ratios)
    
    st.plotly_chart(fig_sales_profit, use_container_width=True)
    st.plotly_chart(fig_growth, use_container_width=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.plotly_chart(fig_eps, use_container_width=True)
    with col2:
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.plotly_chart(fig_interest_coverage, use_container_width=True)
    with col3:
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.plotly_chart(fig_operating_expense_ratio, use_container_width=True)
    with col1:
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.plotly_chart(fig_debt_to_eq, use_container_width=True)
    with col2:
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.plotly_chart(fig_debt_to_assets, use_container_width=True)
    with col3:
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.plotly_chart(fig_reserves_to_equity, use_container_width=True)
    with col1:
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.plotly_chart(fig_roa, use_container_width=True)
    with col2:
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.plotly_chart(fig_roe, use_container_width=True)
    with col3:
        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.plotly_chart(fig_roce, use_container_width=True)
    
    