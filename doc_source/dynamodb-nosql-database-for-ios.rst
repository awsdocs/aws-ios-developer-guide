.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Amazon DynamoDB: Store and Retrieve Data
########################################

<<<<<<< HEAD
In this section:
=======
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

#. Download the iOS SDK and include it in your iOS project, as described at :doc:`setup-aws-sdk-for-ios`.
#. Import the following header (Objective-C) or library (Swift) into your project.

    .. container:: option

        Swift
            .. code-block:: swift

                import AWSDynamoDB


        Objective-C
            .. code-block:: objc

                #import <AWSDynamoDB/AWSDynamoDB.h>

Configure Credentials
---------------------

Amazon Cognito lets you create unique end user identifiers for accessing AWS cloud
services. You'll use Amazon Cognito to provide temporary AWS credentials to your app.

#. Log in to the `Cognito console <https://console.aws.amazon.com/cognito/>`_.

#. Create an identity pool. For this tutorial, you don't need to configure public identity providers, OpenID Connect providers, or developer authenticated identities. But do enable unauthenticated identities.

#. Amazon Cognito creates and assigns new IAM roles for you. When you have the option, select :guilabel:`Update Roles`.

#. Copy the auto-generated Amazon Cognito client initialization code into your project. For this tutorial, you won't need the store-and-synchronize snippet.

For more information on setting up the Amazon Cognito client, see `Cognito Identity Developer Guide <http://docs.aws.amazon.com/cognito/devguide/identity/>`_.

Create a DynamoDB Table and Index
---------------------------------

For this tutorial, let's assume we're building a bookstore app. Our app will need to keep track of the books available in the bookstore, and we can create a DynamoDB table to do so.

To create the Books table:

#. Log in to the `DynamoDB Console <https://console.aws.amazon.com/dynamodb/home>`_.
#. Click :guilabel:`Create Table`.
#. Enter :command:`Books` as the name of the table.
#. Enter :command:`ISBN` in the :guilabel:`Partition key` field of the :guilabel:`Primary key` with :guilabel:`String` as its type.
#. Uncheck the :guilabel:`Use default settings` checkbox and click :guilabel:`+ Add Index`.
#. In the :guilabel:`Add Index` dialog enter :command:`Author` with :guilabel:`String` as its type.
#. Check the :guilabel:`Add sort key` checkbox and enter :command:`Title` as the sort key value, with :guilabel:`String` as its type.
#. Leave the other values at their defaults and click :guilabel:`Add index` to add the :command:`Author-Title-index` index.
#. Set the read capacity to ``10`` and the write capacity to ``5``.
#. Click :guilabel:`Create`. DynamoDB will create your database.
#. Refresh the console and select your Books table from the list of tables.
#. Open the :guilabel:`Overview` tab and copy or note the Amazon Resource Name (ARN). You'll need
   this in a moment.

Set Permissions
---------------

To use DynamoDB in an application, you must set the correct permissions. The following IAM policy allows the user to perform the actions shown in this tutorial on two resources (a table and an index) identified by `ARN <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_.

    .. code-block:: json

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

Apply this policy to the unauthenticated role assigned to your Amazon Cognito identity pool, replacing the ``Resource`` values with the correct ARN for your DynamoDB table:

#. Log in to the `IAM console <https://console.aws.amazon.com/iam>`_.
#. Select :guilabel:`Roles` and select the "Unauth" role that Amazon Cognito created for you.
#. Click :guilabel:`Attach Role Policy`.
#. Select :guilabel:`Custom Policy` and click :guilabel:`Select`.
#. Enter a name for your policy and paste in the policy document shown above, replacing the ``Resource`` values with the ARNs for your table and index. (You can retrieve the table ARN from the :guilabel:`Details` tab of the database; then append :file:`/index/*` to obtain the value for the index ARN.
#. Click :guilabel:`Apply Policy`.

To learn more about IAM policies, see `Using IAM <http://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_Introduction.html>`_. To learn more about DynamoDB-specific policies, see `Using IAM to Control Access to DynamoDB Resources <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/UsingIAMWithDDB.html>`_.

Create a DynamoDB Object Mapper Client
--------------------------------------

We're going to use the `AWSDynamoDBObjectMapper <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSDynamoDBObjectMapper.html>`_ to map a client-side class to our database. The Object Mapper supports high-level operations like creating, getting, querying, updating, and deleting records. We can create an Object Mapper as follows.

    .. container:: option

        Swift
            .. code-block:: swift

                let dynamoDBObjectMapper = AWSDynamoDBObjectMapper.default()


        Objective-C
            .. code-block:: objc

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

Here's the Objective-C header for our ``Book`` class.

    .. container:: option

        Objective-C
            .. code-block:: objc

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

