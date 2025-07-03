# LogLensApp/database_manager.py
import sqlite3
import os
from datetime import datetime
import re

# Lấy đường dẫn chính xác đến file DB
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_ROOT, 'database', 'logs.db')

def get_db_connection():
    """Tạo và trả về một kết nối đến database."""
    # Đảm bảo thư mục tồn tại
    db_dir = os.path.dirname(DB_PATH)
    os.makedirs(db_dir, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Khởi tạo bảng trong database nếu chưa tồn tại."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_line TEXT NOT NULL,
            ip TEXT,
            url TEXT,
            status INTEGER,
            timestamp TEXT, -- Lưu timestamp dưới dạng TEXT theo chuẩn ISO
            is_suspicious INTEGER,
            suspicion_score REAL
        );
    ''')
    conn.commit()
    conn.close()
    print(f"Database initialized and ready at: {os.path.abspath(DB_PATH)}")

def parse_and_format_timestamp(log_line):
    """Trích xuất và chuyển đổi timestamp sang định dạng ISO 8601."""
    # Pattern để trích xuất timestamp: [dd/Mon/YYYY:HH:MM:SS +0000]
    match = re.search(r'\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}\s[+\-]\d{4})\]', log_line)
    if not match:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Chuyển đổi từ '19/Jul/2024:07:24:21 +0000' sang đối tượng datetime
        dt_object = datetime.strptime(match.group(1), '%d/%b/%Y:%H:%M:%S %z')
        # Chuyển đổi sang định dạng text mà SQLite có thể sắp xếp được
        return dt_object.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, IndexError):
        # Nếu có lỗi, trả về thời gian hiện tại
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def insert_log_to_db(log_line, ip, url, status, is_suspicious, suspicion_score):
    """Chèn một dòng log đã được xử lý vào database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Lấy và định dạng lại timestamp từ log gốc
    formatted_timestamp = parse_and_format_timestamp(log_line)
    
    cursor.execute(
        '''
        INSERT INTO processed_logs (log_line, ip, url, status, timestamp, is_suspicious, suspicion_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (log_line, ip, url, status, formatted_timestamp, is_suspicious, suspicion_score)
    )
    conn.commit()
    conn.close()