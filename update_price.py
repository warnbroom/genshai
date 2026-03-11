import requests
import json

def get_prices():
    # THAY CÁI LINK DƯỚI ĐÂY BẰNG LINK BẠN VỪA COPY Ở BƯỚC 1
    api_url = "https://script.google.com/macros/s/AKfycbz01JmHtP9IuA2ut2EXDBBHj0_EsbSTR1pg8NGtAjM-GCkIxafKLvWXliccdE5G_4qMSA/exec"
    
    try:
        # Google Web App sẽ có lệnh chuyển hướng (Redirect), requests xử lý được
        response = requests.get(api_url, timeout=30)
        result = response.json()
        
        if result.get("RON95") and result.get("DO") and result["RON95"] > 0:
            print(f"Lấy giá thành công từ Google Proxy: {result}")
            
            with open('prices.json', 'w', encoding='utf-8') as f:
                json.dump({
                    "RON95": result["RON95"],
                    "DO": result["DO"]
                }, f, ensure_ascii=False, indent=4)
        else:
            print("Google Proxy chạy được nhưng Petrolimex vẫn đang chặn hoặc thay đổi giao diện.")
            
    except Exception as e:
        print(f"Lỗi kết nối đến Proxy: {e}")

if __name__ == "__main__":
    get_prices()
