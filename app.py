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
    st.title("🔗 Crawl Dữ Liệu Facebook")

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

# Giao diện Phân Tích Dữ Liệu
if selected == "Phân Tích Dữ Liệu":
    st.title("📊 Phân Tích Dữ Liệu Facebook")

    try:
        fb_data = pd.read_csv("facebook_data.csv")
        st.subheader("💬 Dữ Liệu Từ Facebook")
        st.dataframe(fb_data)

        # Biểu đồ tương tác hiện tại
        fig, ax = plt.subplots()
        ax.bar(fb_data["Message"], fb_data["Likes"], label="Likes", color="blue")
        ax.bar(fb_data["Message"], fb_data["Comments"], label="Comments", color="orange")
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(fig)

        # Biểu đồ dự đoán xu hướng
        st.subheader("📈 Dự Đoán Xu Hướng Lượt Thích Facebook")
        future_likes = predict_trend(fb_data, "Likes", days=5)
        future_days = np.arange(len(fb_data), len(fb_data) + 5)

        plt.figure(figsize=(10, 6))
        plt.plot(fb_data.index, fb_data["Likes"], label="Actual Likes", marker='o')
        plt.plot(future_days, future_likes, label="Predicted Likes", linestyle="--", marker='o')
        plt.title("Dự Đoán Xu Hướng Lượt Thích")
        plt.legend()
        st.pyplot(plt)
    except:
        st.warning("Chưa có dữ liệu Facebook. Vui lòng crawl dữ liệu trước.")
