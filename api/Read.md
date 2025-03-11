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
GET https://zmieuqxc1f.execute-api.us-east-1.amazonaws.com/prod/vpcs

###**Fetches a specific VPC by its ID.**
- **URL:**  
GET https://zmieuqxc1f.execute-api.us-east-1.amazonaws.com/prod/vpcs?vpcId=<VPC_ID>

###**add vpc with multiple subnets**
- **URL:**  
POST https://zmieuqxc1f.execute-api.us-east-1.amazonaws.com/prod/vpcs

## HEADER ###
Need to aquire token by login into website and signup or signin. Only Sign in user is allowed to access the api's. Token should be pass in header Authorization
NOTE - Cognito website is created for user sign up and sign in