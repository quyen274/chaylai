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
st.write("Mô phỏng dữ liệu với khả năng phóng to và cuộn thanh kéo.")

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

# Prepare data for stacked column chart
pivot_data = display_data.pivot_table(
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

# Line chart for each platform on top of the bars
colors = ['#d62728', '#9467bd', '#8c564b']  # Different colors for lines
for i, platform in enumerate(platforms):
    if platform in pivot_data.columns:
        ax1.plot(pivot_data.index, pivot_data[platform], marker='o', label=f"{platform}", linestyle='-', color=colors[i], linewidth=2)

# Add legend
ax1.legend(loc="upper left", bbox_to_anchor=(1.05, 1))

# Display the chart
st.pyplot(fig)
