.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Amazon S3: Store and Retrieve Files and Data
############################################

`Amazon Simple Storage Service (S3) <http://aws.amazon.com/s3/>`_ provides secure,
durable, highly-scalable object storage in the cloud. Using the AWS Mobile SDK, you can
directly access Amazon S3 from your mobile app.

In this section:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   Setup for Amazon S3 Integration <s3-setup-for-ios>
   TransferManager for File Transfers <s3transfermanager>
   TransferUtility for File and Data Transfers <s3transferutility>
   Presigned URLs for File Access <s3-pre-signed-urls>
   Server-side Encryption for Transfers <s3-server-side-encryption>

.. _manager-or-utility:

Should I Use TransferManager or TransferUtility?
================================================

Both the Amazon S3 TransferManager and TransferUtitliy classes make it easy for you to upload and download files from Amazon S3 while optimizing for performance and reliability. Both hide the complexity of making asynchronous file transfers behind simple APIs. Both provide the ability to pause, resume, and cancel file transfers.

The differences are as follows.

- Use ``TransferUtility`` to:

  - Make background file or data transfers that complete even if the system suspends an app invoking the transfer

  - Transfer binary data to a file with out saving a file at the transfer source location first.

- Use ``TransferManager`` to make file transfers that happen while the app is in the foreground.

  Whenever possible, ``TransferManager`` uploads are broken up into multiple pieces. Several pieces can be sent in parallel to provide better throughput that is resilient to I/O errors.

Additional Resources
====================

For information about Amazon S3 regional availability, see  `AWS Service Region Availability <http://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/>`_.

* `Amazon Simple Storage Service Getting Started Guide <http://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html>`_
* `Amazon Simple Storage Service API Reference <http://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html>`_
* `Amazon Simple Storage Service Developer Guide <http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html>`_

.. _Identity and Access Management Console: https://console.aws.amazon.com/iam/home
.. _Granting Access to an Amazon S3 Bucket: http://blogs.aws.amazon.com/security/post/Tx3VRSWZ6B3SHAV/Writing-IAM-Policies-How-to-grant-access-to-an-Amazon-S3-bucket
