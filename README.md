# CloudComputing_Clever_Photo_Album #

## Overview ##
Customer Service is a core service for a lot of businesses around the world, and it is getting disrupted at the moment by Natural Language Processing-powered applications. The [Clever_Photo_Album](https://cloud-computing-a2-b1.s3.amazonaws.com/index.html) is a serverless, micro service-driven web application that offers users an intelligent album. It not only allows users to upload their photos but search by natural language. Besides, this album supports customized labels assigned by users.

## Demo ##
![image](https://github.com/tim-kao/CloudComputing_Clever_Photo_Album/blob/main/demo/cat_and_dog.png)

## Application (Language & Tools) ##
1) Frontend: CSS, HTML, JavaScript
2) Backend: AWS Serverless ([S3](https://aws.amazon.com/s3/), [Lambda](https://aws.amazon.com/lambda/), [API Gateway](https://aws.amazon.com/apigateway/), [Lex](https://aws.amazon.com/lex/), [SQS](https://aws.amazon.com/sqs/), [SNS](https://aws.amazon.com/sns/), [DynamoDB](https://aws.amazon.com/dynamodb/), [ElasticSearch](https://aws.amazon.com/es/), [Codebuild](https://docs.aws.amazon.com/codebuild/), [Cloudformation](https://aws.amazon.com/cloudformation/)), Swagger API, PyThon


## Architecture ##
![image](https://github.com/tim-kao/CloudComputing_Clever_Photo_Album/blob/main/demo/architecture.png)
1) User -> Frontend (chat.html / AWS S3): user input "hello" to initiate the conversation
2) Frontend -> API: send user's messages to API.
3) API -> 
4) LF1 -> 
5) LF2 -> 
6) Lex -> Retrieve objects from natural language


## Description ##
#### 1) [S3](https://aws.amazon.com/s3/)
- Store the frontend files.
- Generate SDK from AWS API Gateway and store it into js folder.
- chat.js file needs modification.
- Create CORS policy.

#### 2) [API Gateway](https://aws.amazon.com/apigateway/)
- Create a new API by importing swagger API.
- Set POST method and integrate Lambda function LF0 with it.
- Set OPTIONS method and its response method with HTTP status 200.
- Enable CORS.
- Deploy API.
- Generate SDK for frontend.

#### 3) [Lambda](https://aws.amazon.com/lambda/) - LF0
- Receive messages from the frontend user.
- Direct messages to Dining Chatbot in Lex.

#### 4) [Lex](https://aws.amazon.com/lex/)
- Create a Dining Chatbot with three intents (GreetingIntent, DiningSuggestionsIntent, ThankYouIntent).
- Set up user utterances and slots in each intents for interaction conversation. 
- Integrate with Lambda function LF1.
- Publish the chatbot.

#### 5) [Lambda](https://aws.amazon.com/lambda/) - LF1
- Trigger to fulfill the recommendation by sending it to SQS for later processing after the conversation.

#### 6) [Simple Queue Servive](https://console.aws.amazon.com/sqs/v2/home)
- FIFO type.

#### 7) [ElasticSearch](https://console.aws.amazon.com/es/home)
- 7000+ Yelp API cuisines data.
- Store restaurants Key ID and cuisine types.

#### 8) [DynamoDB](https://console.aws.amazon.com/dynamodb/home?region=us-east-1)
- 7000+ Yelp API cuisines data.
- Key: restaurant ID and insertedAtTimestamp.
- Data columns: Business ID, Name, Address, Coordinates, Number of Reviews, Rating, Zip Code, and Phone number.

#### 9) [Lambda](https://aws.amazon.com/lambda/) - LF2
- Take requests from SQS.
- Retrieve key message and get key id by elasticsearch.
- Use key as an index to load data from dynamodB.
- Randomly select recommended restaurants.
- Organize the data into a message and deliver it to users by both e-mail and phone.

#### 10) [Cloudformation](https://aws.amazon.com/Cloudformation/) - CL
![image](https://github.com/tim-kao/CloudComputing_Clever_Photo_Album/blob/main/demo/cloudformation.png)
Quick/Automatic deployment by cloudformation

*AWS Region: US-east-1 (N. Virginia)


## Contributor ##
#### [Tim Kao](https://github.com/tim-kao) (UNI: sk4920)
#### [Yin Cheng](https://github.com/jyincheng)(UNI: cc4717)
