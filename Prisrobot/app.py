from flask import Flask, render_template, request
from winecollector_api import hent_mest_solgte
from utils import sammenlign_med_konkurrenter

app = Flask(__name__)

@app.route('/')
def index():
    vine = hent_mest_solgte()
    resultater = sammenlign_med_konkurrenter(vine)
    return render_template('index.html', vine=resultater)

@app.route('/søg', methods=['GET', 'POST'])
def søg():
    resultater = []
    if request.method == 'POST':
        søgeord = request.form.get('vinnavn')
        resultater = sammenlign_med_konkurrenter([{'navn': søgeord}])
    return render_template('search.html', vine=resultater)

if __name__ == '__main__':
    app.run(debug=True)
