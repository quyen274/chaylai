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

if 'total_sales' not in st.session_state:
    st.session_state['total_sales'] = current_day_sales['Sales (15 min)'].sum()

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

# Calculate KPIs
total_sales = filtered_data['Sales (15 min)'].sum()
total_cost = total_sales * 0.6  # Giả sử 60% doanh số là chi phí
total_profit = total_sales - total_cost

# Display KPIs
st.metric("Tổng Doanh Thu", f"${total_sales / 1e6:.2f}M", delta=f"+{(total_sales - st.session_state['total_sales']) / 1e6:.2f}M")
st.metric("Tổng Lợi Nhuận", f"${total_profit / 1e6:.2f}M", delta=f"-{total_cost / 1e6:.1f}M")
st.session_state['total_sales'] = total_sales

# Pie chart: Số lượng bán trên từng sàn
sales_by_platform = filtered_data.groupby('Platform')['Sales (15 min)'].sum()
fig1 = go.Figure(data=[go.Pie(labels=sales_by_platform.index, values=sales_by_platform.values)])
fig1.update_layout(title="Số Lượng Bán Theo Sàn")

# Pie chart: Số lượng bán theo loại sản phẩm
sales_by_product = filtered_data.groupby('Product')['Sales (15 min)'].sum()
fig2 = go.Figure(data=[go.Pie(labels=sales_by_product.index, values=sales_by_product.values)])
fig2.update_layout(title="Số Lượng Bán Theo Loại Sản Phẩm")

# Display charts
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# Prepare data for visualization
def prepare_data(data):
    pivot_data = data.pivot_table(
        index='Time', columns='Platform', values='Sales (15 min)', aggfunc='sum', fill_value=0
    )
    return pivot_data

# Prepare data for the main chart
pivot_data = prepare_data(filtered_data)
if len(pivot_data) > zoom_level:
    visible_data = pivot_data.iloc[-zoom_level:]
else:
    visible_data = pivot_data

# Main chart
fig3 = go.Figure()

# Add stacked bar traces
for platform in selected_platforms:
    if platform in visible_data.columns:
        fig3.add_trace(go.Bar(
            x=visible_data.index,
            y=visible_data[platform],
            name=platform
        ))

# Add line traces
cumulative_data = visible_data.cumsum(axis=1)
for i, platform in enumerate(selected_platforms):
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

# Display the main chart
st.plotly_chart(fig3, use_container_width=True)
