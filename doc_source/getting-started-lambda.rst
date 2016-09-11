.. Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

.. highlight:: objc

Building a Mobile Backend Using AWS Lambda
==========================================

Amazon Lambda is a compute service that runs your code in response to events and automatically manages the compute resources for you, making it easy to build applications that respond quickly to new information. The Mobile SDK for iOS enables you to call Lambda functions from your iOS mobile apps.

Create an Amazon Lambda function
--------------------------------

To create a Amazon Lambda function, see `Amazon Lambda Getting Started <http://docs.aws.amazon.com/lambda/latest/dg/getting-started-custom-events.html>`_

Authenticate Users with Cognito Identity
----------------------------------------

Amazon Cognito Identity provides secure access to AWS services. Identities are managed by an identity pool. Roles specify resources an identity can access and are associated with an identity pool. To create an identity pool for your application:

	#. Log into the `Amazon Cognito Console <https://console.aws.amazon.com/cognito/home>`_ and click the :guilabel:`New Identity Pool` button
	#. Give your Identity Pool a unique name and enable access to unauthenticated identities
	#. Click the :guilabel:`Create Pool` button and then the :guilabel:`Update Roles` to create your identity pool and associated roles

For more information on Amazon Cognito Identity, see :doc:`cognito-auth`

Set Permissions
---------------
To use Amazon Lambda in an application, you must set the correct permissions. The following IAM policy allows the user to perform the actions shown in this tutorial on an given Amazon Lambda function identified by ARN:

::

   {
        "Statement": [{
           "Effect": "Allow",
           "Action": [
               "lambda:invokefunction"
           ],
           "Resource": [
              "resource-id",
           ]
        }]
   }

Replace the "resource-id" in the sample above with the ARN of your AWS Lambda function. Apply this policy to the unauthenticated role assigned to your Cognito identity pool, replacing the resource-id value with the correct ARN for your Lambda function.

1.	Log in to the IAM console: Amazon IAM console
2.	Select Roles and select the "Unauth" role that Cognito created for you.
3.	Click Attach Role Policy.
4.	Select Custom Policy and click Select.
5.	Enter a name for your policy and paste in the policy document shown above, replacing the Resource values with the ARNs for your function. You can view the ARN for your function in the Amazon Lambda console.
6.	Click Apply Policy.

To learn more about IAM policies, see `Using IAM <http://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_Introduction.html>`_.

Add the following import statements:
::

    #import <AWSCore/AWSCore.h>

Add the following code to application/:didFinishLaunchingWithOptions method/:
::

    AWSCognitoCredentialsProvider *credentialsProvider = [[AWSCognitoCredentialsProvider alloc] initWithRegionType:AWSRegionUSEast1
        identityPoolId:@"<your-identity-pool-arn>"];

    AWSServiceConfiguration *configuration = [[AWSServiceConfiguration alloc] initWithRegion:AWSRegionUSEast1
        credentialsProvider:credentialsProvider];

    AWSServiceManager.defaultServiceManager.defaultServiceConfiguration = configuration;

.. Note::
	If you have an existing credential provider, you do not need to create a new one.

You must replace <your-identity-pool-arn> with the ARN of your Amazon Cognito Identity Pool. For more information on Amazon Cognito Identity, see :doc:`cognito-auth`

Integrate the SDK into Your App
-------------------------------

If you haven't already done so, `download the SDK for iOS <http://aws.amazon.com/mobile/sdk/>`_,
unzip it, and include it in your application as described at :doc:`setup`. The
instructions direct you to import the headers for the services you'll be
using. For this example, you need the following import:
::

	#import <AWSLambda/AWSLambda.h>

Invoke a Amazon Lambda Function with AWSLambdaInvoker
-----------------------------------------------------

Get a reference to the defualt instance of AWSLambdaInvoker:

::

	AWSLambdaInvoker *lambdaInvoker = [AWSLambdaInvoker defaultLambdaInvoker];

You can pass parameters to your Amazon Lambda Function using a dictionary, an array, or a string. The following snippets illuststrate each of these options.

::

   // Invoke with dictionary input
    AWSLambdaInvoker *lambdaInvoker = [AWSLambdaInvoker defaultLambdaInvoker];
    NSDictionary *parameters = @{@"key1" : @"value1",
                                 @"key2" : @"value2",
                                 @"key3" : @"value3",
                                 @"isError" : @NO};
    [[lambdaInvoker invokeFunction:LambdaFunctionName
                        JSONObject:parameters] continueWithBlock:^id(AWSTask *task) {
        if (task.error) {
            NSLog(@"Error: %@", task.error);
        }
        if (task.exception) {
            NSLog(@"Exception: %@", task.exception);
        }
        if (task.result) {
            NSLog(@"Result: %@", task.result);

            dispatch_async(dispatch_get_main_queue(), ^{
                [self printOutputJSON:task.result];
            });
        }
        return nil;
    }];

::

	// Invoke with array input
	AWSLambdaInvoker *lambdaInvoker = [AWSLambdaInvoker defaultLambdaInvoker];

	    NSArray *parameters = @[@"John", @"Smith"];
	    [[lambdaInvoker invokeFunction:LambdaFunctionName
	                        JSONObject:parameters] continueWithBlock:^id(AWSTask *task) {
	        if (task.error) {
	            NSLog(@"Error: %@", task.error);
	        }
	        if (task.exception) {
	            NSLog(@"Exception: %@", task.exception);
	        }
	        if (task.result) {
	            NSLog(@"Result: %@", task.result);

	            dispatch_async(dispatch_get_main_queue(), ^{
	                [self printOutputJSON:task.result];
	            });
	        }
	        return nil;
	    }];

::

	// Invoke with string input
	AWSLambdaInvoker *lambdaInvoker = [AWSLambdaInvoker defaultLambdaInvoker];

	    NSString *parameters = @"Hello";
	    [[lambdaInvoker invokeFunction:LambdaFunctionName
	                        JSONObject:parameters] continueWithBlock:^id(AWSTask *task) {
	        if (task.error) {
	            NSLog(@"Error: %@", task.error);
	        }
	        if (task.exception) {
	            NSLog(@"Exception: %@", task.exception);
	        }
	        if (task.result) {
	            NSLog(@"Result: %@", task.result);

	            dispatch_async(dispatch_get_main_queue(), ^{
	                [self printOutputJSON:task.result];
	            });
	        }
	        return nil;
	    }];

For more information on accessing AWS Lambda, see :doc:`lambda`.
