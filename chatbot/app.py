from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector  

# Rasa sunucusunun API URL'si
RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

# Flask uygulaması
app = Flask(__name__)

# MySQL veritabanı bağlantısını kurun
db_connection = mysql.connector.connect(
    host='localhost',         
    user='root',              
    password='Hedaland430',   
    database='chatbot_db'     
)

# Ana sayfa route
@app.route('/')
def home():
    return render_template('index.html')

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json['message']
    print("User Message:", user_message)

    # Kullanıcı mesajını Rasa'ya gönder ve yanıt al
    rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
    rasa_response_json = rasa_response.json()

    bot_response = rasa_response_json[0]['text'] if rasa_response_json else "Üzgünüm, anlayamadım."

    # Veritabanına mesajları ve yanıtları kaydet
    save_conversation_to_db(user_message, bot_response)

    return jsonify({'response': bot_response})

# Veritabanına kaydetme fonksiyonu
def save_conversation_to_db(user_message, bot_response):
    try:
        cursor = db_connection.cursor()
        insert_query = "INSERT INTO conversations (user_message, bot_response) VALUES (%s, %s)"
        cursor.execute(insert_query, (user_message, bot_response))
        db_connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Kayıtları listeleme route
@app.route('/logs')
def show_logs():
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM conversations ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    cursor.close()
    return render_template('logs.html', logs=logs)

# Sohbet geçmişini silme route
@app.route('/delete_logs', methods=['POST'])
def delete_logs():
    try:
        cursor = db_connection.cursor()
        delete_query = "DELETE FROM conversations"
        cursor.execute(delete_query)
        db_connection.commit()
        cursor.close()
        return '', 204  # Başarılı işlem
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 'Error', 500  # Sunucu hatası

if __name__ == "__main__":
    app.run(debug=True, port=3000)
