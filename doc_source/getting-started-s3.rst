.. Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Store and Retrieve Files with Amazon S3
=======================================

.. highlight:: objc

Authenticate Users with Cognito Identity
----------------------------------------

Cognito Identity provides secure access to AWS services. Identities are managed by an identity pool. Roles specify resources an identity can access and are associated with an identity pool. To create an identity pool for your application:

#. Log into the `Cognito Console`_ and click the :guilabel:`New Identity Pool` button
#. Give your Identity Pool a unique name and enable access to unauthenticated identities
#. Click the :guilabel:`Create Pool` button and then the :guilabel:`Update Roles` to create your identity pool and associated roles

For more information on Cognito Identity, see :doc:`cognito-auth`

Add the following import statement:
::

	#import <AWSCore/AWSCore.h>

Add the following code to application:didFinishLaunchingWithOptions method:
::

	AWSCognitoCredentialsProvider *credentialsProvider = [[AWSCognitoCredentialsProvider alloc] initWithRegionType:AWSRegionUSEast1
		identityPoolId:@"<your-identity-pool-arn>"];

	AWSServiceConfiguration *configuration = [[AWSServiceConfiguration alloc] initWithRegion:AWSRegionUSEast1
		credentialsProvider:credentialsProvider];

	AWSServiceManager.defaultServiceManager.defaultServiceConfiguration = configuration;

.. Note::
	If you have an existing credential provider, you do not need to create a new one.

For more information on Cognito Identity, see :doc:`cognito-auth`.

Grant Access to your S3 Resources
---------------------------------

Configure your Cognito Identity to have access to the S3 buckets in your AWS account:

1. Navigate to the `Identity and Access Management Console`_ and click :guilabel:`Roles` in the left-hand pane.
2. Type your Identity Pool name into the search box - two roles will be listed one for unauthenticated users and one for authenticated users.
3. Click the role for unauthenticated users (it will have unauth appended to your Identity Pool name).
4. Click the :guilabel:`Create Role Policy` button, select :guilabel:`Policy Generator`, and click the :guilabel:`Select` button.
5. In the Edit Permissions page make the settings shown in the following image:

.. image:: images/edit-permissions.png

.. Note::
	These settings will give your Identity Pool full access to all of the S3 buckets in your AWS account.

6. Click the :guilabel:`Add Statement` button and then the :guilabel:`Next Step` button.
7. The Wizard will show you the configuration generated, click the :guilabel:`Apply Policy` button.

For more information on granting access to S3, see `Granting Access to an Amazon S3 Bucket`_.

Upload a File to Amazon S3
--------------------------

Create a AWSS3TransferManagerUploadRequest instance specifying the file to upload and the destination bucket:
::

    AWSS3TransferManagerUploadRequest *uploadRequest = [AWSS3TransferManagerUploadRequest new];
    uploadRequest.bucket = @"example-bucket";
    uploadRequest.key = @"test.txt";
    uploadRequest.body = self.downloadFileURL;

Submit the upload request to the S3 service asynchronously:
::

    AWSS3TransferManager *transferManager = [AWSS3TransferManager defaultS3TransferManager];

    [[transferManager upload:uploadRequest] continueWithExecutor:[AWSExecutor mainThreadExecutor]
                                                       withBlock:^id(AWSTask *task) {
          if (task.error != nil) {
 		 	NSLog(@"%s %@","Error uploading :", uploadRequest.key);
         }
         else { NSLog(@"Upload completed"); }
         return nil;
     }];

Download a File from Amazon S3
------------------------------

Create a destination URL where file will be downloaded:
::

    NSString *downloadingFilePath = [NSTemporaryDirectory() stringByAppendingPathComponent:FileName];
    NSURL *downloadingFileURL = [NSURL fileURLWithPath:downloadingFilePath];


Create the download request:
::

    AWSS3TransferManagerDownloadRequest *downloadRequest = [AWSS3TransferManagerDownloadRequest new];
    downloadRequest.bucket = BucketName;
    downloadRequest.key = FileName;
    downloadRequest.downloadingFileURL = downloadingFileURL;

Submit the download request:
::

    AWSS3TransferManager *transferManager = [AWSS3TransferManager defaultS3TransferManager];
    self.txtLabel.text = @"Download started, please wait...";

    [[transferManager download:downloadRequest] continueWithExecutor:[AWSExecutor mainThreadExecutor]
                                                           withBlock:^id(AWSTask *task){
         if (task.error != nil) {
             NSLog(@"%s %@","Error downloading :", downloadRequest.key);
         }
         else {
             NSLog(@"download completed");
             self.txtLabel.text = @"Download completed";
         }
         return nil;
     }];

This exercise assumes the use of an unauthenticated identity provided by Amazon Cognito. For more information on using authenticated identities, see :doc:`cognito-auth`.

For more information on accessing Amazon S3 from an iOS application, see `Calling Amazon S3 from iOS Apps`_.

.. _Cognito Console: https://console.aws.amazon.com/cognito/home
.. _Identity and Access Management Console: https://console.aws.amazon.com/iam/home
.. _Granting Access to an Amazon S3 Bucket: http://blogs.aws.amazon.com/security/post/Tx3VRSWZ6B3SHAV/Writing-IAM-Policies-How-to-grant-access-to-an-Amazon-S3-bucket
.. _Calling Amazon S3 from iOS Apps: http://docs.aws.amazon.com/mobile/sdkforios/developerguide/s3transfermanager.html
