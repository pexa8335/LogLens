# app.py - PHIÊN BẢN ĐẦY ĐỦ VÀ CHÍNH XÁC
import os
import sqlite3
import pandas as pd
from flask import Flask, render_template, jsonify, request, g
import shap
import numpy as np

from database_manager import get_db_connection
from predictor import LogPredictor
from parsinglog import parse_nginx_log
from feature_engineering import timestamp_features, status_features, referrer_features

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(APP_ROOT)
TEMPLATE_DIR = os.path.join(PARENT_DIR, 'Web')
STATIC_DIR = os.path.join(PARENT_DIR, 'Web', 'static')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

MODEL_PATH = os.path.join(APP_ROOT, 'catboost_model.joblib')
DB_PATH = os.path.join(APP_ROOT, 'database', 'logs.db')
app.config['DATABASE'] = DB_PATH
MODEL_COLUMNS = ['method', 'protocol', 'status', 'size', 'hour_of_day', 'day_of_week', 'is_weekend', 'part_of_day', 'hour_sin', 'hour_cos', 'day_of_week_sin', 'day_of_week_cos', 'time_since_last_event', 'status_is_client_error', 'status_is_server_error', 'status_is_success', 'status_is_redirect', 'size_is_zero', 'referrer_len', 'referrer_entropy', 'referrer_is_empty', 'referrer_domain', 'referrer_is_external_or_valid']
CATEGORICAL_FEATURES = ['method', 'protocol', 'part_of_day', 'referrer_domain']

try:
    log_predictor = LogPredictor(model_path=MODEL_PATH, model_columns=MODEL_COLUMNS, cat_features=CATEGORICAL_FEATURES)
    explainer = shap.TreeExplainer(log_predictor.model)
    expected_value = explainer.expected_value
    if isinstance(expected_value, np.ndarray):
        if expected_value.ndim == 0: base_value = float(expected_value)
        elif expected_value.ndim == 1 and len(expected_value) > 1: base_value = float(expected_value[1])
        else: base_value = float(expected_value.flatten()[0]) if expected_value.size > 0 else 0.0
    elif isinstance(expected_value, (float, int)): base_value = float(expected_value)
    else:
        print(f"app.py (WARNING): Unexpected type for explainer.expected_value: {type(expected_value)}. Setting base_value to 0.0.")
        base_value = 0.0
    print(f"SHAP Explainer initialized globally. Global Base Value: {base_value}")
except Exception as e:
    print(f"CRITICAL ERROR loading model or explainer: {e}")
    log_predictor = None; explainer = None; base_value = None
