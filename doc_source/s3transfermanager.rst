.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Amazon S3 Transfer Manager for iOS
##################################

`Amazon Simple Storage Service (S3) <http://aws.amazon.com/s3/>`_ provides secure,
durable, highly-scalable object storage in the cloud. Using the AWS Mobile SDK, you can
directly access Amazon S3 from your mobile app.

Amazon S3 Transfer Manager makes it easy for you to upload and download files from S3
while optimizing for performance and reliability. It hides the complexity of transferring
files behind a simple API. Whenever possible, uploads are broken up into multiple pieces,
so that several pieces can be sent in parallel to provide better throughput. This approach
enables more robust transfers, since an I/O error in any individual piece means the SDK
only needs to retransmit the one affected piece, and not the entire transfer.

S3 Transfer Manager provides simple APIs to pause, resume, and cancel file transfers.
For information about S3 Region availability, see  `AWS Service Region Availability <http://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/>`_.

Getting Started
===============

This section provides a step-by-step guide for getting started with Amazon S3 using the
AWS Mobile SDK for iOS. You can also try out the
`Amazon S3 sample <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/S3TransferManager-Sample/
Objective-C>`_ available in the AWSLabs GitHub repository.

Get the SDK
-----------

To use S3 with your mobile app, first set up the AWS Mobile SDK for iOS:

#. Download the iOS SDK and include it in your iOS project, as described at :doc:`setup-aws-sdk-for-ios`.
#. Import the following header into your project


    .. container:: option

        Swift
            .. code-block:: swift

                import AWSS3


        Objective-C
            .. code-block:: objc

                #import <AWSS3/AWSS3.h>

Configure Credentials
---------------------

Amazon Cognito lets you create unique end user identifiers for accessing AWS cloud
services. You'll use Amazon Cognito to provide temporary AWS credentials to your app.

Log in to the `Cognito console <https://console.aws.amazon.com/cognito/>`_.

Create an identity pool and copy the Amazon Cognito client initialization code into your project. For more
information on setting up the Amazon Cognito client, see `Cognito Identity Developer Guide <http://docs.aws.amazon.com/cognito/devguide/identity/>`_.

Create and Configure an S3 Bucket
---------------------------------

Amazon S3 stores your resources in buckets |mdash| cloud storage containers that live in a
specific `region <http://docs.aws.amazon.com/general/latest/gr/rande.html>`_. Each S3 bucket
must have a globally unique name.

Let's use the AWS Management Console to create an S3 bucket.

Create an S3 Bucket
^^^^^^^^^^^^^^^^^^^
#. Sign in to the `S3 console <https://console.aws.amazon.com/s3/>`_ and click :guilabel:`Create Bucket`.
#. Enter a bucket name, select a region, and click create.

Grant Access to Your S3 Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default IAM role policy grants your application access to Amazon Mobile Analytics and Amazon Cognito Sync. In order for your Cognito identity pool to access Amazon S3, you must modify the identity pool's roles.

#. Navigate to the `Identity and Access Management Console`_ and click :guilabel:`Roles` in the left-hand pane.
#. Type your identity pool name into the search box. Two roles will be listed: one for unauthenticated users and one for authenticated users.
#. Click the role for unauthenticated users (it will have unauth appended to your Identity Pool name).
#. Click the :guilabel:`Create Role Policy` button, select :guilabel:`Policy Generator`, and then click the :guilabel:`Select` button.
#. On the Edit Permissions page, enter the settings shown in the following image. The Amazon Resource Name (ARN) of an S3 bucket looks like :code:`arn:aws:s3:::examplebucket/*` and is composed of the region in which the bucket is located and the name of the bucket. The settings shown below will give your identity pool full to access to all actions for the specified bucket.

    .. image:: images/edit-permissions.png

6. Click the :guilabel:`Add Statement` button and then the :guilabel:`Next Step` button.
7. The Wizard will show you the configuration that you generated. Click the :guilabel:`Apply Policy` button.

For more information on granting access to S3, see `Granting Access to an Amazon S3 Bucket`_.


Upload Files from the Console
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's seed the S3 bucket with a test file. We could do this programmatically, but for now
let's just use the console.

#. In the S3 console, in your bucket view, click :guilabel:`Upload`.
#. Click :guilabel:`Add Files` and select a test file to upload. For this tutorial, we'll
   assume you're uploading an image called :file:`myImage.jpg`.
