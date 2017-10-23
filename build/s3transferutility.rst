.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Amazon S3 TransferUtility for iOS
##################################

On this page:

.. contents::
   :local:
   :depth: 1

:guilabel:`Amazon Simple Storage Service (S3)`

`Amazon Simple Storage Service (S3) <http://aws.amazon.com/s3/>`_ provides secure,
durable, highly scalable object storage in the cloud. Using the AWS Mobile SDK for iOS, you can
directly access Amazon S3 from your mobile app. For information about Amazon S3 regional availability,
see  `AWS Service Region Availability <http://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/>`_.

:guilabel:`TransferUtility Features`

In addition to downloading, uploading, pausing, resuming and cancelling transfers, use the Amazon S3 TransferUtility class to transfer data to a file without saving a source file. This class also completes transfers in the background, even if the system suspends your app. User choice to suspend an app cancels in-progress transfers.

.. admonition:: Should I Use ``TransferManager`` or ``TransferUtility``?

    To choose which API best suits your needs, see :ref:`manager-or-utility`


Setup
=====

To set your project up to use ``TransferUtility``, take the steps below.

1. Setup the SDK, Credentials, and Services
-------------------------------------------

    Follow the steps described in :doc:`s3-setup-for-ios` to install the AWS Mobile SDK for iOS and configure
    AWS services, credentials, and permissions.

2. Import the SDK Amazon S3 APIs
--------------------------------

    Add the following import statements to your Xcode project.

        .. container:: option

            Swift
                .. code-block:: swift

                    import AWSS3

            Objective-C
                .. code-block:: objc

                    #import <AWSS3/AWSS3.h>

3. Configure the Application Delegate
---------------------------------------

    The Transfer Utility for iOS uses the background transfer feature in iOS to continue data
    transfers even when your app isn't running.

    Call the following method in ``- application:handleEventsForBackgroundURLSession:``
    ``completionHandler:`` of your application delegate. When the app in the foreground, the delegate
    enables iOS to notify ``TransferUtility`` that a transfer has completed.

        .. container:: option

            Swift
                .. code-block:: swift

                    func application(_ application: UIApplication, handleEventsForBackgroundURLSession identifier: String, completionHandler: @escaping () -> Void) {
                        // Store the completion handler. 
                        AWSS3TransferUtility.interceptApplication(application, handleEventsForBackgroundURLSession: identifier, completionHandler: completionHandler)
                    }


            Objective-C
                .. code-block:: objc


                    - (void)application:(UIApplication *)application handleEventsForBackgroundURLSession:(NSString *)identifier
                    completionHandler:(void (^)())completionHandler {
                        /* Store the completion handler.*/
                        [AWSS3TransferUtility interceptApplication:application handleEventsForBackgroundURLSession:identifier completionHandler:completionHandler];
                    }

Uploading a File
================

The following code for uploading a file by calling ``uploadFile:`` on ``AWSS3TransferUtility`` uses the
pattern that is common to all the types of transfers ``TransferUtility`` supports. For code examples for other kinds of transfer, see :ref:`more-examples`.
.

    .. container:: option

        Swift
            .. code-block:: swift

                let fileURL = // The file to upload
                let  transferUtility = AWSS3TransferUtility.default()
                transferUtility.uploadFile(fileURL,
                        bucket: S3BucketName,
                        key: S3UploadKeyName, 
                        contentType: "image/png",
                        expression: nil,
                        completionHandler: nil).continueWith {
                    (task) -> AnyObject! in if let error = task.error {
                        print("Error: \(error.localizedDescription)")
                    }

                    if let _ = task.result {
                        // Do something with uploadTask.
                    }
                    return nil;
                }

        Objective-C
            .. code-block:: objc

                NSURL *fileURL = // The file to upload.

                AWSS3TransferUtility *transferUtility = [AWSS3TransferUtility defaultS3TransferUtility];
                [[transferUtility uploadFile:fileURL
                                    bucket:@"YourBucketName"
                                    key:@"YourObjectKeyName"
                                    contentType:@"text/plain"
                                    expression:nil
                                    completionHandler:nil] continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                        NSLog(@"Error: %@", task.error);
                    }
                    if (task.result) {
                        AWSS3TransferUtilityUploadTask *uploadTask = task.result;
                        // Do something with uploadTask.
                    }

                    return nil;
                }];

.. _progress-completion:

Tracking Progress and Completion
================================

Implement progress and completion actions for TransferManager transfers by passing `progressBlock` and `completionHandler` blocks to the call to ``TransferUtility`` that initiates the transfer.

The following example of initiating a data upload shows how progress and completion handling is typically
done for all transfers.

    .. container:: option

        Swift
            .. code-block:: swift

                let data = // The data to upload

                let expression = AWSS3TransferUtilityUploadExpression()
                expression.progressBlock = {(task, progress) in DispatchQueue.main.async(execute: {
                        // Do something e.g. Update a progress bar.
                    })
                }

                let completionHandler = { (task, error) -> Void in
                    DispatchQueue.main.async(execute: {
                        // Do something e.g. Alert a user for transfer completion.
                        // On failed uploads, `error` contains the error object.
                    })
                }

                let  transferUtility = AWSS3TransferUtility.default()

                transferUtility.uploadData(data,
                            bucket: S3BucketName,
                            key: S3UploadKeyName,
                            contentType: "image/png",
                            expression: expression,
                            completionHandler: completionHandler).continueWith { (task) -> AnyObject! in
                    if let error = task.error {
                        print("Error: \(error.localizedDescription)")
                    }

                    if let _ = task.result {
                        // Do something with uploadTask.
                    }

                    return nil;
                }


        Objective-C
            .. code-block:: objc

                NSData *dataToUpload = // The data to upload.

                AWSS3TransferUtilityUploadExpression *expression = [AWSS3TransferUtilityUploadExpression new];
                expression.progressBlock = ^(AWSS3TransferUtilityTask *task, NSProgress *progress) {
                    dispatch_async(dispatch_get_main_queue(), ^{
                        // Do something e.g. Update a progress bar.
                    });
                };


                AWSS3TransferUtilityUploadCompletionHandlerBlock completionHandler = ^(AWSS3TransferUtilityUploadTask *task, NSError *error) {
                    dispatch_async(dispatch_get_main_queue(), ^{
                        // Do something e.g. Alert a user for transfer completion.
                        // On failed uploads, `error` contains the error object.
                    });
                };

                AWSS3TransferUtility *transferUtility = [AWSS3TransferUtility defaultS3TransferUtility];
                [[transferUtility uploadData:dataToUpload
                                bucket:@"YourBucketName"
                                key:@"YourObjectKeyName"
                                contentType:@"text/plain"
                                expression:expression
                                completionHandler:completionHandler] continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                        NSLog(@"Error: %@", task.error);
                    }
                    if (task.result) {
                       AWSS3TransferUtilityUploadTask *uploadTask = task.result;
                        // Do something with uploadTask.
                    }

                    return nil;
                }];

.. _managing-transfers:

Managing Transfers
==================

This section describes how to manage ``TransferUtility`` transfers at different points in the app lifecycle.

With the App in the Foreground
------------------------------

To suspend, resume, and cancel uploads and downloads, retain references to
``AWSS3TransferUtilityUploadTask`` and ``AWSS3TransferUtilityDownloadTask``.
To manage data transfers call ``suspend``, ``resume``, and ``cancel`` on those tasks.
The following example shows the ``cancel`` method being called on an upload.

    .. container:: option

        Swift
            .. code-block:: swift

                transferUtility.uploadFile(fileURL,
                        bucket: S3BucketName,
                        key: S3UploadKeyName,
                        contentType: "image/png",
                        expression: nil,
                        completionHandler: nil).continueWith {
                    (task) -> AnyObject! in if let error = task.error {
                        print("Error: \(error.localizedDescription)")
                    }

                    if let uploadTask = task.result {
                        uploadTask.cancel()
                    }
                    return nil;
                }

        Objective-C
            .. code-block:: objc

                [[transferUtility uploadFile:fileURL
                                    bucket:@"YourBucketName"
                                    key:@"YourObjectKeyName"
                                    contentType:@"text/plain"
                                    expression:nil
                                    completionHandler:nil] continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                        NSLog(@"Error: %@", task.error);
                    }
                    if (task.result) {
                        AWSS3TransferUtilityUploadTask *uploadTask = task.result;
                        [uploadTask cancel]
                    }

                    return nil;
                }];

When a Suspended App Returns to the Foreground
----------------------------------------------

Upon App Returning to the Foreground

When an app that has initiated a ``TransferUtility`` transfer becomes suspended and then returns to the foreground, the transfer may still be in progress or may have completed. In both cases, use the following code to reestablish the transfer as being handled by progress and completion blocks of the app in the foreground.

The code uses downloading a file as the example but the pattern also works for upload:

