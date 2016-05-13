.. Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

.. highlight:: objc

.. _setup-ios:

======================
Set Up the SDK for iOS
======================

To get started with the AWS SDK for iOS, you can set up the SDK and start building a new
project, or you integrate the SDK in an existing project. You can also run the samples to
get a sense of how the SDK works.

To use the AWS SDK for iOS, you will need the following installed on your development
machine:

- Xcode 7 or later

- iOS 8 or later

At the AWS GitHub repo, you can check out the `SDK source code <https://github.com/aws/aws-sdk-ios>`_.

.. _include_sdk_ios:

Include the SDK for iOS in an Existing Application
##################################################

The samples included with the SDK for iOS are standalone projects that are already set up for you. You can also integrate the SDK for iOS with your own existing project. There are three ways to import the AWS Mobile SDK for iOS into your project:

- CocoaPods
- Carthage
- Dynamic Frameworks

You should use one of these three ways to import the AWS Mobile SDK but not multiple. Importing the SDK in multiple ways loads duplicate copies of the SDK into the project and causes compiler errors.

CocoaPods
=========

#. The AWS Mobile SDK for iOS is available through `CocoaPods <http://cocoapods.org/>`_. If you have not installed CocoaPods, install it by running the command:

    :command:`$ gem install cocoapods`

    :command:`$ pod setup`

    Depending on your system settings, you may have to use `sudo` for installing `cocoapods` as follows:

    :command:`$ sudo gem install cocoapods`

    :command:`$ pod setup`

#. In your project directory (the directory where your :file:`*.xcodeproj` file is), create a plain text file named :file:`Podfile` (without any file extension) and add the lines below. Replace `YourTarget` with your actual target name.::

    source 'https://github.com/CocoaPods/Specs.git'
    
    platform :ios, '8.0'
    use_frameworks!
    
    target :'YourTarget' do
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
        pod 'AWSMachineLearning'
        pod 'AWSMobileAnalytics'
        pod 'AWSS3'
        pod 'AWSSES'
        pod 'AWSSimpleDB'
        pod 'AWSSNS'
        pod 'AWSSQS'
    end


#. Then run the following command:

    :command:`$ pod install`

#. Open up :file:`*.xcworkspace` with Xcode and start using the SDK.

.. note:: Do NOT use :file:`*.xcodeproj`. If you open up a project file instead of a workspace, you receive an error.

Carthage
==========
#. Install the latest version of `Carthage <https://github.com/Carthage/Carthage#installing-carthage>`_.

#. Add the following to your `Cartfile`::

	    github "aws/aws-sdk-ios"

#. Then run the following command:
	
	    :command:`$ carthage update`

#. With your project open in Xcode, select your **Target**. Under **General** tab, find **Embedded Binaries** and then click the **+** button.

#. Click the **Add Other...** button, navigate to the `AWS<#ServiceName#>.framework` files under `Carthage` > `Build` > `iOS` and select them. Do not check the **Destination: Copy items if needed** checkbox when prompted.

    * `AWSCore.framework`
    * `AWSAutoScaling.framework`
    * `AWSCloudWatch.framework`
    * `AWSCognito.framework`
    * `AWSCognitoIdentityProvider.framework`
    * `AWSDynamoDB.framework`
    * `AWSEC2.framework`
    * `AWSElasticLoadBalancing.framework`
    * `AWSIoT.framework`
    * `AWSKinesis.framework`
    * `AWSLambda.framework`
    * `AWSMachineLearning.framework`
    * `AWSMobileAnalytics.framework`
    * `AWSS3.framework`
    * `AWSSES.framework`
    * `AWSSimpleDB.framework`
    * `AWSSNS.framework`
    * `AWSSQS.framework`

#. Under the **Buid Phases** tab in your **Target**, click the **+** button on the top left and then select **New Run Script Phase**. Then setup the build phase as follows. Make sure this phase is below the `Embed Frameworks` phase.::

	    Shell /bin/sh
	    
	    bash "${BUILT_PRODUCTS_DIR}/${FRAMEWORKS_FOLDER_PATH}/AWSCore.framework/strip-frameworks.sh"
	    
	    Show environment variables in build log: Checked
	    Run script only when installing: Not checked
	    
	    Input Files: Empty
	    Output Files: Empty

