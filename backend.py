import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def import_html(url, element_type="table", index=0):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()  # Ensure request success
    
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all(element_type)
    
    if index >= len(elements):
        raise ValueError(f"Index {index} out of range. Found {len(elements)} {element_type}(s).")

    return pd.read_html(str(elements[index]))[0]  # Convert table to DataFrame

# ticker  = ticker = input("Enter the company ticker: ")
def get_tables(ticker, option):
    base_url = f"https://www.screener.in/company/{ticker}"
    urls = [f"https://www.screener.in/company/{ticker}/consolidated", base_url]
    # option = input("Select consolidated or standalone: ")

    if option == 'consolidated':
        url = urls[0]
        pnl = import_html(url, element_type="table", index=1)
        sales_growth = import_html(url, element_type="table", index=2)
        profit_growth = import_html(url, element_type="table", index=3)
        stock_cagr = import_html(url, element_type="table", index=4)
        roe = import_html(url, element_type="table", index=5)
        balance_sheet = import_html(url, element_type="table", index=6)
        cash_flow = import_html(url, element_type="table", index=7)
        ratios = import_html(url, element_type="table", index=8)
        shareholding = import_html(url, element_type="table", index=9)
        
    else: 
        url = urls[1]
        pnl = import_html(url, element_type="table", index=1)
        sales_growth = import_html(url, element_type="table", index=2)
        profit_growth = import_html(url, element_type="table", index=3)
        stock_cagr = import_html(url, element_type="table", index=4)
        roe = import_html(url, element_type="table", index=5)
        balance_sheet = import_html(url, element_type="table", index=6)
        cash_flow = import_html(url, element_type="table", index=7)
        ratios = import_html(url, element_type="table", index=8)
        shareholding = import_html(url, element_type="table", index=9)
        
    return pnl, sales_growth, profit_growth, stock_cagr, roe, balance_sheet, cash_flow, ratios, shareholding
        
def pnl_growth_graphs(pnl):
    columns_list = pnl.columns[2:].tolist()  # ['Expenses', 'OPM']

    # Convert Revenue and OPM values to numeric (handling % values)
    row_list = pnl.iloc[2, 1:].astype(str).str.replace('%', '').astype(float).tolist()
    opm_list = pnl.iloc[3, 2:].astype(str).str.replace('%', '').astype(float).tolist()

    # Calculate Revenue Growth (ensure proper indexing)
    revenue_growth = [( (row_list[i] - row_list[i-1]) / row_list[i-1] ) * 100 for i in range(1, len(row_list))]

    # Adjust the Years list (remove first year since revenue growth starts from the second year)
    years = columns_list[1:]

    # Create a figure
    fig = go.Figure()

    # Add Revenue Growth as Bar Chart
    fig.add_trace(go.Bar(
        x=years, 
        y=revenue_growth, 
        name="Revenue Growth (%)",
        marker_color='blue',
        opacity=0.7
    ))

    # Add Operating Profit Margin as Line Chart
    fig.add_trace(go.Scatter(
        x=years, 
        y=opm_list[1:],  # Remove first value to match revenue growth length
        name="Operating Profit Margin (%)",
        mode='lines+markers',
        line=dict(color='red', width=2)
    ))

    # Update Layout
    fig.update_layout(
        title="Revenue Growth & Operating Profit Margin",
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        barmode='group',
        legend_title="Metrics"
    )

    return fig

def plot_sales_operating_profit(pnl):
    years = pnl.columns[1:-1]  # Exclude "Unnamed: 0" and "TTM"
    sales = pnl.iloc[0, 1:-1].astype(float)  # Sales row
    operating_profit = pnl.iloc[2, 1:-1].astype(float)  # Operating Profit row

    fig = go.Figure()

    # Sales as Bar Chart
    fig.add_trace(go.Bar(
        x=years, 
        y=sales, 
        name="Sales", 
        marker_color='blue'
    ))

    # Operating Profit as Bar Chart
    fig.add_trace(go.Bar(
        x=years, 
        y=operating_profit, 
        name="Operating Profit", 
        marker_color='green'
    ))

    fig.update_layout(
        title="Sales & Operating Profit",
        xaxis_title="Year",
        yaxis_title="Amount",
        barmode='group',
        legend_title="Metrics"
    )

    return fig

def plot_eps(df):
    years = df.columns[1:-1]
    eps = df.iloc[10, 1:-1].astype(float)  # EPS row

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years, 
        y=eps, 
        mode='lines+markers', 
        name="EPS",
        line=dict(color='purple', width=2)
    ))

    fig.update_layout(
        title="Earnings Per Share (EPS)",
        xaxis_title="Year",
        yaxis_title="EPS in Rs",
        legend_title="Metrics"
    )

    return fig

