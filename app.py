import streamlit as st
import pandas as pd
from playwright.sync_api import sync_playwright
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

# Cấu hình Streamlit
st.set_page_config(page_title="Shopee & Facebook Data", layout="wide")

# Thanh điều hướng
with st.sidebar:
    selected = option_menu(
        "Menu", ["Crawl Dữ Liệu", "Phân Tích Dữ Liệu"],
        icons=["cloud-download", "bar-chart"],
        menu_icon="cast",
        default_index=0,
    )

# Hàm crawl dữ liệu Shopee
def crawl_shopee(keyword="labubu", max_pages=1):
    product_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            for page_num in range(max_pages):
                url = f"https://shopee.vn/search?keyword={keyword}&page={page_num}"
                page.goto(url)
                page.wait_for_timeout(5000)  # Đợi 5s để trang tải xong

                # Lấy danh sách sản phẩm
                items = page.locator(".shopee-search-item-result__item")
                count = items.count()

                for i in range(count):
                    try:
                        title = items.nth(i).locator(".ie3A+n").inner_text()
                        price = items.nth(i).locator(".ZEgDH9").inner_text()
                        product_data.append({"Product": title, "Price": price})
                    except:
                        continue
            browser.close()
            return pd.DataFrame(product_data)
        except Exception as e:
            st.error(f"Lỗi: {e}")
            browser.close()
            return pd.DataFrame()

# Hàm mock crawl Facebook
def crawl_facebook(keyword="labubu", max_posts=10):
    return pd.DataFrame({
        "Post": [f"{keyword} is trending!", f"Get {keyword} now!", f"Limited stocks of {keyword}!"],
        "Likes": [120, 230, 310],
        "Comments": [10, 30, 50]
    })

# Giao diện Crawl Dữ Liệu
if selected == "Crawl Dữ Liệu":
    st.title("🛒 Crawl Dữ Liệu Shopee & Facebook")

    keyword = st.text_input("Nhập từ khóa tìm kiếm:", value="labubu")
    max_pages = st.slider("Số trang cần crawl:", 1, 5, 1)

    if st.button("Crawl Shopee"):
        shopee_data = crawl_shopee(keyword, max_pages)
        if not shopee_data.empty:
            st.write(f"Kết quả từ Shopee ({len(shopee_data)} sản phẩm):")
            st.dataframe(shopee_data)
            shopee_data.to_csv("shopee_data.csv", index=False)
        else:
            st.warning("Không có dữ liệu.")

    if st.button("Crawl Facebook"):
        facebook_data = crawl_facebook(keyword)
        if not facebook_data.empty:
            st.write(f"Kết quả từ Facebook ({len(facebook_data)} bài đăng):")
            st.dataframe(facebook_data)
            facebook_data.to_csv("facebook_data.csv", index=False)
        else:
            st.warning("Không có dữ liệu.")

# Giao diện Phân Tích Dữ Liệu
if selected == "Phân Tích Dữ Liệu":
    st.title("📊 Phân Tích Dữ Liệu")

    # Phân tích Shopee
    try:
        shopee_data = pd.read_csv("shopee_data.csv")
        st.subheader("🔥 Top Sản Phẩm Từ Shopee")
        st.dataframe(shopee_data)

        fig, ax = plt.subplots()
        top_products = shopee_data.head(10)
        ax.bar(top_products["Product"], top_products["Price"].str.replace("₫", "").astype(float))
        plt.xticks(rotation=90)
        st.pyplot(fig)
    except Exception:
        st.warning("Chưa có dữ liệu Shopee.")

    # Phân tích Facebook
    try:
        facebook_data = pd.read_csv("facebook_data.csv")
        st.subheader("💬 Tương Tác Facebook")
        st.dataframe(facebook_data)
        fig, ax = plt.subplots()
        ax.bar(facebook_data["Post"], facebook_data["Likes"], label="Likes")
        ax.bar(facebook_data["Post"], facebook_data["Comments"], label="Comments")
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(fig)
    except Exception:
        st.warning("Chưa có dữ liệu Facebook.")
