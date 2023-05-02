import boto3
import image_classification as IC
import base64
import time
from PIL import Image
from io import BytesIO
from Sqs_utils import send_message, get_message , delete_recent, get_queue_length 

Access_key_ID = 'AKIARULFMIFKR62ZIRNX'
Secret_access_key = '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'
input_bucket_name = 'inputbucketgp3v2'
output_bucket_name = 'outputprojgp3'

def upload_to_s3(image , image_name , prediction):
    s3 = boto3.client('s3',region_name='us-east-1',
                    aws_access_key_id=Access_key_ID, 
                    aws_secret_access_key=Secret_access_key)
    try:
        prediction_name = image_name[:-4] + " : " + prediction
        s3.upload_file(image , "face-recognition-s3-img" ,image_name)
        s3.upload_file(image , "face-recognition-s3-name" ,prediction_name) 
    except:
        print("Error while uploading")

def upload_response_s3(image_filename, classifier_output):
    s3 = boto3.client('s3',region_name='us-east-1',
                    aws_access_key_id=Access_key_ID, 
                    aws_secret_access_key=Secret_access_key)
    image_name = image_filename.split(".")[0]
    s3_response = s3.put_object(Bucket=output_bucket_name, Key=image_name, Body=str(image_name+", "+classifier_output))
    return s3_response
    
def download_from_s3(image_name):
    pwd = "/home/ubuntu/classifier/"+image_name
    s3 = boto3.client('s3',region_name='us-east-1',
                    aws_access_key_id=Access_key_ID, 
                    aws_secret_access_key=Secret_access_key)
    try:
            s3.download_file(input_bucket_name, image_name, image_name)
    except Exception as e:
            print("Something Happened: ", e)
            return e
    return "{}".format(image_name)


def generate_image(msg):
    decoded_string = Image.open(BytesIO(base64.b64decode(msg)))
    filename = 'some_image.jpg'
    with open(filename, 'wb') as f:
        f.write(decoded_string)
    f.close()

if __name__ == "__main__":
        while(True):
                queue_length = get_queue_length()
                #print(str(queue_length))
                if queue_length > 0:
                    image_name = get_message()
                    if (image_name != None):
                        print('\n\n')
                        print('\nReceived',image_name,'from request queue.')
                        
                        download_from_s3(image_name)
                        print('\nDownloaded',image_name,'from input bucket.')
                        
                        prediction = IC.classify(image_name)
                        print('\nImage',image_name,'classified as:',prediction+'.')
                        
                        upload_response_s3(image_name, prediction)
                        print('\nUploaded',image_name,'response to output bucket.')

                        send_message(prediction, image_name)
                        print('\nUploaded',image_name,'response to response queue.')



                                #generate_image(msg)
                                #prediction = IC.classify("some_image.jpg")
                #upload_to_s3("some_image.jpg" , image_name , prediction)
                #send_message(prediction, image_name)
                                
                        delete_recent(receipt_handle)

                #time.sleep(1)
                                #print(prediction)
                                #print(receipt_handle)
                else:
                    time.sleep(1)
            

        
    