Frameworks
==========

#. Download the SDK from http://aws.amazon.com/mobile/sdk. The SDK is stored in a compressed
   file archive named :file:`aws-ios-sdk-#.#.#` (where '#.#.#' represents the version number, so for version
   2.2.2, the filename is
   :file:`aws-ios-sdk-2.2.2`).


#. With your project open in Xcode, select your **Target**. Under **General** tab, find **Embedded Binaries** and then click the **+** button.

#. Click the **Add Other...** button, navigate to the `AWS<#ServiceName#>.framework` files and select them. Check the **Destination: Copy items if needed** checkbox when prompted.

    * `AWSCore.framework`
    * `AWSAutoScaling.framework`
    * `AWSCloudWatch.framework`
    * `AWSCognito.framework`
    * `AWSCognitoIdentityProvider.framework`
    * `AWSDynamoDB.framework`
    * `AWSEC2.framework`
    * `AWSElasticLoadBalancing.framework`
    * `AWSIoT.framework`
    * `AWSKinesis.framework`
    * `AWSLambda.framework`
    * `AWSMachineLearning.framework`
    * `AWSMobileAnalytics.framework`
    * `AWSS3.framework`
    * `AWSSES.framework`
    * `AWSSimpleDB.framework`
    * `AWSSNS.framework`
    * `AWSSQS.framework`

4. Under the **Buid Phases** tab in your **Target**, click the **+** button on the top left and then select **New Run Script Phase**. Then setup the build phase as follows. Make sure this phase is below the `Embed Frameworks` phase.::

        Shell /bin/sh
        
        bash "${BUILT_PRODUCTS_DIR}/${FRAMEWORKS_FOLDER_PATH}/AWSCore.framework/strip-frameworks.sh"
        
        Show environment variables in build log: Checked
        Run script only when installing: Not checked
        
        Input Files: Empty
        Output Files: Empty

Update the SDK to a Newer Version
#################################

When a new version of the SDK is released, you can pick up the changes as described below.

CocoaPods
=========

Run the following command in your project directory. CocoaPods automatically picks up the new changes.

:command:`$ pod update`

.. note:: If your pod is having an issue, you can delete :file:`Podfile.lock` and :file:`Pods/` and then run :command:`pod install` to cleanly install the SDK.

Carthage
=========

Run the following command in your project directory. Carthage automatically picks up the new changes.

:command:`$ carthage update`

Frameworks
==========

#. In Xcode select the following frameworks in **Project Navigator** and hit **delete** on your keyboard. Then select **Move to Trash**:

    * `AWSCore.framework`
    * `AWSAutoScaling.framework`
    * `AWSCloudWatch.framework`
    * `AWSCognito.framework`
    * `AWSCognitoIdentityProvider.framework`
    * `AWSDynamoDB.framework`
    * `AWSEC2.framework`
    * `AWSElasticLoadBalancing.framework`
    * `AWSIoT.framework`
    * `AWSKinesis.framework`
    * `AWSLambda.framework`
    * `AWSMachineLearning.framework`
    * `AWSMobileAnalytics.framework`
    * `AWSS3.framework`
    * `AWSSES.framework`
    * `AWSSimpleDB.framework`
    * `AWSSNS.framework`
    * `AWSSQS.framework`

#. Follow the installation process above to include the new version of the SDK.

Preparing iOS 9 Apps
####################

The release of iOS 9 includes changes that might impact how your apps interact with some AWS services. If you compile your apps with Apple’s iOS 9 SDK
(or Xcode 7), there are additional steps you must complete for your app to successfully connect with any AWS service you need to call. For more information,
see `Preparing Your Apps for iOS 9 <http://docs.aws.amazon.com/mobile/sdkforios/developerguide/ats.html>`_.

Getting Started with Swift
##########################

#. Import the AWSCore header in the application delegate. ::

        import AWSCore

