import requests
import json
import re

def get_prices():
    # Sử dụng proxy trung gian để tránh bị Petrolimex chặn IP từ GitHub
    target_url = "https://www.petrolimex.com.vn/thong-tin-khach-hang.html"
    proxy_url = f"https://api.allorigins.win/get?url={target_url}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(proxy_url, headers=headers, timeout=30)
        if response.status_code != 200:
            raise Exception("Không thể kết nối qua Proxy")
            
        # Dữ liệu từ AllOrigins nằm trong trường 'contents'
        full_html = response.json().get('contents', '')
        
        # Làm sạch văn bản để quét số
        clean_text = " ".join(full_html.split())
        
        # Giá trị mặc định mới (Số lạ để bạn biết nếu nó bị lỗi)
        data = {"RON95": 11111, "DO": 22222} 

        # Tìm kiếm giá RON 95-V
        # Chúng ta tìm cụm từ "95-V" và lấy số XX.XXX đầu tiên sau nó
        ron_match = re.search(r"95-V.*?(\d{2}\.\d{3})", clean_text)
        if ron_match:
            data["RON95"] = int(ron_match.group(1).replace('.', ''))
            
        # Tìm kiếm giá DO 0,001S-V
        do_match = re.search(r"0,001S-V.*?(\d{2}\.\d{3})", clean_text)
        if do_match:
            data["DO"] = int(do_match.group(1).replace('.', ''))

        # Log kết quả ra console của GitHub để kiểm tra
        print(f"Dữ liệu quét được từ Petrolimex: {data}")

        # Ghi vào file JSON
        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Lỗi thực thi: {e}")
        # Nếu lỗi, giữ nguyên giá cũ hoặc để giá nhận biết lỗi
        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump({"RON95": 0, "DO": 0}, f)

if __name__ == "__main__":
    get_prices()
