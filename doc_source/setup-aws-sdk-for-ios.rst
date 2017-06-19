.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

.. _setup-ios:

======================
Set Up the SDK for iOS
======================

To get started with the AWS Mobile SDK for iOS you can set up the SDK and build a new
project, or you can integrate the SDK in an existing project. You can also run the samples to
get a sense of how the SDK works.

To use the SDK, install the following on your development machine:

- Xcode 7 or later

- iOS 8 or later

You can view the source code in the `AWS Mobile SDK for iOS GitHub repository <https://github.com/aws/aws-sdk-ios>`_.

.. _include_sdk_ios:

Include the AWS Mobile SDK for iOS in an Existing Application
#############################################################

The samples included with the SDK are standalone projects that are already set up. You can also integrate the SDK into your own existing project. Choose one of the following three ways to import the SDK into your project:

- Cocoapods
- Carthage
- Dynamic Frameworks

.. note:: Importing the SDK in multiple ways loads duplicate copies of the SDK into the project and causes compiler errors.

.. container:: option

    CocoaPods
        #. The AWS Mobile SDK for iOS is available through `CocoaPods <http://cocoapods.org/>`_. Install CocoaPods by running the following commands from the folder containing your projects :file:`*.xcodeproj` file.

            $ :command:`gem install cocoapods`

           ..note:: Depending on your system settings, you may need to run the command as administrator using `sudo`, as follows:

                $ :command:`sudo gem install cocoapods`

            $ :command:`pod setup`

            $ :command:`pod init`

        #. In your project directory (the directory where your :file:`*.xcodeproj` file is), open the empty text file named :file:`Podfile` (without a file extension) and add the following lines to the file. Replace ``myAppName`` with your app name. You can also remove pods for services that you don't use. For example, if you don't use `AWSAutoScaling`, remove or do not include the ``AWSAutoScaling`` pod.

            .. code-block:: javascript

                source 'https://github.com/CocoaPods/Specs.git'

                platform :ios, '8.0'
                use_frameworks!

                target :'myAppName' do
                    pod 'AWSAutoScaling'
                    pod 'AWSCloudWatch'
                    pod 'AWSCognito'
                    pod 'AWSCognitoIdentityProvider'
                    pod 'AWSDynamoDB'
                    pod 'AWSEC2'
                    pod 'AWSElasticLoadBalancing'
                    pod 'AWSIoT'
                    pod 'AWSKinesis'
                    pod 'AWSLambda'
                    pod 'AWSLex'
                    pod 'AWSMachineLearning'
                    pod 'AWSMobileAnalytics'
                    pod 'AWSPinpoint'
                    pod 'AWSPolly'
                    pod 'AWSRekognition'
                    pod 'AWSS3'
                    pod 'AWSSES'
                    pod 'AWSSimpleDB'
                    pod 'AWSSNS'
                    pod 'AWSSQS'
                end

        #. Run the following command:

            $ :command:`pod install`

        #. Open :file:`*.xcworkspace` with Xcode and start using the SDK.

            .. note::

                Do not open :file:`*.xcodeproj`. Opening this project file instead of a workspace results in an error.

    Carthage
        #. Install the latest version of `Carthage <https://github.com/Carthage/Carthage#installing-carthage>`_.

        #. Add the following to your `Cartfile`::

            github "aws/aws-sdk-ios"

        #. Run the following command:

            $ :command:`carthage update`

        #. With your project open in Xcode, choose your **Target**. In the **General** tab, find **Embedded Binaries**,  then choose the **+** button.

        #. Choose the **Add Other** button, navigate to the ``AWS<#ServiceName#>.framework`` files under **Carthage** > **Build** > **iOS** and select ``AWSCore.framework`` and the other service frameworks you require. Do not select the **Destination: Copy items if needed** checkbox when prompted.

            * ``AWSCore.framework``
            * ``AWSAutoScaling.framework``
            * ``AWSCloudWatch.framework``
            * ``AWSCognito.framework``
            * ``AWSCognitoIdentityProvider.framework``
            * ``AWSDynamoDB.framework``
            * ``AWSEC2.framework``
            * ``AWSElasticLoadBalancing.framework``
            * ``AWSIoT.framework``
            * ``AWSKinesis.framework``
            * ``AWSLambda.framework``
            * ``AWSLex.framework``
            * ``AWSMachineLearning.framework``
            * ``AWSMobileAnalytics.framework``
            * ``AWSPinpoint.framework``
            * ``AWSPolly.framework``
            * ``AWSRekognition.framework``
            * ``AWSS3.framework``
            * ``AWSSES.framework``
            * ``AWSSimpleDB.framework``
            * ``AWSSNS.framework``
            * ``AWSSQS.framework``

        #. Under the **Build Phases** tab in your **Target**, choose the **+** button on the top left and then select **New Run Script Phase**.

        # Setup the build phase as follows. Make sure this phase is below the **Embed Frameworks** phase.

            .. code-block:: bash


                Shell /bin/sh

                bash "${BUILT_PRODUCTS_DIR}/${FRAMEWORKS_FOLDER_PATH}/AWSCore.framework/strip-frameworks.sh"

                Show environment variables in build log: Checked
                Run script only when installing: Not checked

                Input Files: Empty
                Output Files: Empty

    Frameworks
        #. Download the SDK from http://aws.amazon.com/mobile/sdk. The SDK is stored in a compressed
           file archive named :file:`aws-ios-sdk-#.#.#`, where '#.#.#' represents the version number. For version
           2.5.0, the filename is :file:`aws-ios-sdk-2.5.0`.


        #. With your project open in Xcode, choose your **Target**. Under the **General** tab, find
           **Embedded Binaries** and then choose the **+** button.

        #. Choose **Add Other**. Navigate to the ``AWS<#ServiceName#>.framework`` files
           and select ``AWSCore.framework`` and the other service frameworks you require. Select
           the **Destination: Copy items if needed** checkbox when prompted.

            * ``AWSCore.framework``
            * ``AWSAutoScaling.framework``
            * ``AWSCloudWatch.framework``
            * ``AWSCognito.framework``
            * ``AWSCognitoIdentityProvider.framework``
            * ``AWSDynamoDB.framework``
            * ``AWSEC2.framework``
            * ``AWSElasticLoadBalancing.framework``
            * ``AWSIoT.framework``
            * ``AWSKinesis.framework``
            * ``AWSLambda.framework``
            * ``AWSLex.framework``
            * ``AWSMachineLearning.framework``
            * ``AWSMobileAnalytics.framework``
            * ``AWSPinpoint.framework``
            * ``AWSPolly.framework``
            * ``AWSRekognition.framework``
            * ``AWSS3.framework``
            * ``AWSSES.framework``
            * ``AWSSimpleDB.framework``
            * ``AWSSNS.framework``
            * ``AWSSQS.framework``

        4. Under the **Build Phases** tab in your **Target**, click the **+** button on the top left and then select **New Run Script Phase**.

        #. Setup the build phase as follows. Make sure this phase is below the `Embed Frameworks` phase.

            .. code-block:: bash

                Shell /bin/sh

                bash "${BUILT_PRODUCTS_DIR}/${FRAMEWORKS_FOLDER_PATH}/AWSCore.framework/strip-frameworks.sh"

                Show environment variables in build log: Checked
                Run script only when installing: Not checked

                Input Files: Empty
                Output Files: Empty

