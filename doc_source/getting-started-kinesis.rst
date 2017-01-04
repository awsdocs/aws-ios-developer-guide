.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Writing App Data to Amazon Kinesis
====================================

.. highlight:: objc

`Amazon Kinesis <http://aws.amazon.com/kinesis/>`_ is a fully managed service for real-time processing of streaming data at massive scale.

Authenticate Users with Cognito Identity
----------------------------------------

Cognito Identity provides secure access to AWS services. Identities are managed by an identity pool. Roles specify resources an identity can access and are associated with an identity pool. To create an identity pool for your application:

#. Log into the `Cognito Console`_ and click the :guilabel:`New Identity Pool` button.
#. Give your Identity Pool a unique name and enable access to unauthenticated identities.
#. Click the :guilabel:`Create Pool` button and then the :guilabel:`Update Roles` to create your identity pool and associated roles.

Add the following import statement:
::

	#import <AWSCore/AWSCore.h>

Add the following code to application:didFinishLaunchingWithOptions method:
::

    AWSCognitoCredentialsProvider *credentialsProvider = [[AWSCognitoCredentialsProvider alloc] initWithRegionType:AWSRegionUSEast1
                                                                                                    identityPoolId:@"COGNITO_IDENTITY_POOL"];

    AWSServiceConfiguration *configuration = [[AWSServiceConfiguration alloc] initWithRegion:AWSRegionUSEast1 credentialsProvider:credentialsProvider];

    AWSServiceManager.defaultServiceManager.defaultServiceConfiguration = configuration;

.. Note::
	If you have an existing credential provider, you do not need to create a new one.

For more information on Cognito Identity, see :doc:`cognito-auth`


Grant Role Access to Your Kinesis Stream
----------------------------------------
To use Kinesis in an application, you must allow the IAM roles associated with your Cognito Identity Pool access to your Kinesis stream. To set this policy:

1. Navigate to the `Identity and Access Management Console`_ and choose :guilabel:`Roles` in the left-hand pane.
2. Type your Identity Pool name into the search box. Two roles will be listed: one for unauthenticated users and one for authenticated users.
3. Choose the role for unauthenticated users (it will have "unauth" appended to your Identity Pool name).
4. Scroll down the web page until you see the :guilabel:`Create Role Policy`. Choose it, select :guilabel:`Policy Generator`, and then choose the :guilabel:`Select` button.
5. Select the :guilabel:`Allow` radio button, Amazon Kinesis in the :guilabel:`AWS Service` drop-down, PutRecord under :guilabel:`Actions`, and enter the ARN to your Kinesis stream in the :guilabel:`Amazon Resource Name (ARN)` text box.
6. Choose the :guilabel:`Add Statement` button, the :guilabel:`Next Step` button, and the :guilabel:`Apply Policy` button.

To learn more about Kinesis-specific policies, see
`Controlling Access to Amazon Kinesis Resources with IAM <http://docs.aws.amazon.com/kinesis/latest/dev/kinesis-using-iam.html>`_.

Grant Role Access to Your Kinesis Firehose Delivery Stream
----------------------------------------
To use Kinesis Firehose in an application, you must allow the IAM roles associated with your Amazon Cognito Identity Pool access to your Kinesis Firehose delivery stream. To set this policy:

1. Navigate to the `Identity and Access Management Console`_ and choose :guilabel:`Roles` in the left-hand pane.
2. Type your Identity Pool name into the search box. Two roles will be listed: one for unauthenticated users and one for authenticated users.
3. Choose the role for unauthenticated users (it will have "unauth" appended to your Identity Pool name).
4. Scroll down the web page until you see the :guilabel:`Create Role Policy`. Choose it, select :guilabel:`Policy Generator`, and then choose the :guilabel:`Select` button.
5. Select the :guilabel:`Allow` radio button, Amazon Kinesis in the :guilabel:`AWS Service` drop-down, PutRecord under :guilabel:`Actions`, and enter the ARN to your Kinesis Firehose delivery stream in the :guilabel:`Amazon Resource Name (ARN)` text box.
6. Choose the :guilabel:`Add Statement` button, the :guilabel:`Next Step` button, and the :guilabel:`Apply Policy` button.

To learn more about Kinesis Firehose-specific policies, see
`Controlling Access to Amazon Kinesis Firehose <http://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html>`_.

Configure the Kinesis Service Client
------------------------------------
Add the following import statement::

	#import <AWSKinesis/AWSKinesis.h>

Use the :command:`AWSKinesisRecorder` to interact with the Kinesis service. The
following snippet returns a shared instance of the Kinesis service client:

::

	AWSKinesisRecorder *kinesisRecorder = [AWSKinesisRecorder defaultKinesisRecorder];

Configure the :command:`AWSKinesisRecorder` through its properties:

::

    kinesisRecorder.diskAgeLimit = 30 * 24 * 60 * 60; // 30 days
    kinesisRecorder.diskByteLimit = 10 * 1024 * 1024; // 10MB
    kinesisRecorder.notificationByteThreshold = 5 * 1024 * 1024; // 5MB

Save Records to Local Storage
-----------------------------
With :command:`AWSKinesisRecorder` created and configured, you can use :command:`saveRecord:streamName:` to save records to local storage:

::

	// Create some text data
	NSData *yourData = [@"Test_data" dataUsingEncoding:NSUTF8StringEncoding];

	// save the data to local storage
	[kinesisRecorder saveRecord:yourData streamName:@"YourStreamName"]

Submit Records to an Amazon Kinesis Stream
--------------------------------
Use the :command:`submitAllRecords` asynchronous method on the :command:`AWSKinesisRecorder` object to send all locally saved records to your Kinesis stream. Both :command:`saveRecord` and :command:`submitAllRecords` are asynchronous operations, so you should ensure that :command:`saveRecord` is complete before you invoke :command:`submitAllRecords`. The following code sample shows the how to call these methods using the AWSTask:

::

	// Create an task array to track the saveRecord calls.
	NSMutableArray *tasks = [NSMutableArray new];

	// Call saveRecord for each record
	for (int32_t i = 0; i < 100; i++) {
		[tasks addObject:[kinesisRecorder saveRecord:[[NSString stringWithFormat:@"TestString-%02d", i] dataUsingEncoding:NSUTF8StringEncoding] streamName:@"YourStreamName"]];
	}
	// When all of the saveRecord calls have completed, call submitAllRecords to write all records
	// to the Kinesis stream
	[[[AWSTask taskForCompletionOfAllTasks:tasks] continueWithSuccessBlock:^id(AWSTask *task) {
		return [kinesisRecorder submitAllRecords];
		}] continueWithBlock:^id(AWSTask *task) {
		if (task.error) {
			NSLog(@"Error: [%@]", task.error);
		}
		return nil;
	}];

To learn more about working with Amazon Kinesis, see the `Amazon Kinesis Developer Resources <http://aws.amazon.com/kinesis/developer-resources/>`_.
To learn more about working with Amazon Kinesis Firehose, see the `Amazon Kinesis Firehose Documentation <http://aws.amazon.com/documentation/firehose/>`_.
To learn more about the Kinesis classes, see the `class reference for AWSKinesisRecorder <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSKinesisRecorder.html>`_.


.. _Cognito Console: https://console.aws.amazon.com/cognito/home
.. _Identity and Access Management Console: https://console.aws.amazon.com/iam/home
