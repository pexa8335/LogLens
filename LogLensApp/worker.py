# worker.py (phiên bản gỡ lỗi và giải thích)
import time
import requests
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_FILE_PATH = "normal.log"
ANALYZE_API_ENDPOINT = "http://127.0.0.1:5000/analyze" 
LOG_RESULT_API_ENDPOINT = "http://127.0.0.1:5000/log_result" # NEW: Thêm endpoint cho lời giải thích
SUSPICION_EXPLANATION_THRESHOLD = 0.8 # NEW: Ngưỡng để yêu cầu giải thích (ví dụ: chỉ giải thích nếu điểm đáng ngờ >= 0.8)

class LogHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_position = 0
        self.log_file_abs_path = os.path.abspath(LOG_FILE_PATH)
        
        print(f"Worker is now watching for changes to: {self.log_file_abs_path}")

        if os.path.exists(LOG_FILE_PATH):
            try:
                with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
                    f.seek(0, 2)
                    self.last_position = f.tell()
                    print(f"Initial position for '{LOG_FILE_PATH}' set to the end of the file ({self.last_position} bytes).")
            except IOError as e:
                print(f"Could not initialize LogHandler: {e}")

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(LOG_FILE_PATH):
            print(f"Detected change in '{LOG_FILE_PATH}'. Processing new entries...")
            try:
                with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
                    f.seek(self.last_position)
                    new_lines = [line.strip() for line in f.readlines() if line.strip()]
                    self.last_position = f.tell()

                    if new_lines:
                        # 1. GỌI API /ANALYZE
                        try:
                            response = requests.post(ANALYZE_API_ENDPOINT, json={'log_line': new_lines})
                            response.raise_for_status() # Báo lỗi nếu status code là 4xx hoặc 5xx
                            
                            analysis_results = response.json()
                            print(f"Analyzed {len(analysis_results)} log(s) successfully.")

                            # 2. DUYỆT QUA TỪNG KẾT QUẢ VÀ GỬI ĐẾN API /LOG_RESULT
                            for result in analysis_results:
                                try:
                                    save_response = requests.post(LOG_RESULT_API_ENDPOINT, json=result)
                                    save_response.raise_for_status()
                                    print(f" > Saved log to DB: {result['log_line'][:50]}...")
                                except requests.exceptions.RequestException as e:
                                    print(f"ERROR: Failed to save result to DB. Reason: {e}")

                        except requests.exceptions.RequestException as e:
                            print(f"CRITICAL ERROR: Could not connect to API at {ANALYZE_API_ENDPOINT}. Details: {e}")
            
            except IOError as e:
                print(f"ERROR: Could not read log file: {e}")

def start_worker():
    print("LogLens Worker started. Watching for log changes...")
    
    if not os.path.exists(LOG_FILE_PATH):
        print(f"Log file '{LOG_FILE_PATH}' not found. Creating it.")
        open(LOG_FILE_PATH, 'a').close()

    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping worker...")
        observer.stop()
    
    observer.join()
    print("Worker stopped.")

if __name__ == "__main__":
    start_worker()