import boto3
from boto3 import client as boto3_client
import base64
import os
from app import app
import urllib.request
from PIL import Image
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from io import BytesIO
#from Controller import control

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

input_bucket_name = 'inputbucketgp3v2'
ACCESS_KEY = 'AKIARULFMIFKR62ZIRNX'
SECRET_KEY = '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'
dir_path = 'static/uploads'

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(path, bucket_name, name):
        s3 = boto3_client('s3')
        client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        )
        try:
                s3.upload_file(path, bucket_name, name)
        except Exception as e:
                print("Something Happened: ", e)
                return e
        return "{}".format(name)

        
@app.route('/')
def upload_form():
        return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
        if 'files[]' not in request.files:
                flash('No file part')
                return redirect(request.url)
        files = request.files.getlist('files[]')
        file_names = []

        
        sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        
        queue_url = 'https://sqs.us-east-1.amazonaws.com/112418636117/image_classification_request_queue'

        for file in files:
               
                print('file = ', file)
                print('file.filename = ', file.filename)
                if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_names.append(filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        
                #else:
                #       flash('Allowed image types are -> png, jpg, jpeg, gif')
                #       return redirect(request.url)

                #upload image to S3
                final_path = os.path.join(dir_path, file.filename)
                uploaded = upload_file_to_s3(final_path, input_bucket_name, file.filename) 

                # upload image name to SQS - conert image from JPEG to base64
                # img = Image.open(final_path)
                # img = img.tobytes()
             
                # my_string = str(base64.b64encode(img))
                response = sqs.send_message(QueueUrl=queue_url, MessageBody=file.filename)
                # response = sqs.send_message(QueueUrl=queue_url,
                # MessageAttributes={
                # 'ImageName': {
                # 'DataType': 'String',
                # 'StringValue': filename}
                # },
                # MessageBody=(my_string)
                # )

        #invoking controller.py
        #control()

        return render_template('upload.html', filenames=file_names)

@app.route('/display/<filename>')
def display_image(filename):
        print('display_image filename: ' + filename)
        return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=8080)
