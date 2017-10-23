.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Amazon DynamoDB Integration Setup
#################################

This section provides a step-by-step guide for getting started with Amazon DynamoDB using the AWS Mobile SDK for iOS.

Get the SDK
-----------

To use Amazon DynamoDB in your mobile app, first set up the AWS Mobile SDK for iOS:

#. Download the iOS SDK and include it in your iOS project, as described in :doc:`setup-aws-sdk-for-ios`.

#. Install the SDK

   Add the AWS SDK for iOS to your project and import the APIs you need, by following the steps
   in :doc:`setup-aws-sdk-for-ios`.

#. Configure credentials

   To use Amazon Cognito to create AWS identities and credentials that give your users access to your app's AWS resources, follow the steps in :doc:`cognito-auth-aws-identity-for-ios`.

For more information on setting up the Amazon Cognito client, see `Using Federated Identities <http://docs.aws.amazon.com/cognito/devguide/identity/>`_ in the `Amazon Cognito Developer Guide`.


Create an Amazon DynamoDB Table and Index
-----------------------------------------

This tutorial is based on a simple bookstore app. The app tracks the books that are available in the bookstore using an Amazon DynamoDB table.

To create the Books table:

#. Sign in to the `Amazon DynamoDB Console <https://console.aws.amazon.com/dynamodb/home>`_.
#. Choose :guilabel:`Create Table`.
#. Type :command:`Books` as the name of the table.
#. Enter :command:`ISBN` in the :guilabel:`Partition key` field of the :guilabel:`Primary key` with :guilabel:`String` as their type.
#. Clear the :guilabel:`Use default settings` checkbox and choose :guilabel:`+ Add Index`.
#. In the :guilabel:`Add Index` dialog type :command:`Author` with :guilabel:`String` as the type.
#. Check the :guilabel:`Add sort key` checkbox and enter :command:`Title` as the sort key value, with :guilabel:`String` as its type.
#. Leave the other values at their defaults. Choose :guilabel:`Add index` to add the :command:`Author-Title-index` index.
#. Set the read capacity to `10` and the write capacity to `5`.
#. Choose :guilabel:`Create`.Amazon DynamoDB will create your database.
#. Refresh the console and choose your Books table from the list of tables.
#. Open the :guilabel:`Overview` tab and copy or note the Amazon Resource Name (ARN). You need this for the next procedure.

Set Permissions
---------------

To use Amazon DynamoDB in your mobile app, you must set the correct permissions. The following IAM policy allows the user to perform the actions shown in this tutorial on two resources (a table and an index) identified by an `ARN <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_.

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

Apply this policy to the unauthenticated role assigned to your Amazon Cognito identity pool, replacing the `Resource` values with the correct ARN for the Amazon DynamoDB table:

#. Sign in to the `IAM console <https://console.aws.amazon.com/iam>`_.
#. Choose :guilabel:`Roles` and then choose the "Unauth" role that Amazon Cognito created for you.
#. Choose :guilabel:`Attach Role Policy`.
#. Choose :guilabel:`Custom Policy` and then Choose :guilabel:`Select`.
#. Type a name for your policy and paste in the policy document shown above, replacing the `Resource` values with the ARNs for your table and index. (You can retrieve the table ARN from the :guilabel:`Details` tab of the database; then append :file:`/index/*` to obtain the value for the index ARN.
#. Choose :guilabel:`Apply Policy`.

To learn more about IAM policies, see `Using IAM <http://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_Introduction.html>`_. To learn more about creating fine-grained access policies for Amazon DynamoDB, see `DynamoDB on Mobile – Part 5: Fine-Grained Access Control <https://aws.amazon.com/blogs/mobile/dynamodb-on-mobile-part-5-fine-grained-access-control/>`_.
