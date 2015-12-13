from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import simplejson as json

# imports for Bokeh plotting
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components

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

        # generate Bokeh HTML elements
        # create a `figure` object
        p = figure(title=app.vars['ticker'], plot_width=500,plot_height=400)
        # add the line
        p.line(x,y)
        # add axis labels
        p.xaxis.axis_label = "time"
        p.yaxis.axis_label = "price"
        # create the HTML elements to pass to template
        figJS,figDiv = components(p,CDN)

        return render_template('graph.html',y=y, figJS=figJS,figDiv=figDiv,ticker=app.vars['ticker'])

if __name__ == '__main__':
  app.run(port=33507,debug=True)