Update the SDK to a Newer Version
#################################

This section describes how to pick up changes when a new SDK is released.

.. container:: option

    CocoaPods
        Run the following command in your project directory. CocoaPods automatically picks up the changes.

        :command:`$ pod update`

        .. note::

            If your pod update command fails, delete :file:`Podfile.lock` and :file:`Pods/`
            and then run :command:`pod install` to cleanly install the SDK.

    Carthage
        Run the following command in your project directory. Carthage automatically updates
        your frameworks with the new changes.

        :command:`$ carthage update`

    Frameworks
        #. In Xcode select the following frameworks in **Project Navigator** and press the **delete** key. Then select **Move to Trash**:

            * ``AWSCore.framework``
            * ``AWSAutoScaling.framework``
            * ``AWSCloudWatch.framework``
            * ``AWSCognito.framework``
            * ``AWSCognitoIdentityProvider.framework``
            * ``AWSDynamoDB.framework``
            * ``AWSEC2.framework``
            * ``AWSElasticLoadBalancing.framework``
            * ``AWSIoT.framework``
            * ``AWSKinesis.framework``
            * ``AWSLambda.framework``
            * ``AWSLex.framework``
            * ``AWSMachineLearning.framework``
            * ``AWSMobileAnalytics.framework``
            * ``AWSPinpoint.framework``
            * ``AWSPolly.framework``
            * ``AWSRekognition.framework``
            * ``AWSS3.framework``
            * ``AWSSES.framework``
            * ``AWSSimpleDB.framework``
            * ``AWSSNS.framework``
            * ``AWSSQS.framework``

        #. Follow the :ref:`manual Frameworks installation process <install-frameworks>` to include the new version of the SDK.

