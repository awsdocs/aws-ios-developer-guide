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

The iOS SDK provides the following components to support the variety of ways the Amazon S3 service can be used in iOS apps.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   s3transfermanager
   s3transferutility
   s3-pre-signed-urls
   s3-server-side-encryption

Amazon S3 Transfer Manager
==========================

The Amazon S3 Transfer Manager makes it easy for you to upload and download files from S3
while optimizing for performance and reliability. S3 Transfer Manager provides simple APIs to
pause, resume, and cancel file transfers.It hides the complexity of transferring
files behind a simple API. Whenever possible, uploads are broken up into multiple pieces,
so that several pieces can be sent in parallel to provide better throughput. This approach
enables more robust transfers, since an I/O error in any individual piece means the SDK
only needs to retransmit the one affected piece, and not the entire transfer.

Learn more at :doc:`s3transfermanager`.

Amazon S3 Transfer Utility
==========================

The AWS iOS SDK provides the Amazon S3 Transfer Utility further simplifies background
transfer of data between your iOS app and Amazon S3. This API should be used where the
granular control allowed by use of the Transfer Manager, in concert with pre-signed urls, is not needed.

The Amazon S3 Transfer Utility offers two main advantages over the S3 Transfer Manager:

    * Ability to continue transferring data in the background without the need to explicitly use pre-signed urls

    * An API to upload binary data without first requiring it be saved as a file. The S3 Transfer Manager requires you to save data to a file before passing it to Transfer Manager.

Learn more at :doc:`s3transferutility`.

Pre-signed URLs for Amazon S3 Transfers
=======================================

The iOS SDK provides Pre-signed URLs that facilitate performing data transfers in the background. Learn more at :doc:`s3-pre-signed-urls`.


Server Side Encryption for Amazon S3
====================================

The AWS iOS SDK supports server-side encryption of Amazon S3 data. Learn more at :doc:`s3-server-side-encryption`.

Additional Resources
====================

For information about S3 Region availability, see  `AWS Service Region Availability <http://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/>`_.

* `Amazon Simple Storage Service Getting Started Guide <http://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html>`_
* `Amazon Simple Storage Service API Reference <http://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html>`_
* `Amazon Simple Storage Service Developer Guide <http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html>`_

.. _Identity and Access Management Console: https://console.aws.amazon.com/iam/home
.. _Granting Access to an Amazon S3 Bucket: http://blogs.aws.amazon.com/security/post/Tx3VRSWZ6B3SHAV/Writing-IAM-Policies-How-to-grant-access-to-an-Amazon-S3-bucket
