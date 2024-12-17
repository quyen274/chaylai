import streamlit as st
import pandas as pd
import numpy as np
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

# Hàm tạo dữ liệu giả lập Facebook
def generate_fake_facebook_data():
    total_posts = np.random.randint(50, 100)
    total_likes = total_posts * np.random.randint(100, 500)
    total_comments = total_posts * np.random.randint(20, 200)
    total_shares = total_posts * np.random.randint(10, 100)
    
    return {
        "Tổng số bài đăng": total_posts,
        "Tổng số lượt thích": total_likes,
        "Tổng số lượt bình luận": total_comments,
        "Tổng số lượt chia sẻ": total_shares
    }

# Hàm tạo dữ liệu giả lập Shopee
def generate_fake_shopee_data():
    total_products = np.random.randint(100, 500)
    average_price = np.random.uniform(50000, 500000)
    total_sales = total_products * np.random.randint(1, 50)
    positive_reviews = total_products * np.random.uniform(0.6, 0.9)

    return {
        "Tổng số sản phẩm": total_products,
        "Giá trung bình": f"{average_price:.0f} VND",
        "Tổng số lượng mua": total_sales,
        "Tổng số đánh giá tích cực": int(positive_reviews)
    }

# Giao diện Crawl Dữ Liệu
if selected == "Crawl Dữ Liệu":
    st.title("🔗 Crawl Dữ Liệu Facebook & Shopee (Giả Lập)")

    # Crawl Facebook
    st.subheader("📊 Crawl Dữ Liệu Facebook")
    if st.button("Crawl Dữ Liệu Facebook"):
        fb_data = generate_fake_facebook_data()
        st.write("📊 Kết Quả Dữ Liệu Facebook:")
        st.table(pd.DataFrame([fb_data]))

    # Crawl Shopee
    st.subheader("🛒 Crawl Dữ Liệu Shopee")
    if st.button("Crawl Dữ Liệu Shopee"):
        shopee_data = generate_fake_shopee_data()
        st.write("📊 Kết Quả Dữ Liệu Shopee:")
        st.table(pd.DataFrame([shopee_data]))

# Giao diện Phân Tích Dữ Liệu
if selected == "Phân Tích Dữ Liệu":
    st.title("📈 Phân Tích Dữ Liệu Tổng Quan")

    # Phân tích Facebook
    st.subheader("💬 Phân Tích Dữ Liệu Facebook")
    fb_data = generate_fake_facebook_data()
    st.write("📊 Tổng Quan Dữ Liệu Facebook:")
    st.table(pd.DataFrame([fb_data]))

    # Biểu đồ tương tác Facebook
    st.subheader("📊 Biểu Đồ Tổng Quan Facebook")
    fb_labels = ["Likes", "Comments", "Shares"]
    fb_values = [fb_data["Tổng số lượt thích"], fb_data["Tổng số lượt bình luận"], fb_data["Tổng số lượt chia sẻ"]]
    st.bar_chart(pd.DataFrame({"Tương Tác Facebook": fb_values}, index=fb_labels))

    # Phân tích Shopee
    st.subheader("🛒 Phân Tích Dữ Liệu Shopee")
    shopee_data = generate_fake_shopee_data()
    st.write("📊 Tổng Quan Dữ Liệu Shopee:")
    st.table(pd.DataFrame([shopee_data]))

    # Biểu đồ doanh số Shopee
    st.subheader("📊 Biểu Đồ Tổng Quan Shopee")
    shopee_labels = ["Tổng số sản phẩm", "Tổng số lượng mua", "Tổng số đánh giá tích cực"]
    shopee_values = [shopee_data["Tổng số sản phẩm"], shopee_data["Tổng số lượng mua"], shopee_data["Tổng số đánh giá tích cực"]]
    st.bar_chart(pd.DataFrame({"Tổng Quan Shopee": shopee_values}, index=shopee_labels))
