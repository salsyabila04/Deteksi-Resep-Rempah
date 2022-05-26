from django.shortcuts import render
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask import Flask, render_template, request
from data import YouTubeData
import os
import joblib
import numpy as np
import smtplib
app = Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "foodsioncv@gmail.com"
app.config['MAIL_PASSWORD'] = "sandifoodsion12$"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route("/", methods=['GET', 'POST'])   

@app.route("/index", methods=['GET', 'POST'])   

def weight_prediction():
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        print(dict(request.form))
        weight_features = dict(request.form).values()
        weight_features = np.array([float(x) for x in weight_features])
        model = joblib.load(
            "modeling/Linear_regression_Prediksi_Berat_Badan.pkl")
        weight_features = [weight_features]
        print(weight_features)
        result = model.predict(weight_features)
        result = np.round(result, 2)
        result = float(result[0])
        return render_template('index.html', result=result)
    else:
        return "Unsupported Request Method"
    
@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == "POST":
        email = request.form['email']
        msg = request.form['message']
        subject = request.form['subject']
        
        message = Message(subject,sender="foodsioncv@gmail.com", recipients = [email])

        message.body = msg

        mail.send(message)

        success = "Pesan Terkirim"
        return render_template("result.html", success=success)

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        # getting the video details like images and channelid
        search = request.form['search']
        data = YouTubeData(search)
        snippet = data.get_channel_details(search)
        return render_template('search_page.html', message=snippet, search=search)
    else:
        return render_template('base.html')


@app.route('/get_more/<channelId>/<search>/<videoid>', methods=['GET', 'POST'])
def get_more(channelId, search, videoid):
    if request.method == 'GET':
        data = YouTubeData(search)
        content = data.get_channel_stats(channelId)

        snippet = data.get_videoDetails(videoid)

        stats = data.get_statistics(videoid)

        return render_template("moredata.html", subCount=content, statistics=stats, snippet=snippet)
    else:
        return render_template("index.html")  
if __name__ == '__main__':
    app.run(port=5000, debug=True)
