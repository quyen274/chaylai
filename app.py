import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu

# Cấu hình Streamlit
st.set_page_config(page_title="Facebook & Shopee Analysis", layout="wide")

# Biến toàn cục để lưu dữ liệu
fb_data = pd.DataFrame()
shopee_data = pd.DataFrame()

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
        "Average Price": np.random.uniform(50000, 500000, days),
        "Total Sales": np.random.randint(500, 5000, days),
        "Positive Reviews": np.random.randint(300, 3000, days),
    }
    return pd.DataFrame(data)

# Hàm dự đoán xu hướng
def predict_trend(data, column, future_days=30):
    data["Day"] = range(len(data))
    X = data[["Day"]]
    y = data[column]

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.array(range(len(data), len(data) + future_days)).reshape(-1, 1)
    future_y = model.predict(future_X)
    return future_y

# Giao diện Crawl Dữ Liệu
if selected == "Crawl Dữ Liệu":
    st.title("🔗 Crawl Dữ Liệu Facebook & Shopee (Giả Lập)")

    # Facebook Crawl
    st.subheader("📊 Crawl Dữ Liệu Facebook")
    keyword_fb = st.text_input("Nhập từ khóa tìm kiếm Facebook:", value="labubu")
    posts_fb = st.slider("Số ngày cần tạo dữ liệu:", 1, 30, 30)
    if st.button("Crawl Dữ Liệu Facebook"):
        fb_data = generate_fake_facebook_data(posts_fb, keyword_fb)
        fb_data["Date"] = pd.to_datetime(fb_data["Date"])  # Chuyển Date về dạng datetime
        st.write(f"📊 Kết Quả Dữ Liệu Facebook với từ khóa '{keyword_fb}':")
        st.dataframe(fb_data)

    # Shopee Crawl
    st.subheader("🛒 Crawl Dữ Liệu Shopee")
    keyword_shopee = st.text_input("Nhập từ khóa tìm kiếm Shopee:", value="labubu")
    days_shopee = st.slider("Số ngày cần tạo dữ liệu Shopee:", 1, 30, 30)
    if st.button("Crawl Dữ Liệu Shopee"):
        shopee_data = generate_fake_shopee_data(days_shopee, keyword_shopee)
        shopee_data["Date"] = pd.to_datetime(shopee_data["Date"])  # Chuyển Date về dạng datetime
        st.write(f"📊 Kết Quả Dữ Liệu Shopee với từ khóa '{keyword_shopee}':")
        st.dataframe(shopee_data)

# Giao diện Phân Tích Dữ Liệu
if selected == "Phân Tích Dữ Liệu":
    st.title("📈 Phân Tích Dữ Liệu và Dự Đoán Xu Hướng")

    # Phân tích Facebook
    st.subheader("💬 Phân Tích Dữ Liệu Facebook")
    if not fb_data.empty:
        st.dataframe(fb_data)

        st.subheader("🔮 Dự Đoán Xu Hướng Facebook")
        future_days = 30
        likes_prediction = predict_trend(fb_data, "Likes", future_days)
        future_dates = pd.date_range(fb_data["Date"].max(), periods=future_days)

        fig, ax = plt.subplots()
        ax.plot(fb_data["Date"], fb_data["Likes"], label="Actual Likes", color="blue")
        ax.plot(future_dates, likes_prediction, "--", label="Predicted Likes", color="blue")
        plt.legend()
        st.pyplot(fig)
    else:
        st.warning("Chưa có dữ liệu Facebook. Vui lòng crawl dữ liệu trước.")

    # Phân tích Shopee
    st.subheader("🛒 Phân Tích Dữ Liệu Shopee")
    if not shopee_data.empty:
        st.dataframe(shopee_data)

        st.subheader("🔮 Dự Đoán Xu Hướng Shopee")
        price_prediction = predict_trend(shopee_data, "Average Price", 30)
        future_dates = pd.date_range(shopee_data["Date"].max(), periods=30)

        fig, ax = plt.subplots()
        ax.plot(shopee_data["Date"], shopee_data["Average Price"], label="Actual Avg Price", color="orange")
        ax.plot(future_dates, price_prediction, "--", label="Predicted Avg Price", color="orange")
        plt.legend()
        st.pyplot(fig)
    else:
        st.warning("Chưa có dữ liệu Shopee. Vui lòng crawl dữ liệu trước.")