Preparing to Work with ATS
##########################

The `App Transport Security (ATS) <https://developer.apple.com/library/prerelease/ios/technotes/App-Transport-Security-Technote/>`_
feature, in the iOS 9.0 SDK or later, might impact how your apps interact with some AWS services.

If you compile your apps with the iOS 9.0 SDK (or Xcode 7) or later, there are additional steps you must
complete for your app to successfully connect with any AWS service your app calls. For more information,
see `Preparing Your App to Work with ATS <http://docs.aws.amazon.com/mobile/sdkforios/developerguide/ats.html>`_.

AWS Credentials
###############

We recommend using Amazon Cognito as your credential provider to access AWS services from your
mobile app. Amazon Cognito provides a secure mechanism to access AWS services without having to embed
credentials in your app. To learn more, see :doc:`cognito-auth-aws-identity-for-ios`.

Alternatively, you can use `AWS Identity and Access
Management <http://aws.amazon.com/iam/>`_ (IAM) in combination with the `AWS Security Token Service AssumeRole API <http://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_. If you choose IAM, ensure that your role's policy is minimally scoped so that it can only perform the required actions for the service being used.

Import and Call SDK APIs with AWS Credentials
#############################################

This section is included to give an overview of how you can connect your app to AWS services. For details about calling a specific service, see the left hand menu.

#. Import the AWSCore header in the application delegate.

    .. container:: option

        Swift
            .. code-block:: swift

                import AWSCore
                import AWSCognito

        Objective-C
            .. code-block:: objc

                #import <AWSCore/AWSCore.h>
                #import <AWSCognito/AWSCognito.h>

   Amazon Cognito APIs provide AWS identity services, and are included because they are
   used in the implementation of most mobile app features through AWS.

#. Create a default service configuration and establish an AWS identity provider by adding the following code
   snippet in the ``application:didFinishLaunchingWithOptions:`` application delegate method.

    .. container:: option

        Swift
            .. code-block:: swift

                let credentialProvider = AWSCognitoCredentialsProvider(regionType: .USEast1, identityPoolId: "YourIdentityPoolId")
                let configuration = AWSServiceConfiguration(region: .USEast1, credentialsProvider: credentialProvider)
                AWSServiceManager.default().defaultServiceConfiguration = configuration

        Objective-C
            .. code-block:: objc

                AWSCognitoCredentialsProvider *credentialsProvider = [[AWSCognitoCredentialsProvider alloc] initWithRegionType:AWSRegionUSEast1
                identityPoolId:@"YourIdentityPoolId"];

                AWSServiceConfiguration *configuration = [[AWSServiceConfiguration alloc] initWithRegion:AWSRegionUSEast1 credentialsProvider:credentialsProvider];

                AWSServiceManager.defaultServiceManager.defaultServiceConfiguration = configuration;

   The value for ``YourIdentityPoolId`` is specific to the Amazon Cognito identity pool you create. To learn
   more, see :doc:`cognito-auth-aws-identity-for-ios`.


#. Include import statements for each AWS service your app will call.

    .. container:: option

        Swift
            .. code-block:: swift

                import AWSS3
                import AWSDynamoDB
                import AWSSQS
                import AWSSNS
                ...

        Objective-C
            .. code-block:: objc

               #import <AWSCore/AWSCore.h>
               #import <AWSS3/AWSS3.h>
               #import <AWSDynamoDB/AWSDynamoDB.h>
               #import <AWSSQS/AWSSQS.h>
               #import <AWSSNS/AWSSNS.h>
               ...

#. Make a call to your AWS service. In the example below, the call is to Amazon S3
   through the SDKs AWSS3TransferManger API.

    .. container:: option

        Swift
            .. code-block:: swift

                let transferManager = AWSS3TransferManager.default()

                let uploadRequest = AWSS3TransferManagerUploadRequest()
                uploadRequest.bucket = "myBucket"
                uploadRequest.key = "myTestFile.txt"
                uploadRequest.body = uploadingFileURL
                uploadRequest.contentLength = fileSize

                transferManager.upload(uploadRequest).continueWith(executor: AWSExecutor.mainThread(), block: { (task:AWSTask<AnyObject>) -> Any? in
                    // Do something with the response
                })


        Objective-C
            .. code-block:: objc

               AWSS3Transfermanager *transferManager = [AWSS3Transfermanager defaultS3TransferManager];

               AWSS3TransferManagerUploadRequest *uploadRequest = [AWSS3TransferManagerUploadRequest new];
               uploadRequest.bucket = yourBucket;
               uploadRequest.key = yourKey;
               uploadRequest.body = yourDataURL;
               uploadRequest.contentLength = [NSNumber numberWithUnsignedLongLong:fileSize];

               [[transferManager upload:uploadRequest] continueWithBlock:^id(AWSTask *task) {
                   // Do something with the response
                   return nil;
               }];

    .. note::

        Most of the service client classes have a singleton method to get a default client, named with the convention of adding ``default`` to the framework name.
        ``AWSS3TransferManager.default()`` (Swift) or ``defaultS3TransferManager`` (Objective-C)
        are examples in the preceding code snippet.

        This singleton method creates a service client with ``defaultServiceConfiguration``, which you
        initialized in the application delegate during a preceding step in this section. The method
        maintains a strong reference to the client.



Logging
#######

As of version 2.5.4 of this SDK, logging utilizes `CocoaLumberjack SDK <https://github.com/CocoaLumberjack/CocoaLumberjack>`_, a flexible, fast, open source logging framework. It supports many capabilities including the ability to set logging level per output target, for instance, concise messages logged to the console and verbose messages to a log file.

