from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test_index.html')

@app.route('/test_submit', methods = ['GET', 'POST'])
def process_data():
    if request.method == 'POST':
        print (request.data)
        print (request.form)
        return request.form['nama']

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8000", debug=True,
		threaded=True, use_reloader=False)