from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import simplejson as json

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
        app.vars['ticker'] = request.form['ticker']
        api_link = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?api_key=u6zoduyGLcrx-vMz5AMN' % (app.vars['ticker'])
        r = requests.get(api_link)
        data = json.loads(r.text)
        df = pd.DataFrame(data['dataset']['data'])
        df.columns = data['dataset']['column_names']
        x = df['Date'][0:22]
        y = df['Close'][0:22]

        fig = figure(title=app.vars['ticker'])
        fig.line(x,y)
        script,div = components(fig)
        return render_template('graph.html',div=div,script=script)


if __name__ == '__main__':
  app.run(port=33507,debug=True)
