import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
st.write("Mô phỏng dữ liệu kết hợp biểu đồ cột và đường trên cùng một biểu đồ.")

# Sidebar for filtering options
platform_filter = st.sidebar.multiselect("Chọn sàn TMĐT:", platforms, default=platforms)
product_filter = st.sidebar.multiselect("Chọn sản phẩm:", products, default=products)

# Sidebar for zooming and scrolling options
zoom_level = st.sidebar.slider("Chọn độ rộng hiển thị (số lượng cột):", 5, 50, 10)
data_window = st.sidebar.slider("Chọn vị trí thanh kéo:", 0, len(current_day_sales) - zoom_level, 0)

# Filter data based on user selection
filtered_data = current_day_sales[(current_day_sales['Platform'].isin(platform_filter)) &
                                  (current_day_sales['Product'].isin(product_filter))]

# Apply scrolling and zooming logic
display_data = filtered_data.iloc[data_window:data_window + zoom_level]

# Prepare data for combined chart
pivot_data = display_data.pivot_table(
    index='Time', columns='Platform', values='Sales (15 min)', aggfunc='sum', fill_value=0
)
total_sales = pivot_data.sum(axis=1)

# Plot the data
fig, ax = plt.subplots(figsize=(12, 6))

# Combined bar and line chart
pivot_data.plot(kind='bar', stacked=True, ax=ax, color=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=0.8)
ax.plot(total_sales.index, total_sales.values, color='red', marker='o', linewidth=2, label='Tổng Doanh Số')

# Customize labels and title
ax.set_ylabel("Doanh Số (15 phút)")
ax.set_xlabel("Thời Gian")
ax.set_title("Biểu Đồ Kết Hợp: Doanh Số Theo Thời Gian")
ax.tick_params(axis='x', rotation=45)
ax.legend(loc="upper left")

# Display the chart
st.pyplot(fig)
