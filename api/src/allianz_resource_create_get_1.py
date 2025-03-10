import json
import boto3
from ipaddress import ip_network

def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'POST' and event['resource'] == '/vpcs':
        return create_vpc(event, context)
    elif event['httpMethod'] == 'GET' and event['resource'] == '/vpcs':
        query_string_parameters = event.get('queryStringParameters')
        if query_string_parameters and 'vpcId' in query_string_parameters:
            return get_vpc_details(event, context)
        else:
            return get_all_vpc_details(event, context)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Endpoint or Method is not allowed'})
        }

def create_vpc(event, context):
    ec2 = boto3.resource('ec2')
    dynamodb = boto3.resource('dynamodb')

    if isinstance(event['body'], dict):
        request_body = event['body']
    else:
        request_body = json.loads(event['body'])

    vpc_cidr = request_body.get('vpcCidr')
    subnet_cidrs = request_body.get('subnetCidrs')  

    if has_overlapping_cidrs(subnet_cidrs):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Subnet CIDR blocks are overlapping'})
        }

    if not all_subnet_cidrs_within_vpc_cidr(subnet_cidrs, vpc_cidr):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Subnet CIDR blocks must be within the VPC CIDR range'})
        }
            
    vpc = ec2.create_vpc(CidrBlock=vpc_cidr)
    vpc.wait_until_available()

    subnet_ids = []
    for cidr in subnet_cidrs:
        subnet = vpc.create_subnet(CidrBlock=cidr)
        subnet_ids.append(subnet.id)

    table = dynamodb.Table('allianz_resources_information')
    response = table.put_item(
       Item={
            'vpcId': vpc.id,
            'vpcCidr': vpc_cidr,
            'subnets': subnet_ids
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'VPC ID': vpc.id,
            'VPC CIDR': vpc_cidr,
            'Subnet IDs': subnet_ids
        })
    }

def get_vpc_details(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('allianz_resources_information')

    param = event['queryStringParameters']
    getkey = {'vpcId' : param['vpcId']}

    try:
        response = table.get_item(Key=getkey)
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'VPC not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'vpcId' : param['vpcId'],
            'body': json.dumps({'error': str(e)})
        }

def get_all_vpc_details(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('allianz_resources_information')

    try:
        response = table.scan()
        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def has_overlapping_cidrs(cidr_list):
    networks = [ip_network(cidr) for cidr in cidr_list]
    for i in range(len(networks)):
        for j in range(i + 1, len(networks)):
            if networks[i].overlaps(networks[j]):
                return True
    return False

def all_subnet_cidrs_within_vpc_cidr(subnet_cidrs, vpc_cidr):
    vpc_network = ip_network(vpc_cidr)
    return all(ip_network(subnet_cidr).subnet_of(vpc_network) for subnet_cidr in subnet_cidrs)
