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

# Initialize session state to retain past data
if 'data' not in st.session_state:
    st.session_state['data'] = current_day_sales.copy()

if 'total_revenue' not in st.session_state:
    st.session_state['total_revenue'] = 100_000_000  # Starting revenue

if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 120_000_000  # Starting cost

if 'sales_by_platform' not in st.session_state:
    st.session_state['sales_by_platform'] = {
        platform: 1 for platform in platforms
    }

if 'sales_by_product' not in st.session_state:
    st.session_state['sales_by_product'] = {
        product: 1 for product in products
    }

# Streamlit setup
st.title('Báo Cáo Tự Động Về Doanh Số')
st.write("Hiển thị doanh số, lợi nhuận và thông tin liên quan.")

# Sidebar for user selections
selected_platforms = st.sidebar.multiselect("Chọn nền tảng:", platforms, default=platforms)
selected_products = st.sidebar.multiselect("Chọn loại sản phẩm:", products, default=products)
zoom_level = st.sidebar.slider("Chọn số lượng cột hiển thị:", 10, 50, 20)

# Filter data based on user selection
def filter_data(data, platforms, products):
    return data[(data['Platform'].isin(platforms)) & (data['Product'].isin(products))]

# Simulate new data for live updates
def simulate_new_data(data):
    latest_time = data['Time'].max() + pd.Timedelta(minutes=15)
    new_data = []
    for platform in platforms:
        for product in products:
            sales_15_min = np.random.randint(1, 20)
            new_data.append({'Time': latest_time, 'Platform': platform, 'Product': product, 'Sales (15 min)': sales_15_min})
    new_df = pd.DataFrame(new_data)
    return pd.concat([data, new_df], ignore_index=True)

# Update real-time data
st.session_state['data'] = simulate_new_data(st.session_state['data'])
filtered_data = filter_data(st.session_state['data'], selected_platforms, selected_products)

# Update KPIs
total_sales_new = filtered_data['Sales (15 min)'].sum()
revenue_increase = 150_000  # Revenue increases by 150K every 5 seconds
st.session_state['total_revenue'] += revenue_increase
total_cost = st.session_state['total_cost'] + revenue_increase * 0.6  # Cost increases proportionally
profit = st.session_state['total_revenue'] - total_cost

# Display KPIs
st.metric("Tổng Doanh Thu", f"${st.session_state['total_revenue'] / 1e6:.2f}M", delta=f"+{revenue_increase / 1e6:.2f}M")
st.metric("Tổng Lợi Nhuận", f"${profit / 1e6:.2f}M", delta=f"+{(revenue_increase - revenue_increase * 0.6) / 1e6:.2f}M")

# Update Pie chart: Số lượng bán trên từng sàn
for platform in st.session_state['sales_by_platform']:
    st.session_state['sales_by_platform'][platform] += np.random.uniform(0.001, 0.02) * st.session_state['sales_by_platform'][platform]

# Create Pie Chart: Sales by Platform
platform_labels = list(st.session_state['sales_by_platform'].keys())
platform_values = list(st.session_state['sales_by_platform'].values())
fig1 = go.Figure(data=[go.Pie(labels=platform_labels, values=platform_values)])
fig1.update_layout(title="Số Lượng Bán Theo Sàn")

# Update Pie chart: Số lượng bán theo loại sản phẩm
for product in st.session_state['sales_by_product']:
    st.session_state['sales_by_product'][product] += np.random.uniform(0.005, 0.01) * st.session_state['sales_by_product'][product]

# Create Pie Chart: Sales by Product
product_labels = list(st.session_state['sales_by_product'].keys())
product_values = list(st.session_state['sales_by_product'].values())
fig2 = go.Figure(data=[go.Pie(labels=product_labels, values=product_values)])
fig2.update_layout(title="Số Lượng Bán Theo Loại Sản Phẩm")

# Display updated Pie charts
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# Prepare data for visualization
def prepare_data(data):
    pivot_data = data.pivot_table(
        index='Time', columns='Platform', values='Sales (15 min)', aggfunc='sum', fill_value=0
    )
    return pivot_data

# Adjust the dataset time
def adjust_time(data):
    min_time = data['Time'].min()
    current_time = pd.Timestamp.now().replace(second=0, microsecond=0)
    time_diff = current_time - min_time
    data['Time'] = data['Time'] + time_diff
    return data

current_day_sales = adjust_time(current_day_sales)

# Placeholder for the chart
chart_placeholder = st.empty()

data = st.session_state['data']

while True:
    # Filter data based on user selections
    filtered_data = filter_data(data, selected_platforms, selected_products)

    # Prepare data for chart
    pivot_data = prepare_data(filtered_data)

    # Select visible data based on zoom level
    if len(pivot_data) > zoom_level:
        visible_data = pivot_data.iloc[-zoom_level:]
    else:
        visible_data = pivot_data

    # Create Plotly figure
    fig = go.Figure()

    # Add stacked bar traces
    for platform in selected_platforms:
        if platform in visible_data.columns:
            fig.add_trace(go.Bar(
                x=visible_data.index,
                y=visible_data[platform],
                name=platform
            ))

    # Add line traces
    cumulative_data = visible_data.cumsum(axis=1)
    for i, platform in enumerate(selected_platforms):
        if platform in cumulative_data.columns:
            fig.add_trace(go.Scatter(
                x=visible_data.index,
                y=cumulative_data[platform],
                mode='lines+markers',
                name=f"{platform} (Đường)"
            ))

    fig.update_layout(
        barmode='stack',
        title="Biểu Đồ Doanh Số Theo Thời Gian",
        xaxis_title="Thời Gian",
        yaxis_title="Doanh Số",
        xaxis=dict(rangeslider=dict(visible=True), type="date"),
        template="plotly_white"
    )

    # Update the chart in the placeholder
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Simulate new data
    data = simulate_new_data(data)

    # Pause for real-time simulation
    time.sleep(5)
