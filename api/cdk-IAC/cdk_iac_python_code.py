from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as _s3,
    aws_apigateway as apigw,
    aws_cognito as cognito,
    aws_dynamodb as dynamodb
)
from constructs import Construct

class CdkDemoAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        user_pool = cognito.UserPool(
            self, "MyUserPool",
            user_pool_name="MyCognitoUserPool",
            self_sign_up_enabled=True, 
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True)  
        )

        user_pool_client = user_pool.add_client(
            "MyUserPoolClient",
            user_pool_client_name="MyAppClient",
            auth_flows=cognito.AuthFlow(user_password=True),
            generate_secret=False,
            o_auth=cognito.OAuthSettings(
                callback_urls=["https://d84l1y8p4kdic.cloudfront.net/callback"],
                logout_urls=["https://d84l1y8p4kdic.cloudfront.net/logout"],
                scopes=[
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.PROFILE
                ]
            )
        )

        user_pool_domain = user_pool.add_domain(
            "CognitoDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix="myvpcapp"  
            )
        )

        lambda_vpc = _lambda.Function(
            self,"lambda_vpc_allianz",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset("./lambdas/lambda_vpc"),
            handler='allianz_resource_create_get_1.lambda_handler',
            timeout=Duration.minutes(5),
            memory_size=1028
        )

        lambda_vpc.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess")
        )

        cognito_authorizer = apigw.CognitoUserPoolsAuthorizer(
            self, "MyAuthorizer",
            cognito_user_pools=[user_pool]
        )

        vpc_api = apigw.LambdaRestApi(
            self, "vpc_create_get",
            handler = lambda_vpc,
            rest_api_name = "vpc_api",
            integration_options=apigw.LambdaIntegrationOptions(
                timeout=Duration.seconds(29)
            ),
            proxy=False
        )

        vpcs = vpc_api.root.add_resource(
            "vpcs",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=apigw.Cors.DEFAULT_HEADERS
            )
        )
        vpcs.add_method("GET",
                        authorization_type=apigw.AuthorizationType.COGNITO,
                        authorizer=cognito_authorizer)

        vpcs.add_method("POST",
                        authorization_type=apigw.AuthorizationType.COGNITO,
                        authorizer=cognito_authorizer)

        table = dynamodb.Table(self, "vpc_resources_information",
                                table_name= "vpc_resources_information",
                                partition_key=dynamodb.Attribute(
                                name="vpcId",
                                type=dynamodb.AttributeType.STRING
                                )
                                )
        table.grant_read_write_data(lambda_vpc)
