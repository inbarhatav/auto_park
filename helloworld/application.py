#!flask/bin/python
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import requests
import json
from flask import Flask, Response ,request, render_template
from helloworld.flaskrun import flaskrun
import requests 
import datetime
import boto3
from werkzeug.utils import secure_filename
from boto3.dynamodb.conditions import Key, Attr

application = Flask(__name__)

@application.route('/upload', methods=['GET','POST'])
def upload_s3():
    
    bucket = 'automaticparking'
    file_name = ''
    result = '0'
    
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # if get show page for upload
    if request.method == 'GET':
        return render_template('make_my_day.html')

    s3 = boto3.resource('s3', region_name = 'us-east-2')
    if request.files:
        file = request.files['user_file']
        file_name = secure_filename(file.filename) + time
        s3.Bucket(bucket).put_object(Key=file_name, Body=file)
    '''
    else:  
        response = request.get_json() 
        print(response)
        bucket = response['bucket'] # 'loggereast1'
        file_name = response['file_name'] + time # whatever name
        country = response['country']
        data = json.dumps(response)
        # to create a file the obdy needs to be of type bytes, hence the data.encode
        s3.Bucket(bucket).put_object(Key=file_name, Body=data.encode('utf-8'))
    '''
    img_res = detect_text(bucket, file_name).replace(' ', '')
    # img_res = int(float(img_res))
    print(img_res)
    my_ses = boto3.Session(region_name = 'us-east-2')
    
    dynamodb = my_ses.resource('dynamodb')
    table = dynamodb.Table('parking_auth')
    resp = table.query(KeyConditionExpression=Key('carid').eq(img_res))
    print('result is {0}'.format(resp['Count']))
    if resp['Count'] == 1:
        result = '1'
    
    return Response(result, mimetype='application/json', status=200)

def detect_text(bucket, key, max_labels=10, min_confidence=50, region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    s3 = boto3.resource('s3', region_name = 'us-east-1')
    
    image = s3.Object(bucket, key) # Get an Image from S3
    img_data = image.get()['Body'].read() # Read the image
    '''
    response = rekognition.detect_labels(
        Image={
            'Bytes': img_data
        },
        MaxLabels=max_labels,
		MinConfidence=min_confidence,
    )
    '''
    response = rekognition.detect_text(
        Image={
            'Bytes': img_data
        },
    )

    
    return json.dumps(response['TextDetections'][0]['DetectedText'])


@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello inbar and dor'}), mimetype='application/json', status=200)

@application.route('/get_ip', methods=['GET'])
def get_ip():
    return Response(json.dumps(get_ip_meta()), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
def get_ip_meta():
    user_ip = str(request.environ['REMOTE_ADDR'])
    service_url = 'http://ipinfo.io/{}'.format(user_ip) 
    return requests.get(service_url).json()
    
if __name__ == '__main__':
    flaskrun(application)
