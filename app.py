from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import simplejson as json
import time
import datetime

# imports for Bokeh plotting
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        #request was a post
        #ticker input
        app.vars['ticker'] = request.form['ticker']
        #pull data from Quandl api
        api_link = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?api_key=u6zoduyGLcrx-vMz5AMN' % (app.vars['ticker'])
        r = requests.get(api_link)
        data = json.loads(r.text)
        #store in pandas data frame and extract past month of data
        df = pd.DataFrame(data['dataset']['data'])
        df.columns = data['dataset']['column_names']
        x = df['Date'][0:22]
        x = [datetime.datetime.strptime(day,'%Y-%m-%d').date() for day in x]
        y = df['Close'][0:22]
        #create bokeh figure and push to front end
        fig = figure(title=app.vars['ticker'],x_axis_type='datetime',x_axis_label ='Date', y_axis_label='Closing Price')
        fig.line(x,y)
        script,div = components(fig)
        return render_template('graph.html',div=div,script=script)


if __name__ == '__main__':
  app.run(port=33507)
