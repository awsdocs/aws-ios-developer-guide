.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

.. highlight:: objc

Store and Retrieve App Data in Amazon DynamoDB
##############################################

`Amazon DynamoDB <http://aws.amazon.com/dynamodb/>`_ is a fast, highly scalable,
highly available, cost-effective, nonrelational database service. DynamoDB removes traditional
scalability limitations on data storage while maintaining low latency and predictable
performance.

The AWS Mobile SDK for iOS provides both low-level and high-level libraries for working with DynamoDB. The high-level library includes the DynamoDB Object Mapper, which lets you map client-side classes to DynamoDB tables; perform various create, read, update, and delete (CRUD) operations; and execute queries. Using the DynamoDB Object Mapper, you can write simple, readable code that stores objects in the cloud.

Most of the tasks described below are accomplished with the DynamoDB Object Mapper. Conditional writes and batch operations are accomplished with the low-level client (see :ref:`conditional-writes` and :ref:`batch-operations`).

For information about DynamoDB Region availability, see  `AWS Service Region Availability <http://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/>`_.

Getting Started
===============

This section provides a step-by-step guide for getting started with DynamoDB using the AWS Mobile SDK for iOS. You can also try out the `DynamoDB sample <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/DynamoDBObjectMapper-Sample>`_.

Get the SDK
-----------

To use DynamoDB from your mobile app, first set up the AWS Mobile SDK for iOS:

#. Download the iOS SDK and include it in your iOS project, as described at :doc:`setup`.
#. Import the following header into your project::

    #import <AWSDynamoDB/AWSDynamoDB.h>

Configure Credentials
---------------------

Amazon Cognito lets you create unique end user identifiers for accessing AWS cloud
services. You'll use Cognito to provide temporary AWS credentials to your app.

#. Log in to the `Cognito console <https://console.aws.amazon.com/cognito/>`_.

#. Create an identity pool. For this tutorial, you don't need to configure public identity providers, OpenID Connect providers, or developer authenticated identities. But do enable unauthenticated identities.

#. Cognito creates and assigns new IAM roles for you. When you have the option, select :guilabel:`Update Roles`.

#. Copy the auto-generated Cognito client initialization code into your project. For this tutorial, you won't need the store-and-synchronize snippet.

For more information on setting up the Cognito client, see `Cognito Identity Developer Guide <http://docs.aws.amazon.com/cognito/devguide/identity/>`_.

Create a DynamoDB Table and Index
---------------------------------

For this tutorial, let's assume we're building a bookstore app. Our app will need to keep track of the books available in the bookstore, and we can create a DynamoDB table to do so.

To create our Books table:

#. Log in to the `DynamoDB console <https://console.aws.amazon.com/dynamodb/>`_.
#. Click :guilabel:`Create Table`.
#. Enter :command:`Books` as the name of the table.
#. Select :guilabel:`Hash` as the primary key type.
#. For the hash attribute name, ensure that :guilabel:`String` is selected and enter :command:`ISBN`. Click :guilabel:`Continue`.
#. With the index type set to :guilabel:`Global Secondary Index` and the data type set to :guilabel:`String`,  enter :command:`Author` in the :guilabel:`Index Hash Key` field.
#. In the :guilabel:`Index Range Key` field, with the data type set to :guilabel:`Number`, enter :command:`Price`.
#. In the :guilabel:`Index Name` field enter :command:`Author-Price-index`.
#. Leave the other values at their defaults and click :guilabel:`Add Index to Table` and then :guilabel:`Continue`.
#. Set the read capacity to ``10`` and the write capacity to ``5``. Click :guilabel:`Continue`.
#. Enter a notification email and click :guilabel:`Continue` to create throughput alarms.
#. Click :guilabel:`Create`. DynamoDB will create your database.
#. Refresh the console and select your Books table from the list of tables.
#. Open the :guilabel:`Details` tab and copy or note the Amazon Resource Name (ARN). You'll need this in a moment.

Set Permissions
---------------

