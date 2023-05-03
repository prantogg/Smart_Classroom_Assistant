# Smart Classroom Assistant

## Overview

The Smart Classroom Assistant is a hybrid cloud application that utilizes both Amazon Web Services (AWS) and OpenStack resources to provide an image recognition service to users. The application allows users to send images, which are then run through a deep learning model to recognize the objects in the images. The architecture scales up and down automatically based on demand, making the service cost-effective.

## Architecture

The application consists of a web tier and an app tier. The web tier is hosted on an OpenStack Nova instance, while the app tier is hosted on AWS EC2 instances. The web tier receives image requests from users and forwards them to the app tier via an AWS SQS request queue. The app tier processes the images using a deep learning model, and the results are sent back to the web tier via an AWS SQS response queue.

The application utilizes the following AWS services:

- AWS EC2 (Elastic Cloud Compute)
- AWS SQS (Simple Queue Service)
- AWS S3 (Simple Storage Service)

## Autoscaling

Autoscaling is implemented to scale out and scale in the app tier based on demand. The number of app tier instances is scaled up and down based on the number of requests in the SQS request queue. A greedy approach is used, with one app tier EC2 instance created for every four user requests in the queue.

## Project Structure

The project is divided into two main components:

- Web Tier
- App Tier

### Web Tier

The web tier consists of the following files:

- main.py
- Controller.py
- sqs_utils.py
- ec2_utils.py
- upload.html

The main.py file hosts the web application where users can upload images. The uploaded images are converted to base64 format and pushed to the SQS request queue and S3 input bucket.

Controller.py handles autoscaling, creating worker app tier instances based on the SQS queue length.

sqs_utils.py and ec2_utils.py contain APIs for working with SQS queues and EC2 instances, respectively.

### App Tier

The app tier consists of the following files:

- app_tier.py
- image_classification.py
- sqs_utils.py

app_tier.py contains the API for uploading classification results to an S3 bucket and generating images in base64 format.

image_classification.py is a function that generates classification results using the provided deep learning model.

sqs_utils.py contains APIs for working with SQS queues, including sending and receiving messages and managing queue length.

## Setup and Execution

To set up and execute the Smart Classroom Assistant, follow these steps:

1. Create a NOVA compute instance on OpenStack using the web tier code.
2. Run `python3 main.py` to start the web application, allowing users to upload images.
3. Run `python3 Controller.py` to initiate autoscaling based on the SQS queue length.
4. App tier instances will be created as requests come in, running `python3 app_tier.py` on each instance.

## Contributors

- Pranav Toggi
- Riyank Mukhopadhyay