CocoaLumberjack logging levels are additive such that when the level is set to verbose, all messages from the levels below verbose are logged. It is also possible to set custom logging to meet your needs. For more information, see `CocoaLumberjack Logging Levels <https://github.com/CocoaLumberjack/CocoaLumberjack/blob/master/Documentation/CustomLogLevels.md>`_

Changing Logging Level
=======================

You can change the logging level to suit the phase of your development cycle by importing AWSCore and calling:

    .. container:: option

        Swift
            :code:`AWSDDLog.sharedInstance().logLevel = .verbose`

            The following logging level options are available:

            - ``.off``
            - ``.error``
            - ``.warning``
            - ``.info``
            - ``.debug``
            - ``.verbose``

            We recommend setting the log level to ``.off`` before publishing to the App Store.

        Objective-C
            :code:`[AWSDDLog sharedInstance].logLevel = AWSDDLogLevelVerbose;`

            The following logging level options are available:

            - ``AWSDDLogLevelOff``
            - ``AWSDDLogLevelError``
            - ``AWSDDLogLevelWarning``
            - ``AWSDDLogLevelInfo``
            - ``AWSDDLogLevelDebug``
            - ``AWSDDLogLevelVerbose``

            We recommend setting the log level to ``AWSDDLogLevelOff`` before publishing to the App Store.


Targeting Log Output
====================

CocoaLumberjack can direct logs to file or used as a framework that integrates with the Xcode console.

To initialize logging to files, use the following code:

    .. container:: option

        Swift
            .. code-block:: swift

                let fileLogger: AWSDDFileLogger = AWSDDFileLogger() // File Logger
                fileLogger.rollingFrequency = TimeInterval(60*60*24)  // 24 hours
                fileLogger.logFileManager.maximumNumberOfLogFiles = 7
                AWSDDLog.add(fileLogger)

        Objective-C
            .. code-block:: objc

                AWSDDFileLogger *fileLogger = [[AWSDDFileLogger alloc] init]; // File Logger
                fileLogger.rollingFrequency = 60 * 60 * 24; // 24 hour rolling
                fileLogger.logFileManager.maximumNumberOfLogFiles = 7;
                [AWSDDLog addLogger:fileLogger];

