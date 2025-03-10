# AWS VPC Management API

## Overview
This project provides a REST API to create, store, and retrieve AWS VPCs and their subnets using **API Gateway, Lambda, and DynamoDB**. The API is protected using **AWS Cognito authentication**.

## Features
**Create a VPC** with multiple subnets and store the details in DynamoDB.
**Retrieve all VPCs** stored in the database.
**Fetch a specific VPC** using its ID.
**Authentication via AWS Cognito** (APItokens required).

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
Need to aquire token by login into website and signup or signin. Only Sign in user is allowed to access the api's. Token should be pass in header Authorization
NOTE - Website to login will be shared during demo.