You receive ``AWSS3TransferUtilityUploadTask`` and ``AWSS3TransferUtilityDownloadTask`` when you initiate the upload and download respectively. These tasks have a property called ``taskIdentifier``, which uniquely identifies the transfer task object within the Transfer Utility. Your app should persist the identifier through closure and relaunch, so that you can uniquely identify the task objects when the app is comes back into the foreground.

   .. container:: option

        Swift
            .. code-block:: swift

                override func viewDidLoad() {
                super.viewDidLoad()

                ...

                let transferUtility = AWSS3TransferUtility.default()

                var uploadProgressBlock: AWSS3TransferUtilityProgressBlock? = {(task: AWSS3TransferUtilityTask, progress: Progress) in
                    DispatchQueue.main.async {
                        // Handle progress feedback, e.g. update progress bar
                    }
                }
                var downloadProgressBlock: AWSS3TransferUtilityProgressBlock? = {
                    (task: AWSS3TransferUtilityTask, progress: Progress) in DispatchQueue.main.async {
                        // Handle progress feedback, e.g. update progress bar
                    }
                }
                var completionBlockUpload:AWSS3TransferUtilityUploadCompletionHandlerBlock? = {
                    (task, error) in DispatchQueue.main.async {
                        // perform some action on completed upload operation
                    }
                }
                var completionBlockDownload:AWSS3TransferUtilityDownloadCompletionHandlerBlock? = {
                    (task, url, data, error) in DispatchQueue.main.async {
                        // perform some action on completed download operation
                    }
                }

                transferUtility.enumerateToAssignBlocks(forUploadTask: {
                    (task, progress, completion) -> Void in

                        let progressPointer = AutoreleasingUnsafeMutablePointer<AWSS3TransferUtilityProgressBlock?>(& uploadProgressBlock)

                        let completionPointer = AutoreleasingUnsafeMutablePointer<AWSS3TransferUtilityUploadCompletionHandlerBlock?>(&completionBlockUpload)

                        // Reassign your progress feedback
                        progress?.pointee = progressPointer.pointee

                        // Reassign your completion handler.
                        completion?.pointee = completionPointer.pointee

                }, downloadTask: {
                    (task, progress, completion) -> Void in

                        let progressPointer = AutoreleasingUnsafeMutablePointer<AWSS3TransferUtilityProgressBlock?>(&downloadProgressBlock)

                        let completionPointer = AutoreleasingUnsafeMutablePointer<AWSS3TransferUtilityDownloadCompletionHandlerBlock?>(&completionBlockDownload)

                        // Reassign your progress feedback
                        progress?.pointee = progressPointer.pointee

                        // Reassign your completion handler.
                        completion?.pointee = completionPointer.pointee
                })

                 if let downloadTask = task.result {
                    // Do something with downloadTask.
                }

        Objective-C
            .. code-block:: objc

                - (void)viewDidLoad {
                    [super viewDidLoad];

                    ...

                    AWSS3TransferUtility *transferUtility = [AWSS3TransferUtility defaultS3TransferUtility];
                    [transferUtility enumerateToAssignBlocksForUploadTask:^(
                        AWSS3TransferUtilityUploadTask *uploadTask,
                        __autoreleasing AWSS3TransferUtilityUploadProgressBlock *uploadProgressBlockReference,
                        __autoreleasing AWSS3TransferUtilityUploadCompletionHandlerBlock *completionHandlerReference
                    ) {
                        NSLog(@"%lu", (unsigned long)uploadTask.taskIdentifier);

                        // Use `uploadTask.taskIdentifier` to determine what blocks to assign.

                        *uploadProgressBlockReference = ...; // Reassign your progress feedback block.
                        *completionHandlerReference = ...; // Reassign your completion handler.
                    }
                    downloadTask:^(AWSS3TransferUtilityDownloadTask *downloadTask, __autoreleasing AWSS3TransferUtilityDownloadProgressBlock *downloadProgressBlockReference, __autoreleasing AWSS3TransferUtilityDownloadCompletionHandlerBlock *completionHandlerReference) {
                        NSLog(@"%lu", (unsigned long)downloadTask.taskIdentifier);

                            // Use `downloadTask.taskIdentifier` to determine what blocks to assign.
                       *downloadProgressBlockReference =  // Reassign your progress feedback block.
                       *completionHandlerReference = // Reassign your completion handler.
                    }];
                }

                if (task.result) {
                    AWSS3TransferUtilityUploadTask *downloadTask = task.result;
                    // Do something with downloadTask.
                }

.. _more-examples:

More Transfer Examples
======================

This section provides descriptions and abbreviated examples of the aspects of each type of
transfer that are unique. For information about typical code surrounding the following snippets
see :ref:`managing-transfers` and :ref:`progress-completion`.

Downloading to a File
---------------------

The following code shows how to download a file.

    .. container:: option

        Swift
            .. code-block:: swift

                let fileURL = // The file URL of the download destination.

                // Add progress and completion blocks
                . . .

                let  transferUtility = AWSS3TransferUtility.default()
                transferUtility.download(
                        to: fileURL
                        bucket: S3BucketName,
                        key: S3DownloadKeyName,
                        expression: expression,
                        completionHandler: completionHandler
                ).continueWith {
                    (task) -> AnyObject! in if let error = task.error {
                        print("Error: \(error.localizedDescription)")
                    }

                    if let _ = task.result {
                        // Do something with downloadTask.
                    }
                    return nil;
                }

        Objective-C
            .. code-block:: objc

                NSURL *fileURL = ...; // The file URL of the download destination.

                // Add progress and completion blocks
                . . .

                AWSS3TransferUtility *transferUtility = [AWSS3TransferUtility defaultS3TransferUtility];
                [[transferUtility downloadToURL:nil
                                bucket:S3BucketName
                                key:S3DownloadKeyName
                                expression:expression
                                completionHandler:completionHandler] continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                        NSLog(@"Error: %@", task.error);
                    }
                    if (task.result) {
                        AWSS3TransferUtilityDownloadTask *downloadTask = task.result;
                        // Do something with downloadTask.
                    }

                    return nil;
                }];

