import requests
from bs4 import BeautifulSoup
import json

def get_prices():
    url = "https://www.petrolimex.com.vn/thong-tin-khach-hang.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tìm tất cả các hàng trong bảng dữ liệu
        rows = soup.find_all('tr')
        data = {}

        for row in rows:
            text = row.get_text()
            # Lấy giá Vùng 1 (thường là cột thứ 2 hoặc 3 tùy cấu trúc web)
            cols = row.find_all('td')
            if len(cols) >= 2:
                product_name = cols[0].get_text(strip=True)
                price_val = cols[1].get_text(strip=True).replace('.', '')
                
                if "RON 95-V" in product_name:
                    data["RON95"] = int(price_val)
                elif "DO 0,001S-V" in product_name:
                    data["DO"] = int(price_val)

        # Lưu kết quả
        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Cập nhật thành công:", data)

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    get_prices()
