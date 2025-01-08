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

# Streamlit setup
st.title('Báo Cáo Tự Động Về Doanh Số')
st.write("Biểu đồ kết hợp: cột chồng và đường hiển thị doanh số theo thời gian.")

# Sidebar for user selections
selected_platforms = st.sidebar.multiselect("Chọn nền tảng:", platforms, default=platforms)
selected_products = st.sidebar.multiselect("Chọn loại sản phẩm:", products, default=products)
zoom_level = st.sidebar.slider("Chọn số lượng cột hiển thị:", 10, 50, 20)

# Filter data based on user selection
def filter_data(data, platforms, products):
    return data[(data['Platform'].isin(platforms)) & (data['Product'].isin(products))]

# Prepare data for visualization
def prepare_data(data):
    pivot_data = data.pivot_table(
        index='Time', columns='Platform', values='Sales (15 min)', aggfunc='sum', fill_value=0
    )
    return pivot_data

# Adjust time for the current run (simulate live updates)
def adjust_time(data):
    min_time = data['Time'].min()
    current_time = pd.Timestamp.now().replace(second=0, microsecond=0)
    time_diff = current_time - min_time
    data['Time'] = data['Time'] + time_diff
    return data

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

# Adjust the dataset time
current_day_sales = adjust_time(current_day_sales)

# Placeholder for the chart
chart_placeholder = st.empty()

# Simulate data in real-time
data = current_day_sales.copy()

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

    # Update layout
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
