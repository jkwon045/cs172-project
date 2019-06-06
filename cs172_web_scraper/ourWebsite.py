#import app
import flask
from flask import Flask, render_template, request
from wtforms import Form, StringField, SelectField
app = Flask(__name__)


from cs172_web_scraper.spiders.query import Searcher
@app.route('/')
def home():
    return render_template('mySite.html')

@app.route('/', methods=['POST'])
def home_post():
    user_query = request.form['search']
#test-case for building the table
#    qResults =[(1,1,"test1","test1c"), (2,2,"test2","test2c"), (3,3,"test3", "test3c")]
    qResults = Searcher.search(user_query)
    return render_template('resultsPage.html', query=query, result_list=qResults)


@app.route('/results', methods=['POST'])
def results():
    user_query = request.form['search']
    qResults = Searcher.search(user_query)
#test case for building the results table
#    qResults = [(1, 1, "test1", "test1c"), (2, 2, "test2", "test2c"), (3, 3, "test3", "test3c")]
    return render_template('resultsPage.html', query=query,result_list=qResults)


if __name__ == '__main__':
    app.run(debug = True)