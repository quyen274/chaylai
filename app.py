import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Cấu hình Streamlit
st.set_page_config(page_title="Facebook & Shopee Growth Analysis", layout="wide")

# Hàm tạo dữ liệu giả lập Facebook theo ngày
def generate_fake_facebook_data(days=30):
    date_range = [datetime.now() - timedelta(days=i) for i in range(days)]
    data = {
        "Date": date_range,
        "Posts": np.random.randint(20, 100, days),
        "Likes": np.random.randint(100000, 2000000, days),
        "Comments": np.random.randint(20000, 400000, days),
        "Shares": np.random.randint(10000, 200000, days)
    }
    return pd.DataFrame(data)

# Hàm tạo dữ liệu giả lập Shopee theo ngày
def generate_fake_shopee_data(days=30):
    date_range = [datetime.now() - timedelta(days=i) for i in range(days)]
    total_products = 500  # Giả định tổng sản phẩm không đổi
    data = {
        "Date": date_range,
        "Products": total_products,
        "Average Price": np.random.uniform(50000, 500000, days),
        "Total Sales": np.random.randint(500, 5000, days),
        "Positive Reviews": np.random.randint(300, 3000, days)
    }
    return pd.DataFrame(data)

# Dự đoán tăng trưởng bằng Linear Regression
def predict_trend(data, column, future_days=30):
    data["Day"] = range(len(data))
    X = data[["Day"]]
    y = data[column]

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.array(range(len(data), len(data) + future_days)).reshape(-1, 1)
    future_y = model.predict(future_X)
    return future_y

# Giao diện Streamlit
st.title("📈 Phân Tích và Dự Đoán Tăng Trưởng Facebook & Shopee")

# Dữ Liệu Facebook
st.subheader("💬 Phân Tích Dữ Liệu Facebook")
fb_data = generate_fake_facebook_data()
st.write("📊 Dữ Liệu Facebook Trong 30 Ngày:")
st.dataframe(fb_data)

# Dự đoán xu hướng Facebook
st.subheader("🔮 Dự Đoán Xu Hướng Facebook Trong Tháng Tiếp Theo")
future_days = 30
likes_prediction = predict_trend(fb_data, "Likes", future_days)
comments_prediction = predict_trend(fb_data, "Comments", future_days)
shares_prediction = predict_trend(fb_data, "Shares", future_days)

# Vẽ biểu đồ dự đoán
future_dates = pd.date_range(fb_data["Date"].min(), periods=30 + future_days)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(fb_data["Date"], fb_data["Likes"], label="Actual Likes", color="blue")
ax.plot(future_dates[-future_days:], likes_prediction, "--", label="Predicted Likes", color="blue")
ax.plot(fb_data["Date"], fb_data["Comments"], label="Actual Comments", color="orange")
ax.plot(future_dates[-future_days:], comments_prediction, "--", label="Predicted Comments", color="orange")
ax.plot(fb_data["Date"], fb_data["Shares"], label="Actual Shares", color="green")
ax.plot(future_dates[-future_days:], shares_prediction, "--", label="Predicted Shares", color="green")
plt.legend()
st.pyplot(fig)

# Dữ Liệu Shopee
st.subheader("🛒 Phân Tích Dữ Liệu Shopee")
shopee_data = generate_fake_shopee_data()
st.write("📊 Dữ Liệu Shopee Trong 30 Ngày:")
st.dataframe(shopee_data)

# Dự đoán xu hướng Shopee
st.subheader("🔮 Dự Đoán Xu Hướng Shopee Trong Tháng Tiếp Theo")
price_prediction = predict_trend(shopee_data, "Average Price", future_days)
sales_prediction = predict_trend(shopee_data, "Total Sales", future_days)
reviews_prediction = predict_trend(shopee_data, "Positive Reviews", future_days)

# Vẽ biểu đồ dự đoán Shopee
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(shopee_data["Date"], shopee_data["Average Price"], label="Actual Avg Price", color="blue")
ax.plot(future_dates[-future_days:], price_prediction, "--", label="Predicted Avg Price", color="blue")
ax.plot(shopee_data["Date"], shopee_data["Total Sales"], label="Actual Total Sales", color="orange")
ax.plot(future_dates[-future_days:], sales_prediction, "--", label="Predicted Total Sales", color="orange")
ax.plot(shopee_data["Date"], shopee_data["Positive Reviews"], label="Actual Reviews", color="green")
ax.plot(future_dates[-future_days:], reviews_prediction, "--", label="Predicted Reviews", color="green")
plt.legend()
st.pyplot(fig)

st.write("🔍 **Kết Luận**: Biểu đồ dự đoán giúp đánh giá khả năng tăng trưởng tương lai dựa trên dữ liệu trong 30 ngày qua.")
