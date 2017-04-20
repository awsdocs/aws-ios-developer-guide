.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Amazon S3 Integration Setup
###########################

To integrate Amazon S3 features of the AWS SDK for iOS into an app, take the following steps.


Create and configure the following AWS services and policies.

#. Install the SDK

   Add the AWS SDK for iOS to your project and import the APIs you need, by following the steps
   in :doc:`setup-aws-sdk-for-ios`.

#. Configure credentials

   To use Amazon Cognito to create AWS identities and credentials that give your users access to your app's AWS resources, follow the steps in :doc:`cognito-auth-aws-identity-for-ios`.


#. Create and configure an Amazon S3 bucket

   Amazon S3 stores your resources in buckets, which are AWS containers for objects. Buckets are created in
   specific `regions <http://docs.aws.amazon.com/general/latest/gr/rande.html>`_. Each bucket
   must have a globally unique name.

   :guilabel:`Create a bucket`

    #. Sign in to the `Amazon S3 console <https://console.aws.amazon.com/s3/>`_.

    #. Choose :guilabel:`Create Bucket`.

    #. Type a bucket name, choose a region, and then choose :guilabel:`Create Bucket`.


   :guilabel:`Grant Permissions`

   Like most AWS service objects, Amazon S3 buckets have access policies attached to them that you can use to
   grant permissions for IAM entities, such as roles or individual identities. Take the following steps to grant
   the unauthenticated IAM role of your app's identity pool permissions to the bucket you created.

    #. Navigate to the `Identity and Access Management console`_.

    #. Choose :guilabel:`Roles` in the left navigation pane.

    #. Type your identity pool name into the search box. Two roles are listed: one for unauthenticated users and one for authenticated users.

    #. Choose the role for unauthenticated users (it has `unauth` appended to your identity pool name).

    #. At the bottom of the :guilabel:`Permissions` tab, find the policy AWS attached when you created the role and choose :guilabel:`Create Role Policy`.

    #. Choose :guilabel:`Custom Policy`, and then choose :guilabel:`Select`.

    #. Enter a name in :guilabel:`Policy Name`, and then copy and paste the following policy statement into the
       :guilabel:`Policy Document` area.


        .. code-block:: json

                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": ["s3:*"],
                            "Resource": ["arn:aws:s3:::examplebucket/"]
                        }
                    ]
                }

    #. Choose :guilabel:`Apply Policy`.

    This policy grants the user permissions for all actions in all objects in the specified bucket. For more information on granting access to Amazon S3, see `Granting Access to an Amazon S3 Bucket`_.


   :guilabel:`Upload files from the console`

   The following steps describe how to manually upload the file used in this walk through to the
   bucket you have created.

    #. In the `Amazon S3 console <https://console.aws.amazon.com/s3/>`_, navigate to your bucket.

    #. In the :guilabel:`Actions`drop down menu, choose :guilabel:`Upload`.

    #. Choose :guilabel:`+ Add Files` and select a test file to upload. For this walk through, we'll
       assume you're uploading an image called :file:`myImage.jpg`.

    #. With your test image selected, choose :guilabel:`Start Upload`.


Additional Resources
====================

* `Amazon Simple Storage Service Getting Started Guide <http://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html>`_
* `Amazon Simple Storage Service API Reference <http://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html>`_
* `Amazon Simple Storage Service Developer Guide <http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html>`_

.. _Identity and Access Management Console: https://console.aws.amazon.com/iam/home
.. _Granting Access to an Amazon S3 Bucket: http://blogs.aws.amazon.com/security/post/Tx3VRSWZ6B3SHAV/Writing-IAM-Policies-How-to-grant-access-to-an-Amazon-S3-bucket