To initialize logging to your Xcode console, use the following code:

    .. container:: option

        Swift
            .. code-block:: swift

                AWSDDLog.add(AWSDDTTYLogger.sharedInstance) // TTY = Xcode console

        Objective-C
            .. code-block:: objc

                [AWSDDLog addLogger:[AWSDDTTYLogger sharedInstance]]; // TTY = Xcode console

To learn more, see `CocoaLumberjack <https://github.com/CocoaLumberjack/CocoaLumberjack>`_ on GitHub.

Sample Apps
###########

The AWS Mobile SDK for iOS includes sample apps that demonstrate common use cases.

**Amazon Cognito Your User Pools Sample** (`Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/CognitoYourUserPools-Sample/Objective-C/>`__)

    This sample demonstrates how sign up and sign in a user to display an authenticated portion of your app.

    AWS services demonstrated:

    - `Amazon Cognito Pools <http://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html>`_
    - `Amazon Cognito Identity <http://aws.amazon.com/cognito/>`_

**Amazon Cognito Sync Sample**
(`Swift <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/CognitoSync-Sample/Swift/>`__,
`Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/CognitoSync-Sample/Objective-C/>`__)

    This sample demonstrates how to securely manage and sync your mobile app data. It also demonstrates how to create unique identities using login providers including Facebook, Google, and Login with Amazon.

    AWS services demonstrated:

    - `Amazon Cognito Sync <http://aws.amazon.com/cognito/>`_
    - `Amazon Cognito Identity <http://aws.amazon.com/cognito/>`_

**Amazon DynamoDB Object Mapper Sample**
(`Swift <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/DynamoDBObjectMapper-Sample/Swift>`__, `Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/DynamoDBObjectMapper-Sample/Objective-C/>`__)

    This sample demonstrates how to insert, update, delete, query items using DynamoDBObjectMapper.

    AWS services demonstrated:

    - `Amazon DynamoDB <http://aws.amazon.com/dynamodb/>`_
    - `Amazon Cognito Identity <http://aws.amazon.com/cognito/>`_

**Amazon S3 Transfer Utility Sample**
(`Swift <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/S3TransferUtility-Sample/Swift/>`__, `Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/S3TransferUtility-Sample/Objective-C/>`__)

    This sample demonstrates how to use the Amazon S3 TransferUtility to download / upload files.

    AWS services demonstrated:

    - `Amazon S3 <http://aws.amazon.com/s3/>`_
    - `Amazon Cognito Identity <http://aws.amazon.com/cognito/>`_

**Amazon SNS Mobile Push and Mobile Analytics Sample**
(`Swift <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/SNS-MobileAnalytics-Sample/Swift/>`__, `Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/SNS-MobileAnalytics-Sample/Objective-C/>`_)

    This sample demonstrates how to set up Amazon SNS mobile push notifications and to record events using Amazon Mobile Analytics.

    AWS services demonstrated:

    - `Amazon SNS (mobile push notification) <http://aws.amazon.com/sns/>`_
    - `Amazon Mobile Analytics <http://aws.amazon.com/mobileanalytics/>`_
    - `Amazon Cognito Identity <http://aws.amazon.com/cognito/>`_

Install the Reference Documentation in Xcode
############################################

The AWS Mobile SDK for iOS includes documentation in the DocSets format that you can view within
Xcode. The easiest way to install the documentation is to use the macOS terminal.

To install the DocSet for Xcode
===============================

Open the macOS terminal and go to the directory containing the expanded
archive. For example:

    :command:`$ cd ~/Downloads/aws-ios-sdk-2.5.0`

.. note::

    Replace :command:`2.5.0` in the preceding example with the
    version number of the AWS Mobile SDK for iOS that you downloaded.

Create a directory called
:file:`~/Library/Developer/Shared/Documentation/DocSets`:


    :command:`$ mkdir -p ~/Library/Developer/Shared/Documentation/DocSets`

Copy (or move) :file:`documentation/com.amazon.aws.ios.docset`
from the SDK installation files to the directory you created in the previous
step:

    :command:`$ mv documentation/com.amazon.aws.ios.docset ~/Library/Developer/Shared/Documentation/DocSets/`

If Xcode was running during this procedure, restart Xcode. To browse the
documentation, go to :strong:`Help`, click :strong:`Documentation and API Reference`, and select :strong:`AWS Mobile SDK for iOS v2.0 Documentation`
(where '2.0' is the appropriate version number).