# === CÁC ROUTE HIỂN THỊ TRANG (PAGE ROUTES) ===
def get_db():
    if 'db' not in g:
        db_dir = os.path.dirname(app.config['DATABASE'])
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"Created database directory: {db_dir}")

        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_line TEXT NOT NULL,
                ip TEXT,
                url TEXT,
                status INTEGER,
                timestamp TEXT,
                is_suspicious INTEGER,
                suspicion_score REAL
            );
        ''')
        db.commit()
    print(f"Database initialized and ready at: {os.path.abspath(app.config['DATABASE'])}")

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')
    
@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/detect')
def detect_page(): return render_template('detect-anomaly.html')

@app.route('/analyze', methods=['POST'])
def analyze_logs():
    if log_predictor is None: return jsonify({"error": "Model not loaded"}), 503
    data = request.get_json()
    log_lines = data.get('log_line')
    if not log_lines or not isinstance(log_lines, list): return jsonify({"error": "Invalid input"}), 400
    try:
        predictions, probabilities = log_predictor.predict_from_logs(log_lines)
        if not predictions and log_lines: return jsonify({"error": "Could not parse any logs"}), 400
        results = [{"log_line": log_lines[i], "is_suspicious": int(predictions[i]), "suspicion_score": float(probabilities[i][1])} for i in range(len(predictions))]
        return jsonify(results)
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": "Internal error"}), 500

@app.route('/explain', methods=['POST'])
def explain_logs():
    if explainer is None: return jsonify({"error": "Explainer not loaded"}), 503
    data = request.get_json()
    log_lines = data.get('log_line')
    if not log_lines or not isinstance(log_lines, list) or len(log_lines) == 0: return jsonify({"error": "Invalid input"}), 400
    try:
        parsed_data = parse_nginx_log([log_lines[0]], as_dataframe=True)
        if parsed_data.empty: return jsonify({"error": "Could not parse log"}), 400
        df_featured = timestamp_features(parsed_data.copy())
        df_featured = status_features(df_featured.copy())
        df_featured = referrer_features(df_featured.copy())
        df_final_features = df_featured[MODEL_COLUMNS].copy()
        raw_shap_values = explainer.shap_values(df_final_features)
        shap_values_for_class_1 = raw_shap_values[1].tolist() if isinstance(raw_shap_values, list) and len(raw_shap_values) == 2 else raw_shap_values.tolist()
        return jsonify({"log_line": log_lines[0], "shap_values": shap_values_for_class_1[0], "base_value": base_value, "feature_names": MODEL_COLUMNS, "feature_values": df_final_features.iloc[0].to_dict()})
    except Exception as e:
        print(f"Explanation error: {e}")
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

# THAY THẾ TOÀN BỘ HÀM CŨ BẰNG HÀM NÀY TRONG app.py

@app.route('/dashboard_data')
def get_dashboard_data():
    conn = get_db_connection() # Sử dụng hàm kết nối từ database_manager.py
    
    # --- Phần tính toán thẻ Overview (giữ nguyên, đã đúng) ---
    stats_cursor = conn.execute('SELECT COUNT(id) as total, SUM(is_suspicious) as suspicious FROM processed_logs')
    stats_result = stats_cursor.fetchone()
    total_requests = stats_result['total'] if stats_result and stats_result['total'] else 0
    suspicious_requests = stats_result['suspicious'] if stats_result and stats_result['suspicious'] else 0
    
    # Dùng coalesce để tránh lỗi nếu không có log nào
    warnings_count_result = conn.execute(
        "SELECT COALESCE(COUNT(id), 0) FROM processed_logs WHERE is_suspicious = 1 AND suspicion_score > 0.90"
    ).fetchone()
    warnings_count = warnings_count_result[0]

    system_health = "Healthy"
    if total_requests > 0:
        anomaly_rate = (suspicious_requests / total_requests) * 100
        if anomaly_rate > 5: system_health = "Critical"
        elif anomaly_rate > 1: system_health = "Warning"

    # --- SỬA LỖI TRUY VẤN CHO BIỂU ĐỒ ---
    # Bỏ điều kiện lọc theo 'now', thay vào đó lấy 24 giờ có dữ liệu gần nhất
    traffic_data = conn.execute('''
        SELECT 
            strftime('%Y-%m-%d %H:00', timestamp) as hour,
            COUNT(id) as total,
            SUM(is_suspicious) as anomalies
        FROM processed_logs
        GROUP BY hour
        ORDER BY hour DESC 
        LIMIT 24 
    ''').fetchall()
    
    # Đảo ngược lại danh sách để hiển thị đúng thứ tự thời gian trên biểu đồ
    traffic_data.reverse()

    chart_labels = [row['hour'] for row in traffic_data]
    normal_traffic = [row['total'] - row['anomalies'] for row in traffic_data]
    anomalies_traffic = [row['anomalies'] for row in traffic_data]

    # --- TRUY VẤN BẢNG "RECENT ANOMALIES" (đã đúng, không cần sửa) ---
    recent_anomalies = conn.execute('''
    SELECT ip, url, status, timestamp, suspicion_score
    FROM processed_logs
    WHERE id IN (
        SELECT MAX(id)
        FROM processed_logs
        WHERE is_suspicious = 1
        GROUP BY log_line
    )
    ORDER BY id DESC
    LIMIT 5;
    ''').fetchall()

    conn.close() # Đóng kết nối sau khi truy vấn xong

    # --- Trả về dữ liệu JSON ---
    data = {
        'cards': {
            'total_requests': total_requests,
            'anomalies_detected': suspicious_requests,
            'warnings': warnings_count,
            'system_health': system_health
        },
        'chart': {
            'labels': chart_labels,
            'normal_data': normal_traffic,
            'anomalies_data': anomalies_traffic
        },
        'table': [dict(row) for row in recent_anomalies]
    }
    
    return jsonify(data)

@app.route('/log_result', methods=['POST'])
def log_result():
    """
    Endpoint này được worker gọi để LƯU KẾT QUẢ đã phân tích vào DB.
    """
    data = request.get_json()
    
    # Kiểm tra xem dữ liệu có hợp lệ không
    if not data or 'log_line' not in data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    db = get_db()
    cursor = db.cursor()
    
    # Trích xuất thông tin từ JSON mà worker gửi lên
    log_line = data.get('log_line')
    is_suspicious = data.get('is_suspicious')
    suspicion_score = data.get('suspicion_score')
    
    # Trích xuất các thông tin phụ từ log_line để lưu vào các cột tương ứng
    # (Bạn có thể dùng lại hàm parse_nginx_log ở đây nếu cần)
    parsed_info = parse_nginx_log([log_line], as_dataframe=True)
    ip = parsed_info['ip'].iloc[0] if not parsed_info.empty else 'N/A'
    url = parsed_info['url'].iloc[0] if not parsed_info.empty else 'N/A'
    status = parsed_info['status'].iloc[0] if not parsed_info.empty else 0
    
    # Lấy và định dạng lại timestamp
    from database_manager import parse_and_format_timestamp # Tái sử dụng hàm đã tạo
    formatted_timestamp = parse_and_format_timestamp(log_line)

    try:
        cursor.execute(
            '''
            INSERT INTO processed_logs (log_line, ip, url, status, timestamp, is_suspicious, suspicion_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (log_line, ip, url, status, formatted_timestamp, is_suspicious, suspicion_score)
        )
        db.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        db.rollback()
        print(f"Error inserting log to DB: {e}")
        return jsonify({"status": "error", "message": "Failed to save to database"}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)