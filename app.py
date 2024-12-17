import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from streamlit_option_menu import option_menu

# Cấu hình Streamlit
st.set_page_config(page_title="Facebook & Shopee Analysis", layout="wide")

# Thanh điều hướng
with st.sidebar:
    selected = option_menu(
        "Menu", ["Crawl Dữ Liệu", "Phân Tích Dữ Liệu"],
        icons=["cloud-download", "bar-chart"],
        default_index=0,
    )

# Hàm giả lập dữ liệu Facebook
def fake_facebook_data(keyword="labubu", posts=10):
    return pd.DataFrame({
        "Message": [f"Bài viết {i} về {keyword}" for i in range(1, posts+1)],
        "Likes": np.random.randint(100, 1000, posts),
        "Comments": np.random.randint(20, 500, posts),
        "Shares": np.random.randint(10, 300, posts)
    })

# Hàm giả lập dữ liệu Shopee
def mock_shopee_data(keyword="labubu"):
    return pd.DataFrame({
        "Product": [f"{keyword} Doll {i}" for i in range(1, 11)],
        "Price": [i * 100000 for i in range(10, 20)],
        "Sales": [i * 10 for i in range(10, 20)]
    })

# Dự đoán xu hướng bằng Linear Regression
def predict_trend(data, column, days=5):
    data["Day"] = range(len(data))
    X = data[["Day"]]
    y = data[column]

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.array(range(len(data), len(data) + days)).reshape(-1, 1)
    predictions = model.predict(future_days)
    return predictions

# Giao diện Crawl Dữ Liệu
if selected == "Crawl Dữ Liệu":
    st.title("🔗 Crawl Dữ Liệu Facebook & Shopee")

    # Facebook Crawl (Giả lập)
    st.subheader("📊 Crawl Dữ Liệu Facebook (Giả Lập)")
    keyword_fb = st.text_input("Nhập từ khóa tìm kiếm Facebook:", value="labubu")
    posts = st.slider("Số bài viết cần lấy:", 1, 50, 10)

    if st.button("Lấy Dữ Liệu Facebook"):
        fb_data = fake_facebook_data(keyword_fb, posts)
        st.write("📊 Dữ Liệu Từ Facebook (Giả Lập):")
        st.dataframe(fb_data)

        # Lưu dữ liệu vào CSV
        fb_data.to_csv("facebook_data.csv", index=False)
        st.success("Dữ liệu đã được lưu thành công.")

    # Shopee Crawl (Giả lập)
    st.subheader("🛒 Crawl Dữ Liệu Shopee (Giả Lập)")
    keyword_shopee = st.text_input("Nhập từ khóa tìm kiếm Shopee:", value="labubu")

    if st.button("Lấy Dữ Liệu Shopee"):
        shopee_data = mock_shopee_data(keyword_shopee)
        st.write("📊 Dữ Liệu Từ Shopee (Giả Lập):")
        st.dataframe(shopee_data)

        # Lưu dữ liệu vào CSV
        shopee_data.to_csv("shopee_data.csv", index=False)
        st.success("Dữ liệu đã được lưu thành công.")

# Giao diện Phân Tích Dữ Liệu
if selected == "Phân Tích Dữ Liệu":
    st.title("📈 Phân Tích Dữ Liệu và Dự Đoán Xu Hướng")

    # Phân tích Facebook
    st.subheader("💬 Phân Tích Dữ Liệu Facebook")
    try:
        fb_data = pd.read_csv("facebook_data.csv")
        st.dataframe(fb_data)

        # Tổng quan dữ liệu
        st.write("**Tổng Số Bài Đăng:**", len(fb_data))
        st.write("**Tổng Số Likes:**", fb_data["Likes"].sum())
        st.write("**Tổng Số Comments:**", fb_data["Comments"].sum())
        st.write("**Tổng Số Shares:**", fb_data["Shares"].sum())

        # Biểu đồ tương tác
        st.subheader("📊 Biểu Đồ Tương Tác")
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(fb_data["Message"], fb_data["Likes"], label="Likes", color="blue")
        ax.bar(fb_data["Message"], fb_data["Comments"], label="Comments", color="orange")
        ax.bar(fb_data["Message"], fb_data["Shares"], label="Shares", color="green")
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(fig)

        # Dự đoán xu hướng
        st.subheader("🔮 Dự Đoán Xu Hướng Lượt Thích Facebook")
        future_likes = predict_trend(fb_data, "Likes", days=5)
        future_days = np.arange(len(fb_data), len(fb_data) + 5)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(fb_data.index, fb_data["Likes"], label="Actual Likes", marker='o')
        ax.plot(future_days, future_likes, label="Predicted Likes", linestyle="--", marker='o')
        ax.legend()
        st.pyplot(fig)
    except:
        st.warning("Chưa có dữ liệu Facebook. Vui lòng crawl dữ liệu trước.")

    # Phân tích Shopee
    st.subheader("🛒 Phân Tích Dữ Liệu Shopee")
    try:
        shopee_data = pd.read_csv("shopee_data.csv")
        st.dataframe(shopee_data)

        # Biểu đồ doanh số
        st.subheader("📊 Biểu Đồ Doanh Số")
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(shopee_data["Product"], shopee_data["Sales"], color="skyblue")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Dự đoán xu hướng
        st.subheader("🔮 Dự Đoán Xu Hướng Doanh Số Shopee")
        future_sales = predict_trend(shopee_data, "Sales", days=5)
        future_days = np.arange(len(shopee_data), len(shopee_data) + 5)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(shopee_data.index, shopee_data["Sales"], label="Actual Sales", marker='o')
        ax.plot(future_days, future_sales, label="Predicted Sales", linestyle="--", marker='o')
        ax.legend()
        st.pyplot(fig)
    except:
        st.warning("Chưa có dữ liệu Shopee. Vui lòng crawl dữ liệu trước.")