Uploading Binary Data to a File
-------------------------------

To upload data to a file in Amazon S3 call ``uploadData:``.

This method saves the data as a file in a temporary directory. The next time ``AWSS3TransferUtility`` is
initialized, the expired temporary files are cleaned up. If you upload many large objects to an Amazon S3 bucket in a short period of time, it is more efficient to use the upload file method and then manually purge the unnecessary temporary files as early as possible.

    .. container:: option

        Swift
            .. code-block:: swift

                let data = // The data to upload

                // Add progress and completion blocks
                . . .

                let  transferUtility = AWSS3TransferUtility.default()

                transferUtility.uploadData(data,
                            bucket: S3BucketName,
                            key: S3UploadKeyName,
                            contentType: "image/png",
                            expression: expression,
                            completionHandler: completionHandler).continueWith { (task) -> AnyObject! in
                    if let error = task.error {
                        print("Error: \(error.localizedDescription)")
                    }
 
                    if let _ = task.result {
                        // Do something with uploadTask.
                    }

                    return nil;
                }


        Objective-C
            .. code-block:: objc

                NSData *dataToUpload = // The data to upload.

                // Add progress and completion blocks
                . . .

                AWSS3TransferUtility *transferUtility = [AWSS3TransferUtility defaultS3TransferUtility];
                [[transferUtility uploadData:dataToUpload
                                bucket:@"YourBucketName"
                                key:@"YourObjectKeyName"
                                contentType:@"text/plain"
                                expression:expression
                                completionHandler:completionHandler] continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                        NSLog(@"Error: %@", task.error);
                    }
                    if (task.result) {
                        AWSS3TransferUtilityUploadTask *uploadTask = task.result;
                        // Do something with uploadTask.
                    }

                    return nil;
                }];


Downloading Binary Data to a File
---------------------------------

The following code shows how to download binary a file.

    .. container:: option

        Swift
            .. code-block:: swift

                let fileURL = // The file URL of the download destination.

                // Add progress and completion blocks
                . . .

                let  transferUtility = AWSS3TransferUtility.default()
                transferUtility.downloadData(
                        fromBucket: S3BucketName,
                        key: S3DownloadKeyName,
                        expression: expression,
                        completionHandler: completionHandler
                ).continueWith {
                    (task) -> AnyObject! in if let error = task.error {
                        print("Error: \(error.localizedDescription)")
                    }

                    if let _ = task.result {
                        // Do something with downloadTask.
                    }

                    return nil;
                }

        Objective-C
            .. code-block:: objc

                AWSS3TransferUtilityDownloadExpression *expression = [AWSS3TransferUtilityDownloadExpression new];

                // Add progress and completion blocks
                . . .

                AWSS3TransferUtility *transferUtility = [AWSS3TransferUtility defaultS3TransferUtility];
                [[transferUtility downloadDataFromBucket:S3BucketName
                    key:S3DownloadKeyName
                    expression:expression
                    completionHandler:completionHandler] continueWithBlock:^id(AWSTask *task) {
                        if (task.error) {
                            NSLog(@"Error: %@", task.error);
                        }
                        if (task.result) {
                            AWSS3TransferUtilityDownloadTask *downloadTask = task.result;
                            // Do something with downloadTask.
                        }

                        return nil;
                    }
                ];


Limitations
===========

The S3 Transfer Utility generates Amazon S3 pre-signed URLs to use for background data transfer.
Using Amazon Cognito Identity, you receive AWS temporary credentials. The credentials are valid for up to 60 minutes.
At the same time, generated S3 pre-signed URLs cannot last longer than that time. Because of this
limitation, the Amazon S3 Transfer Utility enforces 50 minute transfer timeouts, leaving a 10 minute
buffer before AWS temporary credentials are regenerated. After 50 minutes, you receive a transfer failure.

If you need to transfer data that cannot be transferred in under 50 minutes, use `AWSS3` instead.
