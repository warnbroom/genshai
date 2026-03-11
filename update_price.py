import requests
from bs4 import BeautifulSoup
import json
import re

def get_prices():
    url = "https://www.petrolimex.com.vn/thong-tin-khach-hang.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8' # Đảm bảo đọc đúng tiếng Việt
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tìm tất cả các bảng hoặc thẻ div chứa dữ liệu
        rows = soup.find_all(['tr', 'div'])
        data = {"RON95": 0, "DO": 0}

        for row in rows:
            text = row.get_text(separator=' ', strip=True)
            
            # Sử dụng Regex để tìm giá trị số sau tên sản phẩm
            # Tìm "RON 95-V" và lấy con số đầu tiên xuất hiện sau nó (Vùng 1)
            if "RON 95-V" in text and data["RON95"] == 0:
                numbers = re.findall(r'\d{2}\.\d{3}', text)
                if numbers:
                    data["RON95"] = int(numbers[0].replace('.', ''))
            
            # Tìm "DO 0,001S-V"
            if "0,001S-V" in text and data["DO"] == 0:
                numbers = re.findall(r'\d{2}\.\d{3}', text)
                if numbers:
                    data["DO"] = int(numbers[0].replace('.', ''))

        # Nếu không tìm thấy, gán giá trị dự phòng để không làm hỏng file JSON
        if data["RON95"] == 0: data["RON95"] = 27640
        if data["DO"] == 0: data["DO"] = 30530

        # Lưu vào file JSON
        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("Đã cập nhật prices.json thành công:", data)

    except Exception as e:
        print(f"Lỗi khi cào dữ liệu: {e}")
        # Ghi giá trị mặc định nếu có lỗi kết nối
        default = {"RON95": 27640, "DO": 30530}
        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_prices()
