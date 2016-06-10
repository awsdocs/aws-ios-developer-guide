.. Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Execute Code On Demand with Amazon Lambda
=========================================

Amazon Lambda is a compute service that runs your code in response to events and automatically manages the compute resources for you, making it easy to build applications that respond quickly to new information. Amazon Lambda functions can be called directly from mobile, IoT, and Web apps and send a response back synchronously, making it easy to create scalable, secure, and highly available backends for your mobile apps without the need to provision or manage infrastructure. For more information, see `Amazon Lambda <http://aws.amazon.com/lambda/>`_.

The Mobile SDK for iOS enables you to call Amazon Lambda functions from your iOS mobile apps, using the lambdainvoker class. When invoked from the Mobile SDK, Amazon Lambda functions receive data about the device and the end user identity through a client and identity context object, making it easy to create rich, and personalized app experiences. To learn more about the data available within the client and identity context, see :ref:`clientContext` and :ref:`identityContext`.

The :doc:`getting-started-lambda` document describes step-by-step instructions for integrating the AWS Mobile SDK for iOS into your app.

To use the LambdaInvoker API, use the following import statement:

::

	#import <AWSLambda/AWSLambda.h>

Invoking a Amazon Lambda Function
---------------------------------

AWSLambdaInvoker provides a high-level abstraction for Amazon Lambda. When invokeFunction/:JSONObject/: is invoked, the JSON object is serialized into JSON data and sent to the Amazon Lambda service. Amazon Lambda returns a JSON encoded response that is deserialized into a JSON object.

A valid JSON object must have the following properties:

* All objects are instances of `NSString`, `NSNumber`, `NSArray`, `NSDictionary`, or `NSNull`.
* All dictionary keys are instances of `NSString`.
* Numbers are not `NaN` or `infinity`.

For example, it is an example of valid request:

::

    AWSLambdaInvoker *lambdaInvoker = [AWSLambdaInvoker defaultLambdaInvoker];

    [[lambdaInvoker invokeFunction:@"myFunction"
                        JSONObject:@{@"key1" : @"value1",
                                     @"key2" : @2,
                                     @"key3" : [NSNull null],
                                     @"key4" : @[@1, @"2"],
                                     @"isError" : @NO}] continueWithBlock:^id(AWSTask *task) {
        // Handle response
        return nil;
    }];

On successful execution, `task.result` contains a JSON object. For instance, if `myFunctions` returns a dictionary, you can cast the result to an `NSDictionary` as follows:

::

    if (task.result) {
        NSLog(@"Result: %@", task.result);
        NSDictionary *JSONObject = task.result;
        NSLog(@"result: %@", JSONObject[@"resultKey"]);
    }

On failed Amazon Lambda service execution, `task.error` may contain an `NSError` with `AWSLambdaErrorDomain` domain and the following error code:

* `AWSLambdaErrorUnknown`
* `AWSLambdaErrorService`
* `AWSLambdaErrorResourceNotFound`
* `AWSLambdaErrorInvalidParameterValue`

On failed function execution, `task.error` may contain an `NSError` with `AWSLambdaInvokerErrorDomain` domain and the following error code:

* `AWSLambdaInvokerErrorTypeUnknown`
* `AWSLambdaInvokerErrorTypeFunctionError`

When `AWSLambdaInvokerErrorTypeFunctionError` error code is returned, `error.userInfo` may contain a function error from your Amazon Lambda function with `AWSLambdaInvokerFunctionErrorKey` key.

Here is an example code snippet:

::

    if (task.error) {
        NSLog(@"Error: %@", task.error);
        if ([task.error.domain isEqualToString:AWSLambdaInvokerErrorDomain]
            && task.error.code == AWSLambdaInvokerErrorTypeFunctionError) {
            NSLog(@"Function error: %@", task.error.userInfo[AWSLambdaInvokerFunctionErrorKey]);
        }
    }
    if (task.exception) {
        NSLog(@"Exception: %@", task.exception);
    }

With everything put together, here is a complete code snippet:

