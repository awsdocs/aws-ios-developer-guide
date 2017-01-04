.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

#######################################
Sync User Data with Amazon Cognito Sync
#######################################

.. highlight:: objc

Authenticate Users with Amazon Cognito Identity
----------------------------------------

Amazon Cognito Identity provides secure access to AWS services. Identities are managed by an identity pool. Roles specify resources an identity can access and are associated with an identity pool. To create an identity pool for your application:

#. Log into the `Cognito Console`_ and click the :guilabel:`New Identity Pool` button
#. Give your Identity Pool a unique name and enable access to unauthenticated identities
#. Click the :guilabel:`Create Pool` button and then the :guilabel:`Update Roles` to create your identity pool and associated roles

For more information on Cognito Identity, see :doc:`cognito-auth`

.. note::

	The auto-generated Roles include the permissions needed to access Cognito Sync, so no further configuration is required.

The next page displays code that creates a credential provider that provides a Cognito Identity for your app to use. Copy the code from Steps 1 & 2 into your AppDelegate.m file as shown below:

Add the following import statements:
::

	#import <AWSCore/AWSCore.h>
	#import <AWSCognito/AWSCognito.h>

Add the following code to application:didFinishLaunchingWithOptions method:
::

	AWSCognitoCredentialsProvider *credentialsProvider = [[AWSCognitoCredentialsProvider alloc] initWithRegionType:AWSRegionUSEast1
		identityPoolId:@"<your-identity-pool-arn>"];

	AWSServiceConfiguration *configuration = [[AWSServiceConfiguration alloc] initWithRegion:AWSRegionUSEast1
		credentialsProvider:credentialsProvider];

	AWSServiceManager.defaultServiceManager.defaultServiceConfiguration = configuration;

.. note::
	If you have an existing credential provider, you do not need to create a new one.

For more information on Cognito Identity, see :doc:`cognito-auth`

Syncing User Data
-----------------

To sync unauthenticated user data:

#. Create a dataset and add user data.
#. Synchronize the dataset with the cloud.

Create a Dataset and Add User Data
----------------------------------

Create an instance of :code:`AWSCognitoDataset`. User data is added in the form of key/value pairs. Dataset objects are created with the :code:`AWSCognito` class which functions as a Cognito client object. Use the defaultCognito method to get a reference to the default singleton instance of AWSCognito. The openOrCreateDataset method is used to create a new dataset or open an existing instance of a dataset stored locally on the device:
::

	AWSCognitoDataset *dataset = [[AWSCognito defaultCognito] openOrCreateDataset:datasetName];

User data is added to an AWSCognitoDataset instance using the setString\:forKey or setValue\:forKey methods. The following code snippet shows how to add some user data to a dataset:
::

	[dataset setString:@"John Doe" forKey:@"Username"];
	[dataset setString:@"10000" forKey:@"HighScore"];

Synchronize Dataset with the Cloud
----------------------------------

To sync the dataset with the cloud, call the synchronize method on the dataset object:
::

	[dataset synchronize];

All data written to datasets will be stored locally until the dataset is synced. The code in this section assumes you are using an unauthenticated Cognito identity, so when the user data is synced with the cloud it will be stored per device. The device has a device ID associated with it, when the user data is synced to the cloud, it will be associated with that device ID.

To sync user data across devices (based on an authenticated Cognito Identity) see :doc:`cognito-sync`.

Related Documentation
---------------------
:doc:`cognito-auth`

`Developer Authenticated Identities`_


.. _Cognito Console: https://console.aws.amazon.com/cognito
.. _Developer Authenticated Identities: http://docs.aws.amazon.com/mobile/sdkforios/developerguide/cognito-auth.html#using-developer-authenticated-identities

