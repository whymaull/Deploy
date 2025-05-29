# from flask import Blueprint, request, jsonify
# from database.koneksi import get_connection # type: ignore
# from utils.prediksi_arima import get_stock_data, predict_arima # type: ignore
# import json

# predict_bp = Blueprint("predict", __name__)

# @predict_bp.route("/predict", methods=["POST"])
# def predict():
#     content = request.json
#     symbol = content.get("symbol")
#     user_id = content.get("user_id", "guest")
#     periods = content.get("periods", 7)

#     try:
#         data = get_stock_data(f"{symbol}.JK")
#         forecast = predict_arima(data, periods)

#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO riwayat_prediksi (user_id, symbol, periods, forecast) VALUES (%s, %s, %s, %s)",
#             (user_id, symbol, periods, json.dumps(forecast))
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()

#         return jsonify({"symbol": symbol, "forecast": forecast})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# from flask import Blueprint, request, jsonify
# from database.koneksi import get_connection
# from utils.prediksi_arima import get_stock_data, predict_arima
# import json

# predict_bp = Blueprint("predict", __name__)

# @predict_bp.route("/predict", methods=["POST"])
# def predict():
#     content = request.json
#     symbol = content.get("symbol")
#     user_id = content.get("user_id", "guest")
#     periods = content.get("periods", 7)
#     start_date = content.get("start_date")
#     period_type = content.get("period", "daily")

#     if not symbol or not start_date:
#         return jsonify({"error": "symbol dan start_date wajib diisi"}), 400

#     try:
#         # Ambil data historis sampai tanggal yang dipilih user
#         data = get_stock_data(f"{symbol}.JK", end=start_date)
        
#         if data is None:
#             return jsonify({
#                 "error": "Data historis tidak ditemukan untuk symbol dan tanggal tersebut."
#             }), 400

#         # Jalankan prediksi ARIMA
#         result = predict_arima(
#             data,
#             n_periods=periods,
#             start_date=start_date,
#             period_type=period_type
#         )

#         # Simpan hasil lengkap (termasuk tanggal dan nilai prediksi)
#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute("""
#             INSERT INTO riwayat_prediksi (user_id, symbol, start_date, period_type, periods, forecast)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (
#             user_id,
#             symbol,
#             start_date,
#             period_type,
#             periods,
#             json.dumps(result)
#         ))

#         conn.commit()
#         cursor.close()
#         conn.close()

#         return jsonify({
#             "symbol": symbol,
#             "forecast": result
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

from flask import Blueprint, request, jsonify
from database.koneksi import get_connection
from utils.prediksi_arima import get_stock_data, predict_arima
import json
import traceback
from datetime import datetime



predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        content = request.json
        print("[REQUEST]", content)

        symbol = content.get("symbol")
        user_id = content.get("user_id", "guest")
        periods = content.get("periods", 7)
        start_date = content.get("start_date")
        period_type = content.get("period", "daily")

        if not symbol or not start_date:
            return jsonify({"error": "symbol dan start_date wajib diisi"}), 400

        # Validasi tanggal
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Format tanggal salah. Gunakan YYYY-MM-DD"}), 400

        # Interval berdasarkan periode
        interval_map = {
            "daily": "1d",
            "weekly": "1wk",
            "monthly": "1mo"
        }
        interval = interval_map.get(period_type, "1d")

        print(f"[INFO] Mendapatkan data untuk {symbol} sampai {start_date} (interval: {interval})")
        data = get_stock_data(f"{symbol}.JK", end=start_date, interval=interval)

        if data is None or data.empty:
            return jsonify({"error": "Data historis tidak ditemukan."}), 400

        result = predict_arima(
            data,
            n_periods=periods,
            start_date=start_date,
            period_type=period_type
        )

        if not result:
            return jsonify({"error": "Prediksi gagal dijalankan."}), 500

        # Simpan ke DB
        conn = get_connection()
        conn.database = "prediksi_saham"
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO riwayat_prediksi (user_id, symbol, start_date, period_type, periods, forecast)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            symbol,
            start_date,
            period_type,
            periods,
            json.dumps(result)
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "symbol": symbol,
            "forecast": result
        })

    except Exception as e:
        print("[ERROR]", str(e))  # Log error di Railway
        traceback.print_exc() 
        return jsonify({"error": str(e)}), 500