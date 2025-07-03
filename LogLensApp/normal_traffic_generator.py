# log_generator.py
import time
import random

# Danh sách các dòng log mẫu để ghi vào file
LOG_SAMPLES = [
    '101.102.132.191 - - [03/Jun/2025:21:43:48 +0000] "POST /product/710/detail HTTP/1.1" 200 129 "https://twitter.com/" "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"',
    '45.67.195.50 - - [05/Jun/2025:08:03:24 +0000] "GET /search?q=phone HTTP/1.1" 200 2959 "-" "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"',
    '10.0.0.60 - - [08/Jun/2025:09:20:18 +0000] "POST /category/667/items HTTP/1.1" 500 2070 "https://example.com/blog/tech" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"',
    '45.67.4.40 - - [05/Jun/2025:20:28:29 +0000] "GET /search?q=headphones HTTP/1.1" 200 1074 "https://www.google.com/" "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"',
    '45.67.240.211 - - [03/Jun/2025:23:35:26 +0000] "POST /admin/login HTTP/1.1" 200 1334 "https://example.com/" "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"',
    '192.168.1.191 - - [05/Jun/2025:08:03:24 +0000] "POST /dashboard HTTP/1.1" 200 2195 "https://www.facebook.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"',
    '101.102.36.214 - - [08/Jun/2025:03:03:13 +0000] "GET /contact HTTP/1.1" 200 3036 "https://www.linkedin.com/" "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"',
    '101.102.199.122 - - [09/Jun/2025:13:30:26 +0000] "GET /admin/login HTTP/1.1" 200 1721 "https://www.facebook.com/" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"',
    '127.0.0.1 - - [20/Jul/2024:11:22:33 +0000] "GET /correct/test HTTP/1.1" 200 1234 "-" "-"',
    '248.39.111.167 - - [01/Oct/2024:18:44:48 +0000] "PUT /view?file=L3Byb2Mvc2VsZi9lbnZpcm9u HTTP/1.0" 405 1758 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
    '188.166.101.55 - - [15/Jun/2025:10:55:01 +0000] "GET /etc/passwd HTTP/1.1" 404 123 "-" "curl/7.64.1"',
    '10.0.1.5 - - [16/Jun/2025:11:05:10 +0000] "POST /api/v1/users/delete HTTP/1.1" 401 50 "-" "python-requests/2.25.1"'
]

LOG_FILE = "normal.log"

def generate_logs():
    """
    Hàm này chạy một vòng lặp vô tận để ghi log vào file.
    """
    print(f"Log generator started. Appending to '{LOG_FILE}'.")
    print("Press CTRL+C to stop.")
    
    while True:
        try:
            # Chọn ngẫu nhiên một dòng log từ danh sách
            log_line = random.choice(LOG_SAMPLES)
            
            # Mở file ở chế độ 'a' (append - ghi tiếp vào cuối)
            # encoding='utf-8' là một lựa chọn an toàn
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
            
            print(f"Appended: {log_line[:80]}...") # In ra log vừa ghi để theo dõi
            
            # Chờ một khoảng thời gian ngẫu nhiên từ 1 đến 5 giây
            sleep_time = random.uniform(0.01, 0.02)
            time.sleep(sleep_time)
            
        except KeyboardInterrupt:
            # Xử lý khi người dùng nhấn Ctrl+C
            print("\nLog generator stopped by user.")
            break
        except IOError as e:
            # Xử lý khi có lỗi ghi file
            print(f"\nError writing to file: {e}")
            break

if __name__ == "__main__":
    generate_logs()