To use DynamoDB in an application, you must set the correct permissions. The following IAM policy allows the user to perform the actions shown in this tutorial on two resources (a table and an index) identified by `ARN <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_::

    {
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "dynamodb:DeleteItem",
            "dynamodb:GetItem",
            "dynamodb:PutItem",
            "dynamodb:Scan",
            "dynamodb:Query",
            "dynamodb:UpdateItem",
            "dynamodb:BatchWriteItem"
        ],
        "Resource": [
            "arn:aws:dynamodb:us-west-2:123456789012:table/Books",
            "arn:aws:dynamodb:us-west-2:123456789012:table/Books/index/*"
        ]
    }]
    }

Apply this policy to the unauthenticated role assigned to your Cognito identity pool, replacing the ``Resource`` values with the correct ARN for your DynamoDB table:

#. Log in to the `IAM console <https://console.aws.amazon.com/iam>`_.
#. Select :guilabel:`Roles` and select the "Unauth" role that Cognito created for you.
#. Click :guilabel:`Attach Role Policy`.
#. Select :guilabel:`Custom Policy` and click :guilabel:`Select`.
#. Enter a name for your policy and paste in the policy document shown above, replacing the ``Resource`` values with the ARNs for your table and index. (You can retrieve the table ARN from the :guilabel:`Details` tab of the database; then append :file:`/index/*` to obtain the value for the index ARN.
#. Click :guilabel:`Apply Policy`.

To learn more about IAM policies, see `Using IAM <http://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_Introduction.html>`_. To learn more about DynamoDB-specific policies, see `Using IAM to Control Access to DynamoDB Resources <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/UsingIAMWithDDB.html>`_.

Create a DynamoDB Object Mapper Client
--------------------------------------

We're going to use the `AWSDynamoDBObjectMapper <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSDynamoDBObjectMapper.html>`_ to map a client-side class to our database. The Object Mapper supports high-level operations like creating, getting, querying, updating, and deleting records. We can create an Object Mapper as follows::

    AWSDynamoDBObjectMapper *dynamoDBObjectMapper = [AWSDynamoDBObjectMapper defaultDynamoDBObjectMapper];

All of the Object Mapper methods return an ``AWSTask`` object, so you'll need to work with ``AWSTask``
in order to use DynamoDB effectively. To learn how to use the ``AWSTask`` class, see :doc:`awstask`.

Define a Mapping Class
======================

In DynamoDB, a database is a collection of tables, and a table can be described as follows:

* A table is a collection of items.
* Each item is a collection of attributes.
* Each attribute has a name and a value.

For our bookstore app, each item in the table will represent a book, and each item will have four attributes: :dfn:`Title`, :dfn:`Author`, :dfn:`Price`, and :dfn:`ISBN`.

Each item (Book) in the table will have a hash key |mdash| in this case, ISBN |mdash| which is the primary key for the table.

We're going to map each item in the Book table to a ``Book`` object in the client-side code, so that we can directly manipulate the database item through its object representation.

Here's the header for our ``Book`` class::

    #import <Foundation/Foundation.h>
    #import <AWSDynamoDB/AWSDynamoDB.h>

    @interface Book : AWSDynamoDBObjectModel <AWSDynamoDBModeling>

    @property (nonatomic, strong) NSString *Title;
    @property (nonatomic, strong) NSString *Author;
    @property (nonatomic, strong) NSNumber *Price;
    @property (nonatomic, strong) NSString *ISBN;

    @end

Note that the case of each attribute name in the mapping class must match the case of the corresponding attribute name in DynamoDB.  Otherwise, they'll be treated as different attributes.

.. note::

   As of SDK version 2.0.16, the ``AWSDynamoDBModel`` mapping class is deprecated and replaced by ``AWSDynamoDBObjectModel``. The deprecated ``AWSDynamoDBModel`` used ``NSArray`` to represent multi-valued types (String Set, Number Set, and Binary Set); it did not support Boolean, Map, or List types. The new ``AWSDynamoDBObjectModel`` uses ``NSSet`` for multi-valued types and supports Boolean, Map, and List. For the Boolean type, you have to create an ``NSNumber`` using ``[NSNumber numberWithBool:YES]`` or using the shortcuts ``@YES`` and ``@NO``. For the Map type, create using ``NSDictionary``. For the List type, create using ``NSArray``.

Here's the implementation of our model::

    #import <AWSDynamoDB/AWSDynamoDB.h>
    #import "Book.h"

    @implementation Book

    + (NSString *)dynamoDBTableName {
        return @"Books";
    }

    + (NSString *)hashKeyAttribute {
        return @"ISBN";
    }

    @end

To conform to ``AWSDynamoDBModeling``, we have to implement ``dynamoDBTableName`` and ``hashKeyAttribute``. ``dynamoDBTableName`` should return the name of the table, and ``hashKeyAttribute`` should return the name of the hash key. If the table had a range key, we would also need to implement ``+ (NSString *)rangeKeyAttribute``.

Interact with Stored Objects
============================

Now that we have a DynamoDB table, a mapping class, and an Object Mapper client, we can start interacting with objects in the cloud.

Save an Item
------------

