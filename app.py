import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu

# Cấu hình Streamlit
st.set_page_config(page_title="Facebook & Shopee Analysis", layout="wide")

# Sử dụng session_state để lưu dữ liệu giữa các thao tác
if "fb_data" not in st.session_state:
    st.session_state.fb_data = None
if "shopee_data" not in st.session_state:
    st.session_state.shopee_data = None

# Thanh điều hướng
with st.sidebar:
    selected = option_menu(
        "Menu", ["Crawl Dữ Liệu", "Phân Tích Dữ Liệu"],
        icons=["cloud-download", "bar-chart"],
        default_index=0,
    )

# Hàm tạo dữ liệu giả lập Facebook
def generate_fake_facebook_data(days=30, keyword="labubu"):
    date_range = [datetime.now() - timedelta(days=i) for i in range(days)]
    data = {
        "Date": date_range,
        "Posts": np.random.randint(20, 100, days),
        "Likes": np.random.randint(100000, 2000000, days),
        "Comments": np.random.randint(20000, 400000, days),
        "Shares": np.random.randint(10000, 200000, days),
    }
    return pd.DataFrame(data)

# Hàm tạo dữ liệu giả lập Shopee
def generate_fake_shopee_data(days=30, keyword="labubu"):
    date_range = [datetime.now() - timedelta(days=i) for i in range(days)]
    total_products = 500
    data = {
        "Date": date_range,
        "Products": total_products,
        "Average Price": np.random.uniform(400000, 600000, days),
        "Total Sales": np.random.randint(500, 5000, days),
        "Positive Reviews": np.random.randint(300, 3000, days),
    }
    return pd.DataFrame(data)

# Hàm dự đoán số lượng bán biến động ngẫu nhiên
def predict_random_trend(data, column, future_days=30):
    base_value = data[column].iloc[-1]
    predictions = []
    for i in range(future_days):
        change = np.random.randint(-200, 200)  # Biến động ngẫu nhiên
        base_value = max(base_value + change, 0)  # Không cho phép âm
        predictions.append(base_value)
    return predictions

# Giao diện Crawl Dữ Liệu
if selected == "Crawl Dữ Liệu":
    st.title("🔗 Crawl Dữ Liệu Facebook & Shopee (Giả Lập)")

    # Facebook Crawl
    st.subheader("📊 Crawl Dữ Liệu Facebook")
    keyword_fb = st.text_input("Nhập từ khóa tìm kiếm Facebook:", value="labubu")
    posts_fb = st.slider("Số ngày cần tạo dữ liệu:", 1, 30, 30)
    if st.button("Crawl Dữ Liệu Facebook"):
        st.session_state.fb_data = generate_fake_facebook_data(posts_fb, keyword_fb)
        st.success("Dữ liệu Facebook đã được tạo thành công!")

    # Shopee Crawl
    st.subheader("🛒 Crawl Dữ Liệu Shopee")
    keyword_shopee = st.text_input("Nhập từ khóa tìm kiếm Shopee:", value="labubu")
    days_shopee = st.slider("Số ngày cần tạo dữ liệu Shopee:", 1, 30, 30)
    if st.button("Crawl Dữ Liệu Shopee"):
        st.session_state.shopee_data = generate_fake_shopee_data(days_shopee, keyword_shopee)
        st.success("Dữ liệu Shopee đã được tạo thành công!")

# Giao diện Phân Tích Dữ Liệu
if selected == "Phân Tích Dữ Liệu":
    st.title("📈 Phân Tích Dữ Liệu và Dự Đoán Xu Hướng")

    # Phân tích Facebook
    st.subheader("💬 Phân Tích Dữ Liệu Facebook")
    if st.session_state.fb_data is not None:
        fb_data = st.session_state.fb_data
        st.dataframe(fb_data)

        st.subheader("📊 Biểu Đồ Tách Riêng Facebook")
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))

        axs[0, 0].bar(fb_data["Date"], fb_data["Posts"], color="blue")
        axs[0, 0].set_title("Số Bài Đăng")

        axs[0, 1].bar(fb_data["Date"], fb_data["Likes"], color="green")
        axs[0, 1].set_title("Số Lượt Thích")

        axs[1, 0].bar(fb_data["Date"], fb_data["Comments"], color="orange")
        axs[1, 0].set_title("Số Bình Luận")

        axs[1, 1].bar(fb_data["Date"], fb_data["Shares"], color="red")
        axs[1, 1].set_title("Số Chia Sẻ")

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Chưa có dữ liệu Facebook. Vui lòng crawl dữ liệu trước.")

    # Phân tích Shopee
    st.subheader("🛒 Phân Tích Dữ Liệu Shopee")
    if st.session_state.shopee_data is not None:
        shopee_data = st.session_state.shopee_data
        st.dataframe(shopee_data)

        st.subheader("📊 Biểu Đồ Tách Riêng Shopee")
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))

        ax[0].bar(shopee_data["Date"], shopee_data["Total Sales"], color="blue")
        ax[0].set_title("Tổng Số Lượng Bán")

        ax[1].bar(shopee_data["Date"], shopee_data["Positive Reviews"], color="green")
        ax[1].set_title("Số Đánh Giá Tích Cực")

        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("🔮 Dự Đoán Số Lượng Có Thể Bán")
        future_days = 30
        sales_prediction = predict_random_trend(shopee_data, "Total Sales", future_days)
        future_dates = pd.date_range(shopee_data["Date"].max(), periods=future_days)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(future_dates, sales_prediction, color="purple")
        plt.title("Dự Đoán Số Lượng Bán Trong 30 Ngày Tiếp Theo")
        st.pyplot(fig)
    else:
        st.warning("Chưa có dữ liệu Shopee. Vui lòng crawl dữ liệu trước.")