#. With your test image selected, click :guilabel:`Start Upload`.

Create the S3 TransferManager Client
------------------------------------

To use the S3 TransferManager, we first need to create a TransferManager client


    .. container:: option

        Swift
            .. code-block:: swift

                let transferManager = AWSS3TransferManager.default()


        Objective-C
            .. code-block:: objc

                AWSS3TransferManager *transferManager = [AWSS3TransferManager defaultS3TransferManager];

The ``AWSS3TransferManager`` class is our entry point to the high-level S3 API.

Download an Object
==================

To download a file from a bucket, we have to construct the request using
``AWSS3TransferManagerDownloadRequest``. We then pass this request to the ``download`` method
of our client.

In the following snippet, we create an ``NSURL`` that we'll use for a download location.
Then we create a new download request object and set three properties on it:
the bucket name, the key (the name of the object in the bucket), and the URL where the file will be downloaded
(``downloadingFileURL``).


    .. container:: option

        Swift
            .. code-block:: swift

                let downloadingFileURL = URL(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent("myImage.jpg")

                let downloadRequest = AWSS3TransferManagerDownloadRequest()
                downloadRequest.bucket = "myBucket"
                downloadRequest.key = "myImage.jpg"
                downloadRequest.downloadingFileURL = downloadingFileURL

        Objective-C
            .. code-block:: objc

                // Construct the NSURL for the download location.
                NSString *downloadingFilePath = [NSTemporaryDirectory() stringByAppendingPathComponent:@"myImage.jpg"];
                NSURL *downloadingFileURL = [NSURL fileURLWithPath:downloadingFilePath];

                // Construct the download request.
                AWSS3TransferManagerDownloadRequest *downloadRequest = [AWSS3TransferManagerDownloadRequest new];

                downloadRequest.bucket = @"myBucket";
                downloadRequest.key = @"myImage.jpg";
                downloadRequest.downloadingFileURL = downloadingFileURL;

Now we can pass the download request to the ``download:`` method of the TransferManager client.
The AWS Mobile SDK for iOS uses `AWSTask` to support
asynchronous calls to Amazon Web Services. The ``download:`` method is asynchronous and returns a
``AWSTask`` object, so we'll use it accordingly.


    .. container:: option

        Swift
            .. code-block:: swift

                transferManager.download(downloadRequest).continueWith(executor: AWSExecutor.mainThread(), block: { (task:AWSTask<AnyObject>) -> Any? in

                    if let error = task.error as? NSError {
                        if error.domain == AWSS3TransferManagerErrorDomain, let code = AWSS3TransferManagerErrorType(rawValue: error.code) {
                            switch code {
                            case .cancelled, .paused:
                                break
                            default:
                                print("Error downloading: \(downloadRequest.key) Error: \(error)")
                            }
                        } else {
                            print("Error downloading: \(downloadRequest.key) Error: \(error)")
                        }
                        return nil
                    }
                    print("Download complete for: \(downloadRequest.key)")
                    let downloadOutput = task.result
                    return nil
                })

        Objective-C
            .. code-block:: objc

                // Download the file.
                [[transferManager download:downloadRequest ] continueWithExecutor:[AWSExecutor mainThreadExecutor]
                    withBlock:^id(AWSTask *task) {
                    if (task.error){
                        if ([task.error.domain isEqualToString:AWSS3TransferManagerErrorDomain]) {
                            switch (task.error.code) {
                                case AWSS3TransferManagerErrorCancelled:
                                case AWSS3TransferManagerErrorPaused:
                                break;

                                default:
                                    NSLog(@"Error: %@", task.error);
                                    break;
                            }

                        } else {
                            // Unknown error.
                            NSLog(@"Error: %@", task.error);
                        }
                    }

                    if (task.result) {
                        AWSS3TransferManagerDownloadOutput *downloadOutput = task.result;
                        //File downloaded successfully.
                    }
                    return nil;
                }];


In the example above, ``withBlock:`` is executed on the main thread.

We can display the downloaded image in a ``UIImageView``. Assuming ``UIImageView`` has been implemented,
we can do this as follows.

    .. container:: option

        Swift
            .. code-block:: swift

                self.imageView.image = UIImage(contentsOfFile: downloadingFileURL.path)


        Objective-C
            .. code-block:: objc

                self.imageView.image = [UIImage imageWithContentsOfFile:downloadingFilePath];

Note: in order for this image to display, we have to wait for the download to finish.

Upload an Object
================

Uploading an object with the S3 TransferManager is similar to downloading one. First we construct a
request object and then pass that request object the TransferManager client.
For the purposes of this example, let's say that we have an ``NSURL`` object, ``testFileURL``, that
represents the file we want to upload. We can build the request using ``AWSS3TransferManagerUploadRequest``,
as shown below.

    .. container:: option

        Swift
            .. code-block:: swift

                let uploadRequest = AWSS3TransferManagerUploadRequest()
                uploadRequest.bucket = "myBucket"
                uploadRequest.key = "myTestFile.txt"
                uploadRequest.body = URL(fileURLWithPath: "your/file/path/myTestFile.txt")

        Objective-C
            .. code-block:: objc

                AWSS3TransferManagerUploadRequest *uploadRequest = [AWSS3TransferManagerUploadRequest new];
                uploadRequest.bucket = @"myBucket";
                uploadRequest.key = @"myTestFile.txt";
                uploadRequest.body = testFileURL;

As with a download request, the ``key`` value will be the name of the object in the S3 bucket.
The ``body`` property of the request takes an ``NSURL`` object.

Having created the request, we can now pass it to the ``upload`` method of the TransferManager
client. The ``upload`` method returns a ``AWSTask`` object, so we'll again use
``continueWithExecutor:withBlock:`` to handle the upload.

    .. container:: option

        Swift
            .. code-block:: swift

                transferManager.upload(uploadRequest).continueWith(executor: AWSExecutor.mainThread(), block: { (task:AWSTask<AnyObject>) -> Any? in

                    if let error = task.error as? NSError {
                        if error.domain == AWSS3TransferManagerErrorDomain, let code = AWSS3TransferManagerErrorType(rawValue: error.code) {
                            switch code {
                            case .cancelled, .paused:
                                break
                            default:
                                print("Error uploading: \(uploadRequest.key) Error: \(error)")
                            }
                        } else {
                            print("Error uploading: \(uploadRequest.key) Error: \(error)")
                        }
                        return nil
                    }

                    let uploadOutput = task.result
                    print("Upload complete for: \(uploadRequest.key)")
                    return nil
                })

        Objective-C
            .. code-block:: objc

                [[transferManager upload:uploadRequest] continueWithExecutor:[AWSExecutor mainThreadExecutor]
                            withBlock:^id(AWSTask *task) {
                if (task.error) {
                    if ([task.error.domain isEqualToString:AWSS3TransferManagerErrorDomain]) {
                        switch (task.error.code) {
                            case AWSS3TransferManagerErrorCancelled:
                            case AWSS3TransferManagerErrorPaused:
                                break;

                            default:
                                NSLog(@"Error: %@", task.error);
                                break;
                        }
                    } else {
                        // Unknown error.
                        NSLog(@"Error: %@", task.error);
                    }
                }

                if (task.result) {
                    AWSS3TransferManagerUploadOutput *uploadOutput = task.result;
                    // The file uploaded successfully.
                }
                return nil;
            }];


Note that ``upload:`` is an asynchronous method and returns immediately. Since it doesn't
block the running thread, it's safe to call this method on the main thread.

Pause, Resume, and Cancel Object Transfers
==========================================

The TransferManager supports pause, resume, and cancel operations for both
uploads and downloads. ``pause``, ``cancel``, ``resumeAll``, ``cancelAll``, ``pauseAll``,
``upload:``, and ``download:`` all return instances of ``AWSTask``. Thus, you should
use these methods with a ``continueWithBlock`` to catch any errors. For example, a ``pause``
operation might look like this.

    .. container:: option

        Swift
            .. code-block:: swift

                uploadRequest.pause().continueWith(block: { (task:AWSTask<AnyObject>) -> Any? in
                    if let error = task.error as? NSError {
                        print("Error: \(error)")
                        return nil
                    }

                    // Upload has been paused.
                    return nil
                })


        Objective-C
            .. code-block:: objc

                [[self.uploadRequest pause] continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                        NSLog(@"Error: %@",task.error);
                    } else {
                        //Pause the upload.
                    }
                    return nil;
                }];

