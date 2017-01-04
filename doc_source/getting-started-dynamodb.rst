.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Store and Query App Data in DynamoDB
====================================

.. highlight:: objc

Authenticate Users with Cognito Identity
----------------------------------------

Cognito Identity provides secure access to AWS services. Identities are managed by an identity pool. Roles specify resources an identity can access and are associated with an identity pool. To create an identity pool for your application:

	#. Log into the `Cognito Console`_ and click the :guilabel:`New Identity Pool` button
	#. Give your Identity Pool a unique name and enable access to unauthenticated identities
	#. Click the :guilabel:`Create Pool` button and then the :guilabel:`Update Roles` to create your identity pool and associated roles

For more information on Cognito Identity, see :doc:`cognito-auth`

The next page displays code that creates a credential provider that provides a Cognito Identity for your app to use. Copy the code from Steps 1 & 2 into your AppDelegate.m file as shown below:

Add the following import statement:
::

	#import <AWSDynamoDB/AWSDynamoDB.h>

Add the following code to application:didFinishLaunchingWithOptions method:
::

	AWSCognitoCredentialsProvider *credentialsProvider = [[AWSCognitoCredentialsProvider alloc] initWithRegionType:CognitoRegionType
		identityPoolId:CognitoIdentityPoolId];

	AWSServiceConfiguration *configuration = [[AWSServiceConfiguration alloc] initWithRegion:DefaultServiceRegionType
		credentialsProvider:credentialsProvider];

	AWSServiceManager.defaultServiceManager.defaultServiceConfiguration = configuration;

.. Note::
	If you have an existing credential provider, you do not need to create a new one.

Click :guilabel:`Go to Dashboard` to return to the Cognito Console.

Update IAM Roles
----------------

In order for your Cognito Identities to access Amazon DynamoDB, you must modify the Roles associated with your Identity Pool.

1. Navigate to the `Identity and Access Management Console`_ and click :guilabel:`Roles` in the left-hand pane and search for your Identity Pool name - two roles will be listed one for unauthenticated users and one for authenticated users
2. Click the role for unauthenticated users (it will have "unauth" appended to your Identity Pool name) and click the :guilabel:`Attach Role Policy` button
3. Select :guilabel:`Policy Generator` and click the :guilabel:`Select` button
4. In the Edit Permissions page enter the settings shown in the following image:

.. image:: images/edit-permissions-dynamodb.png

The Amazon Resource Name (ARN) of a DynamoDB table is composed of the region in which the table is located, and the owners' AWS account number. For example:
::

	"arn:aws:dynamodb:us-west-2:123456789012:table/table-name".

For more information about specifying ARNs, see `Amazon Resource Names for DynamoDB`_.

5. Click the :guilabel:`Add Statement` button, click the :guilabel:`Next Step` button and the Wizard will show you the configuration generated
6. Click the :guilabel:`Apply Policy` button

Write a Row
-----------

To write a row to the table, define a class to hold your row data. This class must be derived from AWSDynamoDBModel and implement the AWSDynamoDBModel interface. The class should also contain properties that hold the attribute data for the row.  The following class declaration illustrates such a class:
::

	@interface Book : AWSDynamoDBObjectModel <AWSDynamoDBModeling>

	@property (nonatomic, strong) NSString *Title;
	@property (nonatomic, strong) NSString *Author;
	@property (nonatomic, strong) NSNumber *Price;
	@property (nonatomic, strong) NSString *ISBN;

	@end

The following code illustrates the implementation of the class:
::

	@implementation Book

	+ (NSString *)dynamoDBTableName {
	    return @"Books";
	}

	+ (NSString *)hashKeyAttribute {
	    return @"ISBN";
	}

	@end


To insert a row, instantiate the class and set its properties:
::

	Book *myBook = [Book new];
	myBook.ISBN = @"3456789012";
	myBook.Title = @"The Scarlet Letter";
	myBook.Author = @"Nathaniel Hawthorne";
	myBook.Price = [NSNumber numberWithInt:899];

And pass the object to the AWSDyanmoDBObjectMapper's save method:
::

	[[dynamoDBObjectMapper save:myBook]
 	 continueWithBlock:^id(AWSTask *task) {
     if (task.error) {
         NSLog(@"The request failed. Error: [%@]", task.error);
     }
     if (task.exception) {
         NSLog(@"The request failed. Exception: [%@]", task.exception);
     }
     if (task.result) {
         //Do something with the result.
     }
     return nil;
	 }];


To update a row, modify the instance of the DDTableRow class and call AWSDynamoObjectMapper.save as shown above.

Retrieve a Row
--------------

To retrieve a row, instantiate the object to hold the retrieved data and set its primary key and call the AWSDynamoDBObjectMapper class' load method. The following code illustrates calling the load method:
::

	[[dynamoDBObjectMapper load:[Book class] hashKey:@"6543210987" rangeKey:nil]
		continueWithBlock:^id(AWSTask *task) {
			if (task.error) {
				NSLog(@"The request failed. Error: [%@]", task.error);
			}

			if (task.exception) {
				NSLog(@"The request failed. Exception: [%@]", task.exception);
			}

			if (task.result) {
				Book *book = task.result;
				//Do something with the result.
			}
			return nil;
     }];


For more information on accessing DynamoDB from an iOS application, see `Calling Amazon DynamoDB in an iOS App`_


.. _DynamoDB Console: https://console.aws.amazon.com/dynamodb/home
.. _Cognito Console: https://console.aws.amazon.com/cognito/home
.. _Identity and Access Management Console: https://console.aws.amazon.com/iam/home
.. _Amazon Resource Names for DynamoDB: http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/UsingIAMWithDDB.html#ARN_Format
.. _Working With Tables: http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.html
.. _Calling Amazon DynamoDB in an iOS App: http://docs.aws.amazon.com/mobile/sdkforios/developerguide/dynamodb_om.html