The `save: <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSDynamoDBObjectMapper.html#//api/name/save:>`_ method saves an object to DynamoDB, using the default configuration. ``save:`` takes as a parameter an object that inherits from ``AWSDynamoDBObjectModel`` and conforms to the ``AWSDynamoDBModeling`` protocol. The properties of this object will be mapped to attributes in the DynamoDB table.

First, we create the object that we want to save::

    Book *myBook = [Book new];
    myBook.ISBN = @"3456789012";
    myBook.Title = @"The Scarlet Letter";
    myBook.Author = @"Nathaniel Hawthorne";
    myBook.Price = [NSNumber numberWithInt:899];

And then we pass the object to the ``save:`` method::

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

Save Behavior Options
^^^^^^^^^^^^^^^^^^^^^

The AWS Mobile SDK for iOS supports the following save behavior options:

* ``AWSDynamoDBObjectMapperSaveBehaviorUpdate``: Does not affect unmodeled attributes on a save operation; passing a nil value for the modeled attribute will remove it from the corresponding item in DynamoDB. By default, the Object Mapper uses this behavior.
* ``AWSDynamoDBObjectMapperSaveBehaviorUpdateSkipNullAttributes``: Similar to the default update behavior, except that it ignores any null value attribute(s) and will NOT remove them from an item in DynamoDB.
* ``AWSDynamoDBObjectMapperSaveBehaviorAppendSet``: Treats scalar attributes (String, Number, Binary) the same as the ``SkipNullAttributes`` option above. However, for set attributes, it appends to the existing attribute value instead of overriding it. The caller needs to make sure that the modeled attribute type matches the existing set type; otherwise, a service exception will occur.
* ``AWSDynamoDBObjectMapperSaveBehaviorClobber``: Clears and replaces all attributes, including unmodeled ones, on save. Versioned field constraints will also be disregarded.

Here's an example of setting a default save behavior on the Object Mapper::

    AWSDynamoDBObjectMapperConfiguration *updateMapperConfig = [AWSDynamoDBObjectMapperConfiguration new];
    updateMapperConfig.saveBehavior = AWSDynamoDBObjectMapperSaveBehaviorUpdate_Skip_Null_Attributes;
    // Update_Skip_Null_Attributes

Then we can use ``updateMapperConfig`` as an argument when calling `save:configuration: <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSDynamoDBObjectMapper.html#//api/name/save:configuration:>`_.

Retrieve an Item
----------------

Using an object's primary key (in this case, the hash attribute "ISBN"), we can load the corresponding item from the database. The following code snippet returns the Book item with an ISBN of "6543210987"::

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

The Object Mapper creates a mapping between the Book item returned from the database and the ``Book`` object on the client (here, ``resultBook``). Thus, assuming that the Book item has a title, we could access the title at ``resultBook.Title``.

Note that our Books database does not have a range key, so we passed ``nil`` to the ``rangeKey`` parameter.

Update an Item
--------------

To update an item in the database, just set new attributes and save the object again.

Note that setting a new hash key creates a new item in the database, even though it doesn't create a new object on the client. For example, we saved a book titled "The Scarlet Letter" with an ISBN of 3456789012. The ISBN is the hash key for the table. Let's assume that we still have a ``myBook`` reference to this ``Book`` instance. If we assign a new value to ``myBook.ISBN`` and save the object, we'll have two books in the database titled "The Scarlet Letter" |mdash| one with the old ISBN value, and one with the new value.

Delete an Item
--------------

To delete a table row, use the ``remove:`` method::

    Book *bookToDelete = [Book new];
    bookToDelete.ISBN = @"4456789012";

    [[dynamoDBObjectMapper remove:bookToDelete]
     continueWithBlock:^id(AWSTask *task) {

         if (task.error) {
             NSLog(@"The request failed. Error: [%@]", task.error);
         }
         if (task.exception) {
             NSLog(@"The request failed. Exception: [%@]", task.exception);
         }
         if (task.result) {
             //Item deleted.
         }
         return nil;
     }];

Perform a Scan
==============

With a scan operation, we can retrieve all items from a given table. A scan examines every item in the table and returns the results in an undetermined order.

The ``scan:expression:`` method takes two parameters |mdash| the class of the resulting object and an instance of ``AWSDynamoDBScanExpression``, which provides options for filtering results. In the following example, we create an ``AWSDynamoDBScanExpression`` object and set its ``limit`` property. Then we pass our ``Book`` class and the expression object to ``scan:expression:``::

    AWSDynamoDBScanExpression *scanExpression = [AWSDynamoDBScanExpression new];
    scanExpression.limit = @10;

    [[dynamoDBObjectMapper scan:[Book class]
                     expression:scanExpression]
     continueWithBlock:^id(AWSTask *task) {
         if (task.error) {
             NSLog(@"The request failed. Error: [%@]", task.error);
         }
         if (task.exception) {
             NSLog(@"The request failed. Exception: [%@]", task.exception);
         }
         if (task.result) {
             AWSDynamoDBPaginatedOutput *paginatedOutput = task.result;
             for (Book *book in paginatedOutput.items) {
                 //Do something with book.
             }
         }
         return nil;
     }];

