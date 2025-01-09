import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# Load the existing dataset
current_day_sales = pd.read_csv('current_day_sales.csv')
current_day_sales['Time'] = pd.to_datetime(current_day_sales['Time'])

platforms = current_day_sales['Platform'].unique()
products = current_day_sales['Product'].unique()

# Initialize session state for KPIs and data
if 'total_revenue' not in st.session_state:
    st.session_state['total_revenue'] = 100_000_000  # Starting revenue

if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 120_000_000  # Starting cost

if 'sales_by_platform' not in st.session_state:
    st.session_state['sales_by_platform'] = {
        'Shopee': 40,
        'TikTok': 30,
        'Lazada': 30
    }

if 'sales_by_product' not in st.session_state:
    st.session_state['sales_by_product'] = {
        'Búp bê Barbie': 40,
        'Labubu': 30,
        'Capybara': 20,
        'Gấu bông': 10
    }

# Streamlit setup
st.title('Báo Cáo Tự Động Về Doanh Số')
st.write("Hiển thị doanh số, lợi nhuận và thông tin liên quan.")

# Sidebar controls
interval = st.sidebar.slider("Chọn khoảng thời gian cập nhật (giây):", 1, 10, 5)

# Update KPIs every interval
st.session_state['total_revenue'] += 150_000  # Increase revenue by 150K every interval
profit = st.session_state['total_revenue'] - st.session_state['total_cost']

# Display KPIs
st.metric("Tổng Doanh Thu", f"${st.session_state['total_revenue'] / 1e6:.2f}M", 
          delta=f"+150K")
st.metric("Tổng Lợi Nhuận", f"${profit / 1e6:.2f}M", 
          delta=f"+{(150_000 - 150_000 * 0.6) / 1e6:.2f}M")

# Update Pie Chart: Sales by Platform
for platform in st.session_state['sales_by_platform']:
    st.session_state['sales_by_platform'][platform] += np.random.uniform(0.001, 0.02) * st.session_state['sales_by_platform'][platform]

# Create Pie Chart: Sales by Platform
platform_labels = list(st.session_state['sales_by_platform'].keys())
platform_values = list(st.session_state['sales_by_platform'].values())
fig1 = go.Figure(data=[go.Pie(labels=platform_labels, values=platform_values)])
fig1.update_layout(title="Số Lượng Bán Theo Sàn")

# Update Pie Chart: Sales by Product
for product in st.session_state['sales_by_product']:
    st.session_state['sales_by_product'][product] += np.random.uniform(0.005, 0.01) * st.session_state['sales_by_product'][product]

# Create Pie Chart: Sales by Product
product_labels = list(st.session_state['sales_by_product'].keys())
product_values = list(st.session_state['sales_by_product'].values())
fig2 = go.Figure(data=[go.Pie(labels=product_labels, values=product_values)])
fig2.update_layout(title="Số Lượng Bán Theo Loại Sản Phẩm")

# Display Pie Charts
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# Placeholder for the main chart
chart_placeholder = st.empty()

# Main chart logic (retain original behavior)
data = st.session_state['data']
while True:
    # Filter data based on user selections
    filtered_data = data

    # Prepare data for chart
    pivot_data = filtered_data.pivot_table(
        index='Time', columns='Platform', values='Sales (15 min)', aggfunc='sum', fill_value=0
    )

    # Select visible data based on zoom level
    zoom_level = st.sidebar.slider("Chọn số lượng cột hiển thị:", 10, 50, 20)
    if len(pivot_data) > zoom_level:
        visible_data = pivot_data.iloc[-zoom_level:]
    else:
        visible_data = pivot_data

    # Create Plotly figure
    fig3 = go.Figure()

    # Add stacked bar traces
    for platform in platforms:
        if platform in visible_data.columns:
            fig3.add_trace(go.Bar(
                x=visible_data.index,
                y=visible_data[platform],
                name=platform
            ))

    # Add line traces
    cumulative_data = visible_data.cumsum(axis=1)
    for i, platform in enumerate(platforms):
        if platform in cumulative_data.columns:
            fig3.add_trace(go.Scatter(
                x=visible_data.index,
                y=cumulative_data[platform],
                mode='lines+markers',
                name=f"{platform} (Đường)"
            ))

    fig3.update_layout(
        barmode='stack',
        title="Biểu Đồ Doanh Số Theo Thời Gian",
        xaxis_title="Thời Gian",
        yaxis_title="Doanh Số",
        xaxis=dict(rangeslider=dict(visible=True), type="date"),
        template="plotly_white"
    )

    # Update the chart in the placeholder
    chart_placeholder.plotly_chart(fig3, use_container_width=True)

    # Simulate new data
    data = simulate_new_data(data)

    # Pause for real-time simulation
    time.sleep(interval)