For the sake of brevity, the examples below omit the ``continueWithBlock``.

To pause an object transfer, call ``pause`` on the request object.

    .. container:: option

        Swift
            .. code-block:: swift

                uploadRequest.pause()
                downloadRequest.pause()


        Objective-C
            .. code-block:: objc

                [uploadRequest pause];
                [downloadRequest pause];

To resume a transfer, call ``upload`` or ``download``, as appropriate, and pass in
the paused request.

    .. container:: option

        Swift
            .. code-block:: swift

                transferManager.upload(uploadRequest)
                transferManager.download(downloadRequest)


        Objective-C
            .. code-block:: objc

                [transferManager upload:uploadRequest];
                [transferManager download:downloadRequest];

To cancel a transfer, call ``cancel`` on the upload or download request.

    .. container:: option

        Swift
            .. code-block:: swift

                uploadRequest.cancel()
                downloadRequest.cancel()


        Objective-C
            .. code-block:: objc

                [uploadRequest cancel];
                [downloadRequest cancel];

You can also perform pause, resume, and cancel operations in batches. To pause all of the current
upload and download requests, call ``pauseAll`` on the TransferManager.

    .. container:: option

        Swift
            .. code-block:: swift

                transferManager.pauseAll()

        Objective-C
            .. code-block:: objc

                [transferManager pauseAll];

