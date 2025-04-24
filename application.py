import pickle
from flask import Flask,request,render_template,url_for
import numpy as np 
import pandas as pd 
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application=Flask(__name__)

app=application

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/thanks')
def thanks():
    return "thanks"

@app.route('/predict',methods=['GET','POST'])
def predict_datapoints():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race/ethnicity'),
            parental_level_of_education=request.form.get('parental level of education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test preparation course'),
            reading_score=float(request.form.get('reading score')),
            writing_score=float(request.form.get('writing score'))
        )
        pred_df=data.get_data_as_frame()
        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        print(results)
        return render_template('home.html',result=results[0])



if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
