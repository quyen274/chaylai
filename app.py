import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# Initialize the fake dataset for simulation
platforms = ['Shopee', 'TikTok', 'Lazada']
products = ['Búp bê Barbie', 'Labubu', 'Capybara', 'Gấu bông']

# Create an initial dataframe
current_day_sales = pd.DataFrame({
    'Time': pd.date_range(start=pd.Timestamp.now(), periods=4, freq='15T'),
    'Platform': np.random.choice(platforms, size=4),
    'Product': np.random.choice(products, size=4),
    'Sales (15 min)': np.random.randint(1, 20, size=4)
})

# Function to simulate live data updates
def simulate_live_data(data):
    """
    Simulates live data updates by adding random sales data.
    """
    latest_time = data['Time'].max() + pd.Timedelta(minutes=15)
    new_data = []
    for platform in platforms:
        for product in products:
            sales_15_min = np.random.randint(1, 20)
            new_data.append({'Time': latest_time, 'Platform': platform, 'Product': product, 'Sales (15 min)': sales_15_min})
    new_df = pd.DataFrame(new_data)
    return pd.concat([data, new_df], ignore_index=True)

# Streamlit setup
st.title('Báo Cáo Tự Động Về Doanh Số')
st.write("Mô phỏng dữ liệu cập nhật mỗi 5 giây (tương ứng 15 phút thực tế).")

# Sidebar for filtering options
platform_filter = st.sidebar.multiselect("Chọn sàn TMĐT:", platforms, default=platforms)
product_filter = st.sidebar.multiselect("Chọn sản phẩm:", products, default=products)

# Initialize the plot area
chart_placeholder = st.empty()

# Simulate live updates
data = current_day_sales.copy()
for _ in range(20):
    # Update the data
    data = simulate_live_data(data)

    # Filter updated data
    filtered_data = data[(data['Platform'].isin(platform_filter)) &
                         (data['Product'].isin(product_filter))]

    # Prepare data for stacked column chart
    pivot_data = filtered_data.pivot_table(
        index='Time', columns='Platform', values='Sales (15 min)', aggfunc='sum', fill_value=0
    )

    # Plot the data
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Stacked column chart
    pivot_data.plot(kind='bar', stacked=True, ax=ax1, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ax1.set_ylabel("Doanh Số (15 phút)")
    ax1.set_xlabel("Thời Gian")
    ax1.set_title("Biểu Đồ Kết Hợp: Doanh Số Theo Thời Gian")
    ax1.tick_params(axis='x', rotation=45)

    # Line chart for each platform
    ax2 = ax1.twinx()
    colors = ['#d62728', '#9467bd', '#8c564b']  # Different colors for lines
    for i, platform in enumerate(platforms):
        if platform in pivot_data.columns:
            ax2.plot(pivot_data.index, pivot_data[platform], marker='o', label=f"{platform}", linestyle='-', color=colors[i], linewidth=2)
    ax2.set_ylabel("Tổng Doanh Số")
    ax2.legend(loc="upper left", bbox_to_anchor=(1.05, 1))

    # Ensure line chart is visible
    ax2.set_ylim(0, max(pivot_data.sum(axis=1)) * 1.2)

    # Display chart
    chart_placeholder.pyplot(fig)

    # Pause for 5 seconds to simulate real-time update
    time.sleep(5)
