import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# Load the provided datasets
daily_sales = pd.read_csv('daily_sales.csv')
current_day_sales = pd.read_csv('current_day_sales.csv')

# Convert 'Date' and 'Time' columns to datetime
daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])
current_day_sales['Time'] = pd.to_datetime(current_day_sales['Time'])

# Function to simulate live data updates
def simulate_live_data():
    """
    Simulates live data updates by adding random sales data.
    """
    latest_time = current_day_sales['Time'].max() + pd.Timedelta(minutes=15)
    new_data = []
    for platform in ['Shopee', 'TikTok', 'Lazada']:
        for product in ['Búp bê Barbie', 'Labubu', 'Capybara', 'Gấu bông']:
            sales_15_min = np.random.randint(1, 20)
            new_data.append({'Time': latest_time, 'Platform': platform, 'Product': product, 'Sales (15 min)': sales_15_min})
    new_df = pd.DataFrame(new_data)
    return pd.concat([current_day_sales, new_df], ignore_index=True)

# Streamlit setup
st.title('Báo Cáo Tự Động Về Doanh Số')
st.write("Mô phỏng dữ liệu cập nhật mỗi 5 giây (tương ứng 15 phút thực tế).")

# Sidebar for filtering options
platform_filter = st.sidebar.multiselect("Chọn sàn TMĐT:", ['Shopee', 'TikTok', 'Lazada'], default=['Shopee', 'TikTok', 'Lazada'])
product_filter = st.sidebar.multiselect("Chọn sản phẩm:", ['Búp bê Barbie', 'Labubu', 'Capybara', 'Gấu bông'], default=['Búp bê Barbie', 'Labubu'])

# Filter data based on user selection
filtered_data = current_day_sales[current_day_sales['Platform'].isin(platform_filter) &
                                  current_day_sales['Product'].isin(product_filter)]

# Initialize the plot area
chart_placeholder = st.empty()

# Simulate live updates
data = filtered_data.copy()
for _ in range(20):
    # Update the data
    data = simulate_live_data()

    # Filter updated data
    filtered_data = data[data['Platform'].isin(platform_filter) &
                         data['Product'].isin(product_filter)]

    # Line chart for sales trend
    fig, ax = plt.subplots(figsize=(10, 6))
    for product in product_filter:
        product_data = filtered_data[filtered_data['Product'] == product]
        ax.plot(product_data['Time'], product_data['Sales (15 min)'], label=product)
    ax.set_title("Xu Hướng Doanh Số Theo Thời Gian")
    ax.set_xlabel("Thời Gian")
    ax.set_ylabel("Doanh Số (15 phút)")
    ax.legend()
    plt.xticks(rotation=45)

    # Display chart
    chart_placeholder.pyplot(fig)

    # Pause for 5 seconds to simulate real-time update
    time.sleep(5)