The output of a scan is returned as an ``AWSDynamoDBPaginatedOutput`` object. We can access the array of returned items via the ``items`` property.

The ``scanExpression`` method provides several optional parameters. For example, you can optionally use a filter expression to filter the scan result. With a filter expression, you can specify a condition, attribute names, and values on which you want the condition evaluated. For more information about the parameters and the API, see `AWSDynamoDBScanExpression: <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSDynamoDBScanExpression.html>`_.

The following code snippet scans the Books table to find books with price less than 50::

	AWSDynamoDBScanExpression *scanExpression = [AWSDynamoDBScanExpression new];
	scanExpression.limit = @10;
	scanExpression.filterExpression = @"Price < :val";
	scanExpression.expressionAttributeValues = @{@":val":@50};

	[[dynamoDBObjectMapper scan:[Book class]
                 expression:scanExpression]
 	continueWithBlock:^id(AWSTask *task) {
	     if (task.error) {
	         NSLog(@"The request failed. Error: [%@]", task.error);
	     }
	     if (task.exception) {
	         NSLog(@"The request failed. Exception: [%@]", task.exception);
	     }
	     if (task.result) {
	         AWSDynamoDBPaginatedOutput *paginatedOutput = task.result;
	         for (Book *book in paginatedOutput.items) {
	             //Do something with book.
	         }
	     }
	     return nil;
	 }];

You can also use the ``projectionExpression`` property to specify the attributes to retrieve from the ``Books`` table. For example adding ``scanExpression.projectionExpression = @"ISBN, Title, Price";``  in the previous code snippet retrieves only those three properties in the book object. The ``Author`` property in the book object will always be nil.

Scan is an expensive operation and should be used with care to avoid disrupting
higher priority traffic on the table. The *Amazon DynamoDB Developer Guide* has `Guidelines for Query and Scan <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html>`_ that explain best  practices for scan operations.

Perform a Query
===============

The Query API enables you to query a table or a secondary index. You must provide a hash key value in ``AWSDynamoDBQueryExpression``. To query an index, you must also specify the ``indexName``. You must specify the ``hashKeyAttribute`` if you query a global secondary with a different hashKey. If the table or index has a range key, you can optionally refine the results by providing a range key value and a condition.
The ``query:expression:`` method takes two parameters |mdash| the class of the resulting object and an instance of ``AWSDynamoDBQueryExpression``. In the following example, we query the ``Books`` index table to find all books with author of "John Smith" and price less than 50::

	AWSDynamoDBQueryExpression *queryExpression = [AWSDynamoDBQueryExpression new];

	queryExpression.indexName = @"Author-Price-index";

	queryExpression.hashKeyAttribute = @"Author";
	queryExpression.hashKeyValues = @"John Smith";

	queryExpression.rangeKeyConditionExpression = @"Price < :val";
	queryExpression.expressionAttributeValues = @{@":val":@50};

	[[dynamoDBObjectMapper query:[Book class]
                  expression:queryExpression]
 	continueWithBlock:^id(AWSTask *task) {
	     if (task.error) {
	         NSLog(@"The request failed. Error: [%@]", task.error);
	     }
	     if (task.exception) {
	         NSLog(@"The request failed. Exception: [%@]", task.exception);
	     }
	     if (task.result) {
	         AWSDynamoDBPaginatedOutput *paginatedOutput = task.result;
	         for (Book *book in paginatedOutput.items) {
	             //Do something with book.
	         }
	     }
	     return nil;
	 }];

In preceding code, ``indexName`` was specified since we are querying a index. We must also specify the ``hashKeyAttribute`` since the ``hashKeyAttribute`` name of the global secondary index is different from the table. We optionally specified ``rangeKeyConditionExpression`` and ``expressionAttributeValues`` to refine the query to only retrieve items with Price less than 50.
We can also provide ``filterExpression`` and ``projectionExpression`` in ``AWSDynamoDBQueryExpression``. The syntax is the same as that used in a scan operation.

For more information, see `AWSDynamoDBQueryExpression <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSDynamoDBQueryExpression.html>`_.

.. _conditional-writes:

Conditional Writes Using the Low-Level Client
=============================================