To resume all of the current upload and download requests, call ``resumeAll`` on the TransferManager
and pass in an ``AWSS3TransferManagerResumeAllBlock``, which can be used to reset the progress
blocks for the requests.

    .. container:: option

        Swift
            .. code-block:: swift

                transferManager.resumeAll({ (request:AWSRequest?) in
                    // All paused requests have resumed.
                })


        Objective-C
            .. code-block:: objc

                [transferManager resumeAll:^(AWSRequest *request) {
                    //Resume paused requests.
                }];

To cancel all upload and download requests, call ``cancelAll`` on the TransferManager.

    .. container:: option

        Swift
            .. code-block:: swift

                transferManager.cancelAll()

        Objective-C
            .. code-block:: objc

                [transferManager cancelAll];

Track Progress
==============

Using the ``uploadProgress`` and ``downloadProgress`` blocks, you can track the progress of
object transfers. These blocks work in conjunction with the Grand Central Dispatch ``dispatch_async`` function,
as shown in the examples below.

Track the progress of an upload.

    .. container:: option

        Swift
            .. code-block:: swift

                    uploadRequest.uploadProgress = {(bytesSent: Int64, totalBytesSent: Int64, totalBytesExpectedToSend: Int64) -> Void in
                        DispatchQueue.main.async(execute: {() -> Void in
                            //Update progress.
                        })
                    }

        Objective-C
            .. code-block:: objc

                uploadRequest.uploadProgress =  ^(int64_t bytesSent, int64_t totalBytesSent, int64_t totalBytesExpectedToSend){
                    dispatch_async(dispatch_get_main_queue(), ^{
                    //Update progress.
                });

Track the progress of a download.

    .. container:: option

        Swift
            .. code-block:: swift


                downloadRequest.downloadProgress = {(bytesSent: Int64, totalBytesSent: Int64, totalBytesExpectedToSend: Int64) -> Void in
                    DispatchQueue.main.async(execute: {() -> Void in
                        //Update progress.
                    })
                }


        Objective-C
            .. code-block:: objc

                downloadRequest.downloadProgress = ^(int64_t bytesWritten, int64_t totalBytesWritten, int64_t totalBytesExpectedToWrite){
                dispatch_async(dispatch_get_main_queue(), ^{
                    //Update progress
                });

Multipart Upload
================

S3 provides a multipart upload feature that lets you upload a single object as a set of parts.
Each part is a contiguous portion of the object's data, and the object parts are uploaded
independently and in any order. If transmission of any part fails, you can retransmit that part
without affecting other parts. After all parts of the object are uploaded, S3 assembles
these parts and creates the object.

In the AWS Mobile SDK for iOS, the S3 TransferManager handles multipart upload for you. The
minimum part size for a multipart upload is 5MB.

Additional Resources
====================

* `Amazon Simple Storage Service Getting Started Guide <http://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html>`_
* `Amazon Simple Storage Service API Reference <http://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html>`_
* `Amazon Simple Storage Service Developer Guide <http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html>`_

.. _Identity and Access Management Console: https://console.aws.amazon.com/iam/home
.. _Granting Access to an Amazon S3 Bucket: http://blogs.aws.amazon.com/security/post/Tx3VRSWZ6B3SHAV/Writing-IAM-Policies-How-to-grant-access-to-an-Amazon-S3-bucket
