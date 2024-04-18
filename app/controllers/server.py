from flask import Flask, render_template

app = Flask(__name__)

@app.route('/trading')
def trading():
    with open('trading.log', 'r') as f:
        content = f.read()
    return render_template('trading.html', content=content)



if __name__ == '__main__':
    app.run(host='localhost', port="8080", debug=True)