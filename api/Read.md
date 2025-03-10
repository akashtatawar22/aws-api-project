# AWS VPC Management API

## Overview
This project provides a REST API to create, store, and retrieve AWS VPCs and their subnets using **API Gateway, Lambda, and DynamoDB**. The API is protected using **AWS Cognito authentication**.

## Features
**Create a VPC** with multiple subnets and store the details in DynamoDB.
**Retrieve all VPCs** stored in the database.
**Fetch a specific VPC** using its ID.
**Authentication via AWS Cognito** (APItokens required).
**Serverless deployment using AWS services**.

---

## API Endpoints

###**Get All VPCs**
- **URL:**  
GET https://fffw4d32ie.execute-api.us-east-1.amazonaws.com/dev-auth/vpcs

###**Fetches a specific VPC by its ID.**
- **URL:**  
GET https://fffw4d32ie.execute-api.us-east-1.amazonaws.com/dev-auth/vpcs?vpcId=<VPC_ID>

###**add vpc with multiple subnets**
- **URL:**  
POST https://fffw4d32ie.execute-api.us-east-1.amazonaws.com/dev-auth/vpcs

## HEADER ###
GET TOKEN BY LOGIN INTO WEBSITE AND SIGNUP. THEN AQUIRE TOKEN
NOTE - WEBSITE WILL BE SHARED DURING DEMO