import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from streamlit_option_menu import option_menu

# Cấu hình Streamlit
st.set_page_config(page_title="Phân Tích Xu Hướng Sản Phẩm", layout="wide")

# Thanh điều hướng
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Crawl Dữ Liệu", "Phân Tích Dữ Liệu"],
        icons=["cloud-download", "bar-chart"],
        menu_icon="cast",
        default_index=0,
    )

# Hàm crawl dữ liệu từ Shopee
def crawl_shopee(keyword="labubu", max_pages=1):
    product_data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        for page in range(max_pages):
            url = f"https://shopee.vn/search?keyword={keyword}&page={page}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Tìm tất cả sản phẩm
            items = soup.find_all("div", class_="shopee-search-item-result__item")
            for item in items:
                try:
                    title = item.find("div", class_="v-text").get_text()
                    sales = item.find("div", class_="v-badge").get_text() if item.find("div", class_="v-badge") else "0 sold"
                    product_data.append({"Product": title, "Sales": sales})
                except Exception:
                    continue
        
        return pd.DataFrame(product_data)
    except Exception as e:
        st.error(f"Lỗi khi crawl dữ liệu từ Shopee: {e}")
        return pd.DataFrame()

# Hàm giả lập crawl dữ liệu từ Facebook
def crawl_facebook(keyword="labubu", max_posts=50):
    # Đây là hàm giả lập. Để crawl thực tế, bạn cần sử dụng Facebook Graph API hoặc các công cụ phù hợp khác.
    return pd.DataFrame({
        "Post": [f"{keyword} is amazing!", f"Best gift for {keyword} lovers!", f"Limited {keyword} stocks!"],
        "Likes": [150, 230, 300],
        "Comments": [20, 35, 50]
    })

# Trang Crawl Dữ Liệu
if selected == "Crawl Dữ Liệu":
    st.title("🛒 Crawl Dữ Liệu Từ Shopee & Facebook")

    # Crawl từ Shopee
    st.subheader("🔗 Crawl từ Shopee")
    keyword = st.text_input("Nhập từ khóa tìm kiếm (ví dụ: labubu):", value="labubu")
    max_pages = st.slider("Số trang cần crawl:", 1, 5, 1)

    if st.button("Crawl Shopee"):
        shopee_data = crawl_shopee(keyword, max_pages)
        if not shopee_data.empty:
            st.write(f"Kết quả crawl từ Shopee ({len(shopee_data)} sản phẩm):")
            st.dataframe(shopee_data)
        else:
            st.warning("Không có dữ liệu từ Shopee.")

    # Crawl từ Facebook
    st.subheader("💬 Crawl từ Facebook")
    if st.button("Crawl Facebook"):
        facebook_data = crawl_facebook(keyword=keyword, max_posts=50)
        if not facebook_data.empty:
            st.write(f"Kết quả crawl từ Facebook ({len(facebook_data)} bài đăng):")
            st.dataframe(facebook_data)
        else:
            st.warning("Không có dữ liệu từ Facebook.")

# Trang Phân Tích Dữ Liệu
if selected == "Phân Tích Dữ Liệu":
    st.title("📈 Phân Tích Dữ Liệu Sản Phẩm")

    # Kiểm tra dữ liệu đã được crawl
    if 'shopee_data' in locals() and not shopee_data.empty:
        st.subheader("📊 Dữ Liệu Từ Shopee")
        st.dataframe(shopee_data)

        # Chuyển đổi cột Sales thành số nguyên
        shopee_data['Sales'] = shopee_data['Sales'].str.extract('(\d+)').astype(int)

        # Hiển thị tổng số sản phẩm và tổng lượt bán
        st.write(f"Tổng số sản phẩm: {len(shopee_data)}")
        st.write(f"Tổng lượt bán: {shopee_data['Sales'].sum()}")

        # Biểu đồ sản phẩm bán chạy nhất
        st.subheader("🔥 Top 10 Sản Phẩm Bán Chạy Nhất")
        top_products = shopee_data.sort_values(by='Sales', ascending=False).head(10)
        fig, ax = plt.subplots()
        ax.barh(top_products['Product'], top_products['Sales'], color='skyblue')
        ax.set_xlabel('Số Lượng Bán')
        ax.set_title('Top 10 Sản Phẩm Bán Chạy Nhất trên Shopee')
        st.pyplot(fig)
    else:
        st.warning("Chưa có dữ liệu từ Shopee. Vui lòng crawl dữ liệu trước.")

    # Kiểm tra dữ liệu từ Facebook
    if 'facebook_data' in locals() and not facebook_data.empty:
        st.subheader("💬 Dữ Liệu Từ Facebook")
        st.dataframe(facebook_data)

        # Biểu đồ tương tác trên Facebook
        st.subheader("👍 Tương Tác Trên Facebook")
        fig, ax = plt.subplots()
        ax.bar(facebook_data['Post'], facebook_data['Likes'], label='Likes', color='blue')

