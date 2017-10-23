.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Install AWS Mobile SDK for iOS
==============================

The AWS Mobile SDK is installed using CocoaPods. If you don't have CocoaPods installed, see `Install CocoaPods`_.

Create a new project in Xcode, and in your project's directory, create file called podfile. Add the following text to the podfile you just created:
::

	source 'https://github.com/CocoaPods/Specs.git'
	pod 'AWSCore'
	pod 'AWSAutoScaling'
	pod 'AWSCloudWatch'
	pod 'AWSDynamoDB'
	pod 'AWSEC2'
	pod 'AWSElasticLoadBalancing'
	pod 'AWSKinesis'
	pod 'AWSLambda'
	pod 'AWSMachineLearning'
	pod 'AWSMobileAnalytics'
	pod 'AWSS3'
	pod 'AWSSES'
	pod 'AWSSimpleDB'
	pod 'AWSSNS'
	pod 'AWSSQS'
	pod 'AWSCognito'

In a terminal window, navigate to your project directory and run the following command:
::

	pod install

This will install the AWS Mobile SDK and any needed dependencies. Next, reopen your project using the newly generated .xcworkspace file

Your project now has the AWS Mobile SDK for iOS installed.

For more detailed information about installing the AWS Mobile SDK for iOS, see :doc:`setup-aws-sdk-for-ios`

.. _Install CocoaPods: http://cocoapods.org
