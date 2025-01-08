import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# Initialize the fake dataset for simulation
platforms = ['Shopee', 'TikTok', 'Lazada']
products = ['Búp bê Barbie', 'Labubu', 'Capybara', 'Gấu bông']

# Create an initial dataframe
current_day_sales = pd.DataFrame({
    'Time': pd.date_range(start=pd.Timestamp.now(), periods=10, freq='15T'),
    'Platform': np.random.choice(platforms, size=10),
    'Product': np.random.choice(products, size=10),
    'Sales (15 min)': np.random.randint(1, 20, size=10)
})

# Streamlit setup
st.title('Báo Cáo Tự Động Về Doanh Số')
st.write("Biểu đồ liên tục cập nhật với dữ liệu mới, hiển thị cột chồng và đường cho từng sàn.")

# Sidebar for zooming options
zoom_level = st.sidebar.slider("Chọn số lượng cột hiển thị:", 5, 50, 10)

# Function to simulate live data updates
def simulate_live_data(data):
    """
    Simulates live data updates by adding random sales data.
    """
    latest_time = data['Time'].max() + pd.Timedelta(minutes=15)
    new_data = []
    for platform in platforms:
        sales_15_min = np.random.randint(1, 20)
        new_data.append({'Time': latest_time, 'Platform': platform, 'Sales (15 min)': sales_15_min})
    new_df = pd.DataFrame(new_data)
    return pd.concat([data, new_df], ignore_index=True)

# Prepare data for visualization
def prepare_data(data):
    pivot_data = data.pivot_table(
        index='Time', columns='Platform', values='Sales (15 min)', aggfunc='sum', fill_value=0
    )
    return pivot_data

# Initialize data and start scrolling
start_index = 0
data = current_day_sales.copy()

# Placeholder for the chart
chart_placeholder = st.empty()

# Main loop for live updates
while True:
    # Simulate live data
    data = simulate_live_data(data)

    # Prepare data for chart
    pivot_data = prepare_data(data)

    # Scroll logic for zoom level
    if len(pivot_data) > zoom_level:
        start_index = len(pivot_data) - zoom_level
    visible_data = pivot_data.iloc[start_index:]

    # Plot combined chart
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Stacked column chart
    visible_data.plot(kind='bar', stacked=True, ax=ax1, alpha=0.8, width=0.8, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ax1.set_ylabel("Doanh Số (15 phút)")
    ax1.set_xlabel("Thời Gian")
    ax1.set_title("Biểu Đồ Kết Hợp: Doanh Số Theo Thời Gian")
    ax1.tick_params(axis='x', rotation=45)

    # Line chart for each platform (overlayed on top of bars)
    for platform in platforms:
        if platform in visible_data.columns:
            ax1.plot(
                visible_data.index,
                visible_data[platform].cumsum(),  # Display cumulative data for trend
                marker='o',
                linestyle='-',
                label=f"{platform} (Đường)",
                linewidth=2
            )

    # Add legend
    ax1.legend(loc="upper left")

    # Update the chart in the placeholder
    chart_placeholder.pyplot(fig, clear_figure=True)

    # Pause for real-time simulation
    time.sleep(5)
