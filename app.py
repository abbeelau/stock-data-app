"""
Stock Data Fetcher App
A simple web application to fetch and display stock market data using Yahoo Finance API
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Stock Data Fetcher",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for search history
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Sidebar Menu
with st.sidebar:
    st.title("📈 Stock Data Fetcher")
    
    menu = st.radio(
        "Navigation",
        ["🔍 Search Stocks", "📚 Ticker Guide", "📊 Compare Stocks", "🕒 Recent Searches", "ℹ️ About"],
        index=0
    )
    
    st.markdown("---")

# ========================================
# PAGE 1: SEARCH STOCKS
# ========================================
if menu == "🔍 Search Stocks":
    st.header("🔍 Search Stock Data")
    st.markdown("Enter a stock ticker to get real-time data and charts")
    st.markdown("---")
    
    # Settings
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker:",
            value="AAPL",
            help="Enter a valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL)",
            key="ticker_input"
        ).upper().strip()
    
    with col2:
        period = st.selectbox(
            "Time Period:",
            options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=2
        )
    
    fetch_button = st.button("🔍 Fetch Data", type="primary", use_container_width=True)
    
    if fetch_button or ticker:
        # Add to search history
        if ticker and ticker not in st.session_state.search_history:
            st.session_state.search_history.insert(0, ticker)
            if len(st.session_state.search_history) > 10:
                st.session_state.search_history = st.session_state.search_history[:10]
        
        with st.spinner(f"Fetching data for {ticker}..."):
            try:
                # Fetch stock data
                stock = yf.Ticker(ticker)
                info = stock.info
                hist = stock.history(period=period)
                
                if not info or 'currentPrice' not in info:
                    st.error(f"❌ Unable to fetch data for ticker: {ticker}")
                    st.info("💡 **Tips:**\n- Check if the ticker is spelled correctly\n- For international stocks, use the correct suffix (e.g., SHOP.TO for Toronto)\n- Try searching in the Ticker Guide")
                else:
                    # Company header
                    company_name = info.get('longName', ticker)
                    st.title(f"{company_name} ({ticker})")
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    current_price = info.get('currentPrice', 0)
                    previous_close = info.get('previousClose', 0)
                    change = current_price - previous_close
                    change_percent = (change / previous_close * 100) if previous_close else 0
                    
                    with col1:
                        st.metric(
                            "Current Price",
                            f"${current_price:,.2f}" if current_price else "N/A",
                            delta=f"{change:+.2f} ({change_percent:+.2f}%)" if change else None
                        )
                    
                    with col2:
                        volume = info.get('volume', 0)
                        st.metric("Volume", f"{volume:,}" if volume else "N/A")
                    
                    with col3:
                        market_cap = info.get('marketCap', 0)
                        if market_cap:
                            if market_cap >= 1e12:
                                cap_str = f"${market_cap/1e12:.2f}T"
                            elif market_cap >= 1e9:
                                cap_str = f"${market_cap/1e9:.2f}B"
                            elif market_cap >= 1e6:
                                cap_str = f"${market_cap/1e6:.2f}M"
                            else:
                                cap_str = f"${market_cap:,.0f}"
                            st.metric("Market Cap", cap_str)
                        else:
                            st.metric("Market Cap", "N/A")
                    
                    with col4:
                        pe_ratio = info.get('trailingPE', 0)
                        st.metric("P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
                    
                    st.markdown("---")
                    
                    # Company details
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.subheader("📊 Trading Information")
                        st.write(f"**Open:** ${info.get('open', 0):.2f}")
                        st.write(f"**Day High:** ${info.get('dayHigh', 0):.2f}")
                        st.write(f"**Day Low:** ${info.get('dayLow', 0):.2f}")
                        st.write(f"**52 Week High:** ${info.get('fiftyTwoWeekHigh', 0):.2f}")
                        st.write(f"**52 Week Low:** ${info.get('fiftyTwoWeekLow', 0):.2f}")
                    
                    with col_right:
                        st.subheader("🏢 Company Information")
                        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                        st.write(f"**Country:** {info.get('country', 'N/A')}")
                        website = info.get('website', 'N/A')
                        if website != 'N/A':
                            st.write(f"**Website:** [{website}]({website})")
                        else:
                            st.write(f"**Website:** N/A")
                    
                    st.markdown("---")
                    
                    # Price chart
                    if not hist.empty:
                        st.subheader(f"📈 Price Chart ({period})")
                        
                        fig = go.Figure(data=[go.Candlestick(
                            x=hist.index,
                            open=hist['Open'],
                            high=hist['High'],
                            low=hist['Low'],
                            close=hist['Close'],
                            name=ticker
                        )])
                        
                        fig.update_layout(
                            xaxis_title="Date",
                            yaxis_title="Price (USD)",
                            height=600,
                            hovermode='x unified',
                            xaxis_rangeslider_visible=False,
                            template="plotly_white"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Historical data table
                        st.subheader("📋 Historical Data")
                        st.dataframe(hist, use_container_width=True)
                        
                        # Download button
                        csv = hist.to_csv()
                        st.download_button(
                            label="📥 Download Data (CSV)",
                            data=csv,
                            file_name=f"{ticker}_data_{period}.csv",
                            mime="text/csv"
                        )
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Please try a different ticker or check the Ticker Guide for help.")

# ========================================
# PAGE 2: TICKER GUIDE
# ========================================
elif menu == "📚 Ticker Guide":
    st.header("📚 Ticker Symbol Guide")
    st.markdown("Learn how to search for different types of stocks")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🇺🇸 US Stocks", "🌍 International", "💰 Crypto & ETFs", "📊 Indices"])
    
    with tab1:
        st.subhea