In a multi-user environment, multiple clients can access the same item and attempt to modify its attribute values at the same time. To help clients coordinate writes to data items, the DynamoDB low-level client supports conditional writes for ``PutItem``, ``DeleteItem``, and ``UpdateItem`` operations. With a conditional write, an operation succeeds only if the item attributes meet one or more expected conditions; otherwise, it returns an error.

In the following example, we update the price of an item in the Books table *if* the item has a "Price" value of "999"::

    AWSDynamoDB *dynamoDB = [AWSDynamoDB defaultDynamoDB];
    AWSDynamoDBUpdateItemInput *updateInput = [AWSDynamoDBUpdateItemInput new];

    AWSDynamoDBAttributeValue *hashKeyValue = [AWSDynamoDBAttributeValue new];
    hashKeyValue.S = @"4567890123";

    updateInput.tableName = @"Books";
    updateInput.key = @{ @"ISBN" : hashKeyValue };

    AWSDynamoDBAttributeValue *oldPrice = [AWSDynamoDBAttributeValue new];
    oldPrice.N = @"999";

    AWSDynamoDBExpectedAttributeValue *expectedValue = [AWSDynamoDBExpectedAttributeValue new];
    expectedValue.value = oldPrice;

    AWSDynamoDBAttributeValue *newPrice = [AWSDynamoDBAttributeValue new];
    newPrice.N = @"1199";

    AWSDynamoDBAttributeValueUpdate *valueUpdate = [AWSDynamoDBAttributeValueUpdate new];
    valueUpdate.value = newPrice;
    valueUpdate.action = AWSDynamoDBAttributeActionPut;

    updateInput.attributeUpdates = @{@"Price": valueUpdate};
    updateInput.expected = @{@"Price": expectedValue};
    updateInput.returnValues = AWSDynamoDBReturnValueUpdatedNew;

    [[dynamoDB updateItem:updateInput]
     continueWithBlock:^id(AWSTask *task) {
         if (task.error) {
             NSLog(@"The request failed. Error: [%@]", task.error);
         }
         if (task.exception) {
             NSLog(@"The request failed. Exception: [%@]", task.exception);
         }
         if (task.result) {
             //Do something with result.
         }
         return nil;
     }];


Note that conditional writes are idempotent. This means that you can send the same conditional write request multiple times, but it will have no further effect on the item after the first time DynamoDB performs the specified update. In the example above, sending the same request a second time would result in a ``ConditionalCheckFailedException``, because the expected condition would no longer be met after the first update.

.. _batch-operations:

Batch Operations Using the Low-Level Client
===========================================

The DynamoDB low-level client provides batch write operations to put items in the database and delete items from the database. You can also use batch get operations to return the attributes of one or more items from one or more tables

The following example illustrates a batch write operation::

    AWSDynamoDB *dynamoDB = [AWSDynamoDB defaultDynamoDB];

    //Write Request 1
    AWSDynamoDBAttributeValue *hashValue1 = [AWSDynamoDBAttributeValue new];
    hashValue1.S = @"3210987654";
    AWSDynamoDBAttributeValue *otherValue1 = [AWSDynamoDBAttributeValue new];
    otherValue1.S = @"Some Title";

    AWSDynamoDBWriteRequest *writeRequest = [AWSDynamoDBWriteRequest new];
    writeRequest.putRequest = [AWSDynamoDBPutRequest new];
    writeRequest.putRequest.item = @{
                                     @"ISBN" : hashValue1,
                                     @"Title" : otherValue1
                                     };

    //Write Request 2
    AWSDynamoDBAttributeValue *hashValue2 = [AWSDynamoDBAttributeValue new];
    hashValue2.S = @"8901234567";
    AWSDynamoDBAttributeValue *otherValue2 = [AWSDynamoDBAttributeValue new];
    otherValue2.S = @"Another Title";

    AWSDynamoDBWriteRequest *writeRequest2 = [AWSDynamoDBWriteRequest new];
    writeRequest2.putRequest = [AWSDynamoDBPutRequest new];
    writeRequest2.putRequest.item = @{
                                      @"ISBN" : hashValue2,
                                      @"Title" : otherValue2
                                      };

    AWSDynamoDBBatchWriteItemInput *batchWriteItemInput = [AWSDynamoDBBatchWriteItemInput new];
    batchWriteItemInput.requestItems = @{@"Books": @[writeRequest,writeRequest2]};

    [[dynamoDB batchWriteItem:batchWriteItemInput]
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

Additional Resources
====================

* `Amazon DynamoDB Developer Guide <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/>`_
* `Amazon DynamoDB API Reference <http://docs.aws.amazon.com/amazondynamodb/latest/APIReference/>`_

