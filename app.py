import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
zoom_level = st.sidebar.slider("Chọn số lượng cột hiển thị:", 5, 50, 10)

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
start_index = 0

while True:
    # Filter data based on user selections
    filtered_data = filter_data(data, selected_platforms, selected_products)

    # Prepare data for chart
    pivot_data = prepare_data(filtered_data)

    # Scroll logic for zoom level
    if len(pivot_data) > zoom_level:
        start_index = len(pivot_data) - zoom_level
    visible_data = pivot_data.iloc[start_index:]

    # Plot combined chart
    fig, ax = plt.subplots(figsize=(12, 6))

    # Stacked column chart
    bar_width = 0.8
    bar_positions = np.arange(len(visible_data))
    visible_data.plot(kind='bar', stacked=True, ax=ax, alpha=0.8, width=bar_width, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ax.set_ylabel("Doanh Số (15 phút)")
    ax.set_xlabel("Thời Gian")
    ax.set_title("Biểu Đồ Kết Hợp: Doanh Số Theo Thời Gian")
    ax.tick_params(axis='x', rotation=45)
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(visible_data.index.strftime('%H:%M'))

    # Line chart based on the top of stacked bars
    cumulative_data = visible_data.cumsum(axis=1)
    for i, platform in enumerate(selected_platforms):
        if platform in cumulative_data.columns:
            platform_values = cumulative_data[platform].values
            ax.plot(
                bar_positions,  # Match bar positions for x-axis
                platform_values,  # Top of the stacked bar
                marker='o',
                linestyle='-',
                label=f"{platform} (Đường)",
                color=['#d62728', '#9467bd', '#8c564b'][i % len(['#d62728', '#9467bd', '#8c564b'])],
                linewidth=2
            )

    # Add legend
    ax.legend(loc="upper left")

    # Update the chart in the placeholder
    chart_placeholder.pyplot(fig, clear_figure=True)

    # Simulate new data
    data = simulate_new_data(data)

    # Pause for real-time simulation
    time.sleep(5)