#. Create a default service configuration by adding the following code snippet in the `application:didFinishLaunchingWithOptions:` application delegate method. ::

        let credentialsProvider = AWSCognitoCredentialsProvider(
            regionType: CognitoRegionType,
            identityPoolId: CognitoIdentityPoolId)
        let configuration = AWSServiceConfiguration(
            region: DefaultServiceRegionType,
            credentialsProvider: credentialsProvider)
        AWSServiceManager.defaultServiceManager().defaultServiceConfiguration = configuration

#. In Swift file you want to use the SDK, import the appropriate headers for the services you are using. The header file import convention is `import AWSServiceName`, as in the following examples::

        import AWSS3
        import AWSDynamoDB
        import AWSSQS
        import AWSSNS
        import AWSCognito
        
#. Make a call to the AWS services. ::

        let dynamoDB = AWSDynamoDB.defaultDynamoDB()
        let listTableInput = AWSDynamoDBListTablesInput()
        dynamoDB.listTables(listTableInput).continueWithBlock{ (task: AWSTask?) -> AnyObject? in
            if let error = task.error {
                print("Error occurred: \(error)")
                return nil
            }

            let listTablesOutput = task.result as AWSDynamoDBListTablesOutput

            for tableName in listTablesOutput.tableNames {
                print("\(tableName)")
            }

            return nil
        }
        
.. note:: Most of the service client classes have a singleton method to get a default client. The naming convention is `+ defaultSERVICENAME` (e.g. `+ defaultDynamoDB` in the above code snippet). This singleton method creates a service client with `defaultServiceConfiguration`, which you set up in step 5, and maintains a strong reference to the client.

Getting Started with Objective-C
################################

#. Import the AWSCore header in the application delegate::

       #import <AWSCore/AWSCore.h>

#. Create a default service configuration by adding the following code snippet in the ``application:didFinishLaunchingWithOptions:`` application delegate method. ::

	AWSCognitoCredentialsProvider *credentialsProvider = [[AWSCognitoCredentialsProvider alloc] initWithRegionType:AWSRegionUSEast1
		identityPoolId:CognitoPoolID];

	AWSServiceConfiguration *configuration = [[AWSServiceConfiguration alloc] initWithRegion:AWSRegionUSEast1
		credentialsProvider:credentialsProvider];

	AWSServiceManager.defaultServiceManager.defaultServiceConfiguration = configuration;

#. Import service headers where you want to use the services. The header file import convention for frameworks is ``#import <FRAMEWORKNAME/SERVICENAME.h>``, as in the following examples::

   #import <AWSCore/AWSCore.h>
   #import <AWSS3/AWSS3.h>
   #import <AWSDynamoDB/AWSDynamoDB.h>
   #import <AWSSQS/AWSSQS.h>
   #import <AWSSNS/AWSSNS.h>
   #import <AWSCognito/AWSCognito.h>


#. Make a call to the AWS services::

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

   .. note:: Most of the service client classes have a singleton method to get a default client. The naming convention is ``+ defaultSERVICENAME`` (e.g. ``+ defaultS3TransferManager`` in the above code snippet). This singleton method creates a service client with ``defaultServiceConfiguration``, which you set up in step 5, and maintains a strong reference to the client.

Logging
#######

Changing log levels during development may make debugging easier. You can change the log level by importing AWSCore.h and calling:

**Swift** ::

    AWSLogger.defaultLogger().logLevel = .Verbose

The following logging level options are available:

- ``.None``
- ``.Error``
- ``.Warn``
- ``.Info``
- ``.Debug`` (This is the default.)
- ``.Verbose``

**Objective-C** ::

    [AWSLogger defaultLogger].logLevel = AWSLogLevelVerbose;

The following logging level options are available:

- ``AWSLogLevelNone``
- ``AWSLogLevelError``
- ``AWSLogLevelWarn``
- ``AWSLogLevelInfo``
- ``AWSLogLevelDebug`` (This is the default.)
- ``AWSLogLevelVerbose``

We recommend setting the log level to `None` before publishing to the Apple App Store.

Get AWS Credentials with Amazon Cognito or AWS Identity and Access Management
=============================================================================

