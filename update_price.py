import requests
from bs4 import BeautifulSoup
import json
import re
import time

def get_prices():
    # Thêm tham số thời gian vào URL để phá cache của máy chủ Petrolimex
    timestamp = int(time.time())
    url = f"https://www.petrolimex.com.vn/thong-tin-khach-hang.html?v={timestamp}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    
    try:
        # Sử dụng session để duy trì kết nối ổn định
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"Không thể truy cập website. Mã lỗi: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Lấy toàn bộ văn bản và xóa các khoảng trắng thừa
        full_text = soup.get_text(separator=' ', strip=True)
        
        # In một đoạn text ra log để debug trên GitHub Actions
        print(f"Dữ liệu quét được (trích đoạn): {full_text[:500]}...")

        data = {"RON95": 0, "DO": 0}

        # Tìm giá RON 95-V: Tìm số có dạng xx.xxx nằm sau cụm từ RON 95-V
        # Chúng ta tìm tất cả các số có định dạng giá tiền trong văn bản
        all_prices = re.findall(r'\d{2}\.\d{3}', full_text)
        
        # Cách tìm mới: Quét theo vị trí từ khóa
        # Xăng RON 95-V
        match_95 = re.search(r'RON 95-V.*?(\d{2}\.\d{3})', full_text)
        if match_95:
            data["RON95"] = int(match_95.group(1).replace('.', ''))
            
        # Dầu DO 0,001S-V
        match_do = re.search(r'0,001S-V.*?(\d{2}\.\d{3})', full_text)
        if match_do:
            data["DO"] = int(match_do.group(1).replace('.', ''))

        # KIỂM TRA LẠI: Nếu regex search thất bại, dùng fallback tìm theo mảng
        if data["RON95"] == 0 or data["DO"] == 0:
            print("Regex cụ thể thất bại, thử quét toàn bộ số...")
            if len(all_prices) >= 2:
                # Thường RON 95-V và DO nằm ở những vị trí đầu tiên của bảng giá
                # Tuy nhiên cách này hên xui hơn nên ưu tiên cách trên
                if data["RON95"] == 0: data["RON95"] = int(all_prices[0].replace('.', ''))
                if data["DO"] == 0: data["DO"] = int(all_prices[2].replace('.', ''))

        # Lưu kết quả
        with open('prices.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("KẾT QUẢ CUỐI CÙNG:", data)

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    get_prices()
