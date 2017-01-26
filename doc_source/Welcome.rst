.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

============================
What Is the AWS SDK for iOS?
============================

The AWS SDK for iOS is an open-source software development kit, distributed under an Apache Open Source license. The SDK for iOS provides a library, code samples, and documentation to help developers build connected mobile applications using AWS. This guide explains how to get started with the SDK for iOS, how to work with related mobile services such as Amazon Cognito and Amazon Mobile Analytics, and how to use Amazon Web Services effectively in a mobile app.

About the AWS Mobile Services
#############################

The AWS Mobile SDKs include client-side libraries for working with Amazon Web Services. These client libraries provide high-level, mobile-optimized interfaces to services such as Amazon DynamoDB, Amazon Simple Storage Service, and Amazon Kinesis.

The Mobile SDKs also include clients for Amazon Cognito; and Amazon Mobile Analytics |mdash| web services designed specifically for use by mobile developers.

Amazon Cognito
--------------

Amazon Cognito facilitates the delivery of scoped, temporary credentials to mobile
devices or other untrusted environments, and it uniquely identifies a device or user and
supplies the user with a consistent identity throughout the lifetime of an application.
The Amazon Cognito Sync service enables cross-device syncing of application-related user data.
Cognito also persists data locally, so that it's available even if the device is
offline.

After you've set up the SDK, you can start using Amazon Cognito by following the
instructions at :doc:`cognito-auth-aws-identity-for-ios` and :doc:`cognito-sync-data-across-devices-for-ios`.


Amazon Simple Storage Service (S3)
----------------------------------

Amazon Simple Storage Service (S3) provides secure, durable, highly-scalable object storage in the cloud. Using the AWS Mobile SDK, you can directly access Amazon S3 from your mobile app.

After you've set up the SDK, you can start using Amazon S3 by following
the instructions at :doc:`s3-simple-storage-service-for-ios`.

Amazon DynamoDB
---------------

Amazon DynamoDB is a fast, highly scalable, highly available, cost-effective, nonrelational database service. DynamoDB removes traditional scalability limitations on data storage while maintaining low latency and predictable performance.

After you've set up the SDK, you can start using Amazon DynamoDB by following
the instructions at :doc:`dynamodb-nosql-database-for-ios`.

Amazon Kinesis
--------------

Amazon Kinesis is a fully managed service for real-time processing of streaming data at massive scale.

After you've set up the SDK, you can start using Amazon Kinesis by following
the instructions at :doc:`kinesis-data-stream-processing-for-ios`.

AWS Lambda
----------

AWS Lambda is a compute service that runs your code in response to requests or events and automatically manages the compute resources for you, making it easy to build applications that respond quickly to new information.

After you've set up the SDK, you can start using AWS Lambda by following
the instructions at :doc:`lambda-serverless-business-logic-in-the-cloud-for-ios`.

Amazon Lex
----------

Amazon Lex is an AWS service for building  voice and text conversational interfaces into applications. With Amazon Lex, the same deep learning engine that powers Amazon Alexa is now available to any developer, enabling you to build sophisticated, natural language chatbots into your new and existing applications.

After you've set up the SDK, you can start using Amazon Lex by following
the instructions at :doc:`lex-natural-language-interface-for-ios`.

Amazon Polly
------------

Amazon Polly is a service that turns text into lifelike speech, making it easy to develop mobile applications that use high-quality speech to increase engagement and accessibility. With Amazon Polly you can  quickly build speech-enabled apps that work in multiple geographies.

After you've set up the SDK, you can start using Amazon Polly by following
the instructions at :doc:`polly-convert-text-to-speech-for-ios`.

Amazon Pinpoint
---------------

Using Amazon Pinpoint, you can create push notification campaigns that provide your users with timely, relevant, personalized information to encourage them to keep using your mobile app. You can use push notification campaigns to increase app awareness, downloads, and launches; build customer loyalty; and ultimately boost your mobile revenues.

After you've set up the SDK, you can start using Amazon Pinpoint by following
the instructions at :doc:`pinpoint-mobile-analytics-and-user-engagement-for-ios`.

Amazon Mobile Analytics
-----------------------

Amazon Mobile Analytics, which is now being rolled into Amazon Pinpoint, lets you collect, visualize,
and understand app usage for your mobile apps. Reports are available for metrics on active users, sessions,
retention, in-app revenue, and custom events, and can be filtered by platform and date range.

Amazon Pinpoint service offers analytics plus allows you to act programmatically on the data you gather through
customizable push user engagement. Existing Amazon Mobile Analytics objects/configurations are automatically ported to
Amazon Pinpoint. For the time being you can still use Amazon Mobile Analytics by following
the instructions at :doc:`analytics`.

About the SDK for iOS
#####################

The AWS SDK for iOS includes:

- *AWS iOS libraries* – APIs that hide much of
  the lower-level plumbing of the web service interface, including authentication,
  request retries, and error handling. Each service has its own library, so you can
  include libraries for only the services you need.

- *Code samples* – Practical examples of using
  the libraries to build applications.

- *Documentation* – Reference documentation for
  the AWS SDK for iOS.

The SDK is distributed as a :file:`.zip` file containing the following:

- :file:`LICENSE`
- :file:`NOTICE`
- :file:`README.md`
- **frameworks/**

  - :file:`AWSCore.framework`
  - :file:`AWSAutoScaling.framework`
  - :file:`AWSCloudWatch.framework`
  - :file:`AWSDynamoDB.framework`
  - :file:`AWSEC2.framework`
  - :file:`AWSElasticLoadBalancing.framework`
  - :file:`AWSKinesis.framework`
  - :file:`AWSLambda.framework`
  - :file:`AWSLex.framework`
  - :file:`AWSMachineLearning.framework`
  - :file:`AWSMobileAnalytics.framework`
  - :file:`AWSPinpoint.framework`
  - :file:`AWSPolly.framework`
  - :file:`AWSS3.framework`
  - :file:`AWSSES.framework`
  - :file:`AWSSimpleDB.framework`
  - :file:`AWSSNS.framework`
  - :file:`AWSSQS.framework`
- **extras/**

  - :file:`AWSCognito.framework` - The framework for Amazon Cognito sync.
  - :file:`Amazon Software License.txt`
  - :file:`NOTICE`

- **documentation/** – Contains documentation, including a docset, for the AWS SDK for iOS.
- **samples/** – Contains an HTML document that links to samples, which are named based on the services that they demonstrate.
- **src/** – Contains an HTML document that links to source, which contains the implementation and header files for the AWS iOS libraries.