We recommend using Amazon Cognito as your credential provider to access AWS services from your
mobile app. Cognito provides a secure mechanism to access AWS services without having to embed
credentials in your app. To learn more, see :doc:`cognito-auth`.

Alternatively, you can use `AWS Identity and Access
Management <http://aws.amazon.com/iam/>`_ (IAM). If you choose IAM, ensure that your role's policy is minimally scoped
so that it can only perform the desired actions for the service being used.

Sample Apps
###########

The AWS SDK for iOS includes sample apps that demonstrate common use cases.

**Cognito Your User Pools Sample** (`Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/CognitoYourUserPools-Sample/Objective-C/>`__)

This sample demonstrates how sign up and sign in a user to display an authenticated portion of your app.

**Cognito Sync Sample** (`Swift <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/CognitoSync-Sample/Swift/>`__, `Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/CognitoSync-Sample/Objective-C/>`__)

This sample demonstrates how to securely manage and sync your mobile app data and create unique identities via login providers including Facebook, Google, and Login with Amazon.

AWS Services Demonstrated:

- `Amazon Cognito Sync <http://aws.amazon.com/cognito/>`_
- `Amazon Cognito Identity <http://aws.amazon.com/cognito/>`_

**DynamoDB Object Mapper Sample** (`Swift <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/DynamoDBObjectMapper-Sample/Swift>`__, `Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/DynamoDBObjectMapper-Sample/Objective-C/>`__)

This sample demonstrates how to insert / update / delete / query items using DynamoDB Object Mapper.

AWS Services Demonstrated:

- `Amazon DynamoDB <http://aws.amazon.com/cognito/>`_
- `Amazon Cognito Identity <http://aws.amazon.com/cognito/>`_

**S3 Transfer Utility Sample** (`Swift <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/S3TransferUtility-Sample/Swift/>`__, `Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/S3TransferUtility-Sample/Objective-C/>`__)

This sample demonstrates how to use the Amazon S3 Transfer Utility to download / upload files.

AWS Services Demonstrated:

- `Amazon S3 <http://aws.amazon.com/s3/>`_
- `Amazon Cognito Identity <http://aws.amazon.com/cognito/>`_

**SNS Mobile Push and Mobile Analytics Sample** (`Swift <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/SNS-MobileAnalytics-Sample/Swift/>`__, `Objective-C <https://github.com/awslabs/aws-sdk-ios-samples/tree/master/SNS-MobileAnalytics-Sample/Objective-C/>`_)

This sample demonstrates how to set up Amazon SNS Mobile Push and record events using Amazon Mobile Analytics.

AWS Services Demonstrated:

- `Amazon SNS Mobile Push <http://aws.amazon.com/sns/>`_
- `Amazon Mobile Analytics <http://aws.amazon.com/mobileanalytics/>`_
- `Amazon Cognito Identity <http://aws.amazon.com/cognito/>`_

Install the Reference Documentation in Xcode
############################################

The AWS SDK for iOS includes documentation in the DocSets format that you can view within
Xcode. The easiest way to install the documentation is to use the Mac OS X
terminal.

To install the DocSet for Xcode
===============================

Open the Mac OS X terminal and go to the directory containing the expanded
archive. For example:

::

    $ cd ~/Downloads/aws-ios-sdk-2.2.2

.. note:: Remember to replace :command:`2.2.2` in the example above with the
   actual version number of the AWS SDK for iOS that you downloaded.

Create a directory called
:file:`~/Library/Developer/Shared/Documentation/DocSets`:

::

    $ mkdir -p ~/Library/Developer/Shared/Documentation/DocSets

Copy (or move) :file:`documentation/com.amazon.aws.ios.docset`
from the SDK installation files to the directory you created in the previous
step:

::

    $ mv documentation/com.amazon.aws.ios.docset ~/Library/Developer/Shared/Documentation/DocSets/

If Xcode was running during this procedure, restart Xcode. To browse the
documentation, go to :strong:`Help`, click :strong:`Documentation and API Reference`, and select :strong:`AWS SDK for iOS v2.0 Documentation`
(where '2.0' is the appropriate version number).
