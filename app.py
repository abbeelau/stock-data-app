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

# Title
st.title("📊 Stock Data Fetcher")
st.markdown("Enter a stock ticker to get real-time data and charts")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    ticker = st.text_input(
        "Enter Stock Ticker:",
        value="AAPL",
        help="Enter a valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
    ).upper().strip()
    
    period = st.selectbox(
        "Historical Period:",
        options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=2
    )
    
    fetch_button = st.button("🔍 Fetch Data", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📚 About")
    st.info("This app fetches stock data using Yahoo Finance API.")

# Main content
if fetch_button or ticker:
    with st.spinner(f"Fetching data for {ticker}..."):
        try:
            # Fetch stock data
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period=period)
            
            if not info or 'currentPrice' not in info:
                st.error(f"❌ Unable to fetch data for ticker: {ticker}")
                st.info("Please check if the ticker symbol is correct.")
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
                    st.write(f"**Website:** {info.get('website', 'N/A')}")
                
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

else:
    st.info("👈 Enter a stock ticker in the sidebar and click 'Fetch Data'!")
    
    st.markdown("### 🚀 Popular Tickers to Try")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**AAPL** - Apple")
        st.markdown("**MSFT** - Microsoft")
    with col2:
        st.markdown("**GOOGL** - Google")
        st.markdown("**AMZN** - Amazon")
    with col3:
        st.markdown("**TSLA** - Tesla")
        st.markdown("**META** - Meta")
    with col4:
        st.markdown("**NVDA** - NVIDIA")
        st.markdown("**JPM** - JPMorgan")

# Footer
st.markdown("---")
st.markdown("📈 **Stock Data Fetcher** | Powered by Yahoo Finance API")
st.caption("Data is delayed by ~15 minutes. Not for trading purposes.")
```

---

## File 2: `requirements.txt`
```
streamlit>=1.28.0
yfinance>=0.2.28
pandas>=2.0.0
plotly>=5.17.0
