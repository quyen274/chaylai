import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# Load the existing dataset
current_day_sales = pd.read_csv('current_day_sales.csv')
current_day_sales['Time'] = pd.to_datetime(current_day_sales['Time'])

# Load data
daily_sales = pd.read_csv('daily_sales.csv')
cart_data = pd.read_csv('items_in_cart.csv')
available_data = pd.read_csv('available_items.csv')

# Convert dates
daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])

platforms = current_day_sales['Platform'].unique()
products = current_day_sales['Product'].unique()

# Streamlit setup
st.set_page_config(page_title="Phân Tích Sản Phẩm và Báo Cáo Doanh Số", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Chọn trang", ["Phân Tích Sản Phẩm", "Báo Cáo Tự Động Về Doanh Số"])

if page == "Phân Tích Sản Phẩm":
    st.title("Phân Tích Sản Phẩm")

    # 1. Slice Biểu đồ tổng số lượng bán ra theo tháng
    daily_sales['Month'] = daily_sales['Date'].dt.to_period('M')
    sales_by_month = daily_sales.groupby(['Month', 'Platform'])['Daily Sales'].sum().unstack()

    fig_bar = px.bar(
        sales_by_month,
        x='Month',
        y='Daily Sales',
        color='Platform',
        barmode='group',
        title='Total Sales by Month and Platform',
        labels={'Daily Sales': 'Total Sales', 'Month': 'Month'},
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )

    fig_bar.update_layout(
        xaxis=dict(tickangle=45),  # Xoay nhãn trục X
        title=dict(x=0.5),  # Canh giữa tiêu đề
        margin=dict(l=20, r=20, t=50, b=20),  # Lề gọn hơn
        height=400,  # Chiều cao biểu đồ
    )

    # Hiển thị biểu đồ
    st.plotly_chart(fig_bar, use_container_width=True)

    # 2. Pie Chart: Sản phẩm trong giỏ hàng
    platforms = cart_data['Platform'].unique()
    
    for platform in platforms:
        platform_cart = cart_data[cart_data['Platform'] == platform]
        items_in_cart = platform_cart.groupby('Product')['Items in Cart'].sum().reset_index()
    
        # Tạo biểu đồ tròn cho từng nền tảng
        fig_pie = px.pie(
            items_in_cart,
            names='Product',
            values='Items in Cart',
            title=f'Cart Distribution on {platform}',
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
    
        fig_pie.update_traces(textinfo='percent+label')  # Hiển thị phần trăm và nhãn
        fig_pie.update_layout(
            title=dict(x=0.5),  # Canh giữa tiêu đề
            margin=dict(l=20, r=20, t=50, b=20),  # Lề gọn
            height=400,  # Chiều cao biểu đồ
        )

    # Hiển thị biểu đồ tròn
    st.plotly_chart(fig_pie, use_container_width=True)

elif page == "Báo Cáo Tự Động Về Doanh Số":
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

    # Initialize variables for real-time simulation
    current_revenue = 100_000_000  # Starting revenue
    current_cost = 60_000_000  # Starting cost
    sales_by_platform = {platform: 100 / len(platforms) for platform in platforms}
    sales_by_product = {product: 100 / len(products) for product in products}

    # Placeholder for KPI and Pie charts
    kpi_placeholder = st.empty()
    pie_placeholder1 = st.empty()
    pie_placeholder2 = st.empty()
    chart_placeholder = st.empty()

    # Initialize placeholders for Pie Charts
    if "fig1_placeholder" not in st.session_state:
        st.session_state["fig1_placeholder"] = st.empty()
    if "fig2_placeholder" not in st.session_state:
        st.session_state["fig2_placeholder"] = st.empty()

    def update_kpis_and_pies():
        global current_revenue, current_cost, sales_by_platform, sales_by_product

        # Update revenue and cost
        current_revenue += 150_000  # Increase revenue every 5 seconds
        current_cost = current_revenue * 0.6  # Cost is 60% of revenue
        profit = current_revenue - current_cost

        # Display KPIs
        with kpi_placeholder.container():
            st.metric("Tổng Doanh Thu", f"${current_revenue / 1e6:.2f}M", delta=f"+0.15M")
            st.metric("Tổng Lợi Nhuận", f"${profit / 1e6:.2f}M", delta=f"+{(150_000 - 150_000 * 0.6) / 1e6:.2f}M")

        # Update Pie chart: Số lượng bán trên từng sàn
        platform_total = sum(sales_by_platform.values())
        for platform in sales_by_platform:
            sales_by_platform[platform] += np.random.uniform(0.1, 2.0)
        platform_total_new = sum(sales_by_platform.values())
        for platform in sales_by_platform:
            sales_by_platform[platform] = (sales_by_platform[platform] / platform_total_new) * 100

        # Create Pie Chart: Sales by Platform
        platform_labels = list(sales_by_platform.keys())
        platform_values = list(sales_by_platform.values())
        fig1 = go.Figure(data=[go.Pie(labels=platform_labels, values=platform_values)])
        fig1.update_layout(title="Số Lượng Bán Theo Sàn")

        # Update Pie chart: Số lượng bán theo loại sản phẩm
        product_total = sum(sales_by_product.values())
        for product in sales_by_product:
            sales_by_product[product] += np.random.uniform(0.5, 1.0)
        product_total_new = sum(sales_by_product.values())
        for product in sales_by_product:
            sales_by_product[product] = (sales_by_product[product] / product_total_new) * 100

        # Create Pie Chart: Sales by Product
        product_labels = list(sales_by_product.keys())
        product_values = list(sales_by_product.values())
        fig2 = go.Figure(data=[go.Pie(labels=product_labels, values=product_values)])
        fig2.update_layout(title="Số Lượng Bán Theo Loại Sản Phẩm")

        # Update the Pie Charts directly
        with st.columns(2)[0]:  # First column for the first pie chart
            st.session_state["fig1_placeholder"].plotly_chart(fig1, use_container_width=True)
        with st.columns(2)[1]:  # Second column for the second pie chart
            st.session_state["fig2_placeholder"].plotly_chart(fig2, use_container_width=True)

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
    data = current_day_sales.copy()

    while True:
        # Update KPIs and Pie Charts
        update_kpis_and_pies()

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