def plot_interest_coverage(df):
    years = df.columns[1:-1]
    operating_profit = df.iloc[2, 1:-1].astype(float)  # Operating Profit row
    interest = df.iloc[5, 1:-1].astype(float)  # Interest row

    # Avoid division by zero
    interest_coverage = [op / int_val if int_val != 0 else None for op, int_val in zip(operating_profit, interest)]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years, 
        y=interest_coverage, 
        mode='lines+markers', 
        name="Interest Coverage Ratio",
        line=dict(color='red', width=2)
    ))

    fig.update_layout(
        title="Interest Coverage Ratio",
        xaxis_title="Year",
        yaxis_title="Ratio",
        legend_title="Metrics"
    )

    return fig

def plot_operating_expense_ratio(df_pl):
    """Plots the Operating Expense Ratio over time."""
    df = pd.DataFrame()
    
    df['Year'] = df_pl.columns[1:]
    expenses = df_pl.loc[1, df_pl.columns[1:]].astype(float).values  # Convert to float
    sales = df_pl.loc[0, df_pl.columns[1:]].astype(float).values  # Convert to float

    df['Operating Expense Ratio'] = (expenses / sales) * 100  

    fig = px.line(df, x='Year', y='Operating Expense Ratio', title="Operating Expense Ratio Over Time", markers=True)
    return fig

def plot_debt_to_equity(df_bs):
    """Plots Debt-to-Equity Ratio over time."""
    df = pd.DataFrame()

    df['Year'] = df_bs.columns[1:]
    total_liabilities = df_bs.loc[4, df_bs.columns[1:]].astype(float).values  # Convert to float
    equity = df_bs.loc[0, df_bs.columns[1:]].astype(float).values  # Convert to float
    reserves = df_bs.loc[1, df_bs.columns[1:]].astype(float).values

    df['Debt-to-Equity Ratio'] = total_liabilities / (equity+reserves) 

    fig = px.line(df, x='Year', y='Debt-to-Equity Ratio', title="Debt-to-Equity Ratio Over Time", markers=True)
    return fig

def plot_debt_to_total_assets(df_bs):
    """Plots Debt-to-Total Assets Ratio over time."""
    df = pd.DataFrame()

    df['Year'] = df_bs.columns[1:]
    total_liabilities = df_bs.loc[2, df_bs.columns[1:]].astype(float).values  # Convert to float
    total_assets = df_bs.loc[9, df_bs.columns[1:]].astype(float).values  # Convert to float

    df['Debt-to-Total-Assets Ratio'] = total_liabilities / total_assets

    fig = px.line(df, x='Year', y='Debt-to-Total-Assets Ratio', title="Debt-to-Total-Assets Ratio Over Time", markers=True)
    return fig

def plot_reserves_to_equity(df_bs):
    """Plots Reserves as % of Equity Capital over time."""
    df = pd.DataFrame()

    df['Year'] = df_bs.columns[1:]
    reserves = df_bs.loc[1, df_bs.columns[1:]].astype(float).values  # Convert to float
    equity = df_bs.loc[0, df_bs.columns[1:]].astype(float).values  # Convert to float

    df['Reserves-to-Equity (%)'] = (reserves / equity) * 100  

    fig = px.line(df, x='Year', y='Reserves-to-Equity (%)', 
                  title="Reserves as a Percentage of Equity Over Time", 
                  markers=True)
    return fig

def plot_roa(df_bs, df_pl):
    """Plots Return on Assets (ROA) over time."""
    df = pd.DataFrame()
    
    df['Year'] = df_bs.columns[1:]
    net_profit = df_pl.loc[9, df_pl.columns[1:]].astype(float).values  # Convert to float
    total_assets = df_bs.loc[9, df_bs.columns[1:]].astype(float).values  # Convert to float

    df['ROA (%)'] = (net_profit / total_assets) * 100  

    fig = px.line(df, x='Year', y='ROA (%)', title="Return on Assets (ROA) Over Time", markers=True)
    return fig

def plot_roe(df_bs, df_pl):
    """Plots Return on Equity (ROE) over time."""
    df = pd.DataFrame()
    
    df['Year'] = df_bs.columns[1:]
    net_profit = df_pl.loc[9, df_pl.columns[1:]].astype(float).values  # Convert to float
    equity = df_bs.loc[0, df_bs.columns[1:]].astype(float).values   # Convert to float
    reserves = df_bs.loc[1, df_bs.columns[1:]].astype(float).values

    df['ROE (%)'] = (net_profit / (equity+reserves)) * 100  

    fig = px.line(df, x='Year', y='ROE (%)', title="Return on Equity (ROE) Over Time", markers=True)
    return fig

def plot_roce(df_ratios):
    """Plots ROCE % over time using Plotly."""
    # Extract years (columns excluding first)
    years = df_ratios.columns[1:]

    # Extract ROCE row and convert to numeric, handling '%'
    roce_values = df_ratios.iloc[5, 1:].astype(str).str.rstrip('%').astype(float).values

    # Create DataFrame for Plotly
    df_plot = pd.DataFrame({'Year': years, 'ROCE %': roce_values})

    # Create line plot
    fig = px.line(df_plot, x='Year', y='ROCE %', title="ROCE % Over Time", markers=True)
    
    return fig 