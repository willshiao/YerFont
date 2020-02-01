from flask import Flask, request

app = Flask(__name__)

@app.route('/svg', methods=['POST'])
def handle_svg():
    with open('test.svg', 'wb') as f:
        f.write(request.data)
    print('Data', request.data)
    return request.data
