.. Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

.. highlight:: objc

Track App Usage Data with Amazon Mobile Analytics
#################################################

Using Amazon Mobile Analytics, you can track customer behaviors, aggregate metrics, generate
data visualizations, and identify meaningful patterns. The AWS SDK for iOS provides
integration with the Amazon Mobile Analytics service. For information about AWS service region availability
or Mobile Analytics region availability, see `AWS Service Region Availability <http://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/>`_.

What is Amazon Mobile Analytics?
================================

Amazon Mobile Analytics lets you collect, visualize, and understand app usage for your iOS,
Android, FireOS, Windows Phone, Blackberry mobile apps as well as desktop and web apps running
on Windows, OS X, and Linux. Reports are available for metrics on active users, sessions,
retention, in-app revenue, and custom events, and can be filtered by platform and date
range. Amazon Mobile Analytics is built to scale with your business and can collect and process
billions of events from many millions of endpoints.

To learn more about Mobile Analytics, see the `Amazon Mobile Analytics User Guide <http://docs.aws.amazon.com/mobileanalytics/latest/ug/>`_

IAM Policy for Amazon Mobile Analytics
--------------------------------------

To use Amazon Mobile Analytics, AWS users must have the correct permissions. The following IAM
policy allows the user to submit events to Amazon Mobile Analytics:
::

    {
    "Statement": [{
        "Effect": "Allow",
        "Action": "mobileanalytics:PutEvents",
        "Resource": "*"
    }]
    }

This policy should be assigned to roles associated with the Cognito
identity pool for your app. The policy allows clients to record events with the Mobile
Analytics service. Amazon Cognito will set this policy for you, if you let it create new
roles. Other policies are required to allow IAM users to view reports.

You can set permissions at https://console.aws.amazon.com/iam/. To learn more about IAM policies, see
`Using IAM <http://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_Introduction.html>`_.

Integrating Amazon Mobile Analytics
===================================

The sections below explain how to integrate Amazon Mobile Analytics with your app.

Create an App in the Amazon Mobile Analytics Console
----------------------------------------------------

Go to the `Amazon Mobile Analytics console <https://console.aws.amazon.com/mobileanalytics/home>`_
and create an app. Note the :code:`appId` value, as you'll need it later.

To learn more about creating new apps in the console, see `Managing Apps <http://docs.aws.amazon.com/mobileanalytics/latest/ug/managing-apps.html>`_ in the Amazon Mobile Analytics User Guide.

Integrate the SDK into Your App
-------------------------------

If you haven't already done so, `download the SDK for iOS <http://aws.amazon.com/mobile/sdk/>`_,
unzip it, and include it in your application as described at :doc:`setup`. The
instructions direct you to import the headers for the services you'll be
using:
::

	#import <AWSMobileAnalytics/AWSMobileAnalytics.h>

Initialize an :command:`AWSMobileAnalytics` client. In doing so, you'll
need to provide the :code:`appId` value that you generated in the Amazon Mobile Analytics console.
The :code:`appId` is used to group your data in the Amazon Mobile Analytics console.

::

    AWSMobileAnalyticsConfiguration *analyticsConfiguration = [[AWSMobileAnalyticsConfiguration alloc] init];
    [analyticsConfiguration setServiceConfiguration:serviceConfiguration];
    AWSMobileAnalytics *analytics = [AWSMobileAnalytics mobileAnalyticsForAppId:@"yourAppId" configuration: analyticsConfiguration];


where "yourAppId" is the :code:`appId` value from the Amazon Mobile Analytics console.

Add Monetization Events
-----------------------

The SDK for iOS provides the :code:`AWSMobileAnalyticsAppleMonetizationEventBuilder` class, which helps you
build monetization events to track purchases from Apple’s IAP Framework.

To learn more about monetization events, see:

* `AWSMobileAnalyticsAppleMonetizationEventBuilder <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSMobileAnalyticsAppleMonetizationEventBuilder.html>`_ in the API Reference Guide.
* `Creating Monetization Events <http://docs.aws.amazon.com/mobileanalytics/latest/ug/defining-a-monetization-event-sdk.html>`_ in the Amazon Mobile Analytics User Guide.

Record Custom Events
--------------------

To record custom events, we first need to get the event client from the AWSMobileAnalytics instance.

::

    id<AWSMobileAnalyticsEventClient> eventClient = analytics.eventClient;

For this example, let's say your app is a game, and you want to record an
event when a user completes a level. Create a "LevelComplete" event.

::

    id<AWSMobileAnalyticsEvent> levelEvent = [eventClient createEventWithEventType:@"LevelComplete"];

Note that custom events can't start with an underscore (_), or they'll be
filtered out.

Add attributes and metrics to the event in key-value pairs.

::

    [levelEvent addAttribute:@"Upper Dungeon" forKey:@"LevelName"];
    [levelEvent addAttribute:@"Moderately difficult" forKey:@"Difficulty"];
    [levelEvent addMetric:@1763 forKey:@"TimeToComplete"];

Record the event.

::

    [eventClient recordEvent:levelEvent];

Events are submitted automatically when the user goes into the background.
However, if you want to submit events manually, you can do so with the
:command:`submitEvents` method:

::

    [eventClient submitEvents];

If you don't call :command:`submitEvents`, events will automatically be
submitted at periodic intervals.

To learn more about custom events, see:

* `AWSMobileAnalyticsEventClient <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSMobileAnalytics.html#//api/name/eventClient>`_ in the API Reference Guide.
* `AWSMobileAnalyticsEvent <http://docs.aws.amazon.com/AWSiOSSDK/latest/Protocols/AWSMobileAnalyticsEvent.html>`_ in the API Reference Guide.
* `Creating a Custom Event <http://docs.aws.amazon.com/mobileanalytics/latest/ug/creating-a-custom-event-sdk.html>`_ in the Amazon Mobile Analytics User Guide.