Here's the implementation of our model.

    .. container:: option

        Swift
            .. code-block:: swift

                import AWSDynamoDB

                class Book : AWSDynamoDBObjectModel, AWSDynamoDBModeling  {
                    var Title:String?
                    var Author:String?
                    var Price:String?
                    var ISBN:String?

                    class func dynamoDBTableName() -> String {
                        return "Books"
                    }

                    class func hashKeyAttribute() -> String {
                        return "ISBN"
                    }
                }

        Objective-C
            .. code-block:: objc

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

First, we create the object that we want to save.

    .. container:: option

        Swift
            .. code-block:: swift

                let myBook = Book()
                myBook?.ISBN = "3456789012"
                myBook?.Title = "The Scarlet Letter"
                myBook?.Author = "Nathaniel Hawthorne"
                myBook?.Price = 899 as NSNumber?


        Objective-C
            .. code-block:: objc

                Book *myBook = [Book new];
                myBook.ISBN = @"3456789012";
                myBook.Title = @"The Scarlet Letter";
                myBook.Author = @"Nathaniel Hawthorne";
                myBook.Price = [NSNumber numberWithInt:899];

And then we pass the object to the ``save:`` method.

    .. container:: option

        Swift
            .. code-block:: swift

                dynamoDBObjectMapper.save(myBook).continueWith(block: { (task:AWSTask<AnyObject>!) -> Any? in
                    if let error = task.error as? NSError {
                        print("The request failed. Error: \(error)")
                    } else {
                        // Do something with task.result or perform other operations.
                    }
                })


        Objective-C
            .. code-block:: objc

                [[dynamoDBObjectMapper save:myBook]
                continueWithBlock:^id(AWSTask *task) {
                     if (task.error) {
                         NSLog(@"The request failed. Error: [%@]", task.error);
                     } else {
                         //Do something with task.result or perform other operations.
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

Here's an example of setting a default save behavior on the Object Mapper.

    .. container:: option

        Swift
            .. code-block:: swift

                let updateMapperConfig = AWSDynamoDBObjectMapperConfiguration()
                updateMapperConfig.saveBehavior = .updateSkipNullAttributes

        Objective-C
            .. code-block:: objc

                AWSDynamoDBObjectMapperConfiguration *updateMapperConfig = [AWSDynamoDBObjectMapperConfiguration new];
                updateMapperConfig.saveBehavior = AWSDynamoDBObjectMapperSaveBehaviorUpdateSkipNullAttributes;

Then we can use ``updateMapperConfig`` as an argument when calling `save:configuration: <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSDynamoDBObjectMapper.html#//api/name/save:configuration:>`_.
>>>>>>> 2d27673736d46efba52e9219b62818dd436fa027

.. toctree::
   :maxdepth: 1
   :titlesonly:

   Setup for Amazon DynamoDB for iOS <dynamodb-setup-for-ios>
   Amazon DynamoDB DynamoDBMapper <dynamodb-object-mapper>
   Amazon DynamoDB Low-level Client <dynamodb-low-level-client>


`Amazon DynamoDB <http://aws.amazon.com/dynamodb/>`_ is a fast, highly scalable,
highly available, cost-effective, non-relational database service. Amazon DynamoDB removes traditional
scalability limitations on data storage while maintaining low latency and predictable
performance.

The AWS Mobile SDK for iOS provides both low-level and high-level libraries for working with Amazon DynamoDB.
Both allow you to perform create, read, update, and delete (CRUD) operations and to execute queries and scans.

The high-level library includes Amazon DynamoDB object mapper which lets you map client-side classes to tables. Working within the data model defined on your client you can write simple, readable code that stores and retrieves objects in the cloud.  See :doc:`dynamodb-object-mapper`.

The low-level client allows you to access and manipulate Amazon DynamoDB tables directly for NoSQL or other non-relational data designs. The low-level library also supports conditional writes, to mitigate issues with simultaneous writes by multiple users, and batch operations. See :doc:`dynamodb-low-level-client`.

Get Started
===========

You can explore Amazon DynamoDB in the following ways:

- :doc:`dynamodb-setup-for-ios`: Use the walkthroughs provided in this SDK.

- `Try the NoSQL Database feature in the AWS Mobile Hub console <https://aws.amazon.com/mobile>`_:

    - Intuitively design and provisioning of AWS services in minutes
    - Quickstart app demonstrating the services you configure (Android, Swift, or Objective-C)
    - SDK with helper code that can be dropped into your Xcode project
    - Step-by-step instructions for integrating your services into an existing mobile app

    Sign in with your AWS account and create a Mobile hub project - both free - then select NoSQL Database.

- `DynamoDB sample <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/DynamoDBObjectMapper-Sample>`_:
  Download and build the sample app from Github


Additional Resources
====================

* For information Amazon DynamoDB Region availability, see  `AWS Service Region Availability
  <http://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/>`_.
* `Amazon DynamoDB Developer Guide <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/>`_
* `Amazon DynamoDB API Reference <http://docs.aws.amazon.com/amazondynamodb/latest/APIReference/>`_

