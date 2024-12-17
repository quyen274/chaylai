import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
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

# Hàm gọi Facebook Graph API
def fetch_facebook_data(access_token, page_id, limit=10):
    url = f"https://graph.facebook.com/v12.0/{page_id}/posts"
    params = {
        "fields": "message,likes.summary(true),comments.summary(true)",
        "access_token": access_token,
        "limit": limit
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        posts = []
        for post in data.get("data", []):
            posts.append({
                "Message": post.get("message", "No content"),
                "Likes": post.get("likes", {}).get("summary", {}).get("total_count", 0),
                "Comments": post.get("comments", {}).get("summary", {}).get("total_count", 0)
            })
        return pd.DataFrame(posts)
    else:
        st.error(f"Lỗi: {response.status_code}, {response.json()}")
        return pd.DataFrame()

# Hàm mô phỏng dữ liệu Shopee
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

    # Facebook Crawl
    st.subheader("📊 Crawl Dữ Liệu Facebook")
    access_token = st.text_input("Access Token Facebook:", type="password")
    page_id = st.text_input("Page ID hoặc Page Name:")
    limit = st.slider("Số bài viết cần lấy:", 1, 50, 10)

    if st.button("Lấy Dữ Liệu Facebook"):
        if access_token and page_id:
            fb_data = fetch_facebook_data(access_token, page_id, limit)
            if not fb_data.empty:
                st.write("📊 Dữ Liệu Từ Facebook:")
                st.dataframe(fb_data)
                fb_data.to_csv("facebook_data.csv", index=False)
        else:
            st.warning("Vui lòng nhập Access Token và Page ID.")

    # Shopee Crawl (mock)
    st.subheader("🛒 Crawl Dữ Liệu Shopee (Mô Phỏng)")
    keyword = st.text_input("Nhập từ khóa tìm kiếm Shopee:", value="labubu")
    if st.button("Lấy Dữ Liệu Shopee"):
        shopee_data = mock_shopee_data(keyword)
        st.write("📊 Dữ Liệu Từ Shopee:")
        st.dataframe(shopee_data)
        shopee_data.to_csv("shopee_data.csv", index=False)

# Giao diện Phân Tích Dữ Liệu
if selected == "Phân Tích Dữ Liệu":
    st.title("📈 Phân Tích Dữ Liệu và Dự Đoán Xu Hướng")

    # Phân tích Facebook
    st.subheader("💬 Phân Tích Dữ Liệu Facebook")
    try:
        fb_data = pd.read_csv("facebook_data.csv")
        st.dataframe(fb_data)

        # Biểu đồ tương tác
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(fb_data["Message"], fb_data["Likes"], label="Likes", color="blue")
        ax.bar(fb_data["Message"], fb_data["Comments"], label="Comments", color="orange")
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
        fig, ax = plt.subplots(figsize=(3, 1))
        ax.bar(shopee_data["Product"], shopee_data["Sales"], color="skyblue")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Dự đoán xu hướng
        st.subheader("🔮 Dự Đoán Xu Hướng Doanh Số Shopee")
        future_sales = predict_trend(shopee_data, "Sales", days=5)
        future_days = np.arange(len(shopee_data), len(shopee_data) + 5)

        fig, ax = plt.subplots(figsize=(3, 1))
        ax.plot(shopee_data.index, shopee_data["Sales"], label="Actual Sales", marker='o')
        ax.plot(future_days, future_sales, label="Predicted Sales", linestyle="--", marker='o')
        ax.legend()
        st.pyplot(fig)
    except:
        st.warning("Chưa có dữ liệu Shopee. Vui lòng crawl dữ liệu trước.")
