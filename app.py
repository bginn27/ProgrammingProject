from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items')
def items():
    return render_template('items.html')

@app.route('/invoices')
def invoices():
    return render_template('invoices.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

if __name__ == '__main__':
    app.run()