# Emptor Trial Project

### Author: Imaduddin A Majid

This project is AWS Lambda-based project to process documents from the web. In this version, the lambda function takes an URL as an argument, make a request, and extract title from the HTML document response of the request. Then, it returns the extracted title to the caller of Lambda function.

## Setup

### Installation Requirements

* Python >= 3.7.3
* Serverless >= 1.43.0 
* requests >= 2.22.0

Install serverless with the following command:

```
npm install -g serverless
```

Setup your AWS credentials by following the steps described [here](https://github.com/serverless/serverless/blob/master/docs/providers/aws/guide/credentials.md) or [watch this video](https://www.youtube.com/watch?v=HSd9uYj2LJA).

Install Python dependencies using this command:
```
pip install -r requirements/requirements-dev.txt
```

if you need additional packages, write them in `requirements/requirements-dev.in` and run the following
command

```
pip-compile --output-file requirements/requirements-dev.txt requirements/requirements-dev.in
```

## Deploy

To deploy simply run
```
serverless deploy
```

## Usage

To extract the title from a URL, use the following commands on your terminal:

```
curl -X POST 'https://XXXXXXXX.execute-api.eu-central-1.amazonaws.com/dev/extract-title?url=YOUR_URL'
```