::

    AWSLambdaInvoker *lambdaInvoker = [AWSLambdaInvoker defaultLambdaInvoker];

    [[lambdaInvoker invokeFunction:@"myFunction"
                        JSONObject:@{@"key1" : @"value1",
                                     @"key2" : @2,
                                     @"key3" : [NSNull null],
                                     @"key4" : @[@1, @"2"],
                                     @"isError" : @NO}] continueWithBlock:^id(AWSTask *task) {
        if (task.error) {
            NSLog(@"Error: %@", task.error);
            if ([task.error.domain isEqualToString:AWSLambdaInvokerErrorDomain]
                && task.error.code == AWSLambdaInvokerErrorTypeFunctionError) {
                NSLog(@"Function error: %@", task.error.userInfo[AWSLambdaInvokerFunctionErrorKey]);
            }
        }
        if (task.exception) {
            NSLog(@"Exception: %@", task.exception);
        }
        if (task.result) {
            NSLog(@"Result: %@", task.result);
            NSDictionary *JSONObject = task.result;
            NSLog(@"result: %@", JSONObject[@"resultKey"]);
        }
        return nil;
    }];

.. _clientContext:

Client Context
--------------

When invoked through the SDK, Amazon Lambda functions have access to the data about the device and the app using thed ClientContext class. When you use Amazon Cognito as a credential provider, access to the end user identity is available using the IdentityContext class.

You can access the client context in your lambda function as follows:

::

	exports.handler = function(event, context) {
	console.log("installation_id = " + context.clientContext.client.installation_id);
	console.log("app_version_code = " + context.clientContext.client.app_version_code);
	console.log("app_version_name = " + context.clientContext.client.app_version_name);
	console.log("app_package_name = " + context.clientContext.client.app_package_name);
	console.log("app_title = " + context.clientContext.client.app_title);
	console.log("platform_version = " + context.clientContext.env.platform_version);
	console.log("platform = " + context.clientContext.env.platform);
	console.log("make = " + context.clientContext.env.make);
	console.log("model = " + context.clientContext.env.model);
	console.log("locale = " + context.clientContext.env.locale);

	context.succeed("Your platform is " + context.clientContext.env.platform;
	}

ClientContext has the following fields:

client.installation_id
	Auto-generated UUID that is created the first time the app is launched. This is stored in the keychain on the device. In case the keychain is wiped a new installation ID will be generated.

client.app_version_code
	`CFBundleShortVersionString <https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-111349>`_

client.app_version_name
	`CFBundleVersion <https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-102364>`_

client.app_package_name
	`CFBundleIdentifier <https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-102070>`_

client.app_title
	`CFBundleDisplayName <https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-110725>`_

env.platform_version
	`systemVersion <https://developer.apple.com/library/ios/documentation/UIKit/Reference/UIDevice_Class/index.html#//apple_ref/occ/instp/UIDevice/systemVersion>`_

env.platform
	`systemName <https://developer.apple.com/library/ios/documentation/UIKit/Reference/UIDevice_Class/index.html#//apple_ref/occ/instp/UIDevice/systemName>`_

env.make
	Hardcoded as "apple"

env.model
	`Model of the device <https://developer.apple.com/library/ios/documentation/UIKit/Reference/UIDevice_Class/index.html#//apple_ref/occ/instp/UIDevice/model>`_

env.locale
	`localeIdentifier <https://developer.apple.com/library/ios/documentation/Cocoa/Reference/Foundation/Classes/NSLocale_Class/index.html#//apple_ref/occ/instp/NSLocale/localeIdentifier>`_ from `autoupdatingCurrentLocale <https://developer.apple.com/library/ios/documentation/Cocoa/Reference/Foundation/Classes/NSLocale_Class/index.html#//apple_ref/occ/clm/NSLocale/autoupdatingCurrentLocale>`_

.. _identityContext:

Identity Context
----------------

To invoke Amazon Lambda function from your mobile app, you can leverage Amazon Cognito as the credential provider. You can learn more about Amazon Cognito here. Amazon Cognito assigns each user a unique Identity ID. This Identity ID is available to you in the Amazon Lambda functions invoked through the AWS Mobile SDK. You can access the Identity ID as follows:

::

	exports.handler = function(event, context) {
	console.log("clientID = " + context.identity);

	context.succeed("Your client ID is " + context.identity);
	}

For more information about Identity ID, see `Amazon Cognito Identity <http://docs.aws.amazon.com/mobile/sdkforandroid/developerguide/cognito-auth.html>`_.

.. _Cognito Console: https://console.aws.amazon.com/cognito/home
