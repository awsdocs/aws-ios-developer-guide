.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Amazon DynamoDB: Store and Retrieve Data
########################################

In this section:

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

