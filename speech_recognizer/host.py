
from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

# POST isteğine yanıt veren fonksiyon
@app.route('/api', methods=['POST'])
def api():
    # Gelen JSON verisini al
    file_name = request.json['file_name']


    # Socket'i oluştur
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Socket'i hedef IP adresi ve port numarasıyla bağla
    sock.connect(('http://localhost', 5000))
    # JSON verisini UTF-8 formatında encode et ve socket üzerinden gönder
    sock.sendall(json.dumps(file_name).encode('utf-8'))
    # Socket'i kapat
    sock.close()

    response = jsonify({'message': file_name + ' uploaded successfully'})
    # Başarılı yanıt döndürür.

    response.status_code = 201
    return response

    


if __name__ == '__main__':
    # Flask uygulamasını localhost IP adresi ve belirtilen port numarasıyla çalıştır
    app.run(host='0.0.0.0', port=5000)
