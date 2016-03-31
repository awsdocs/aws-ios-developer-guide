.. Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

.. highlight:: objc

Tracking App Usage Data with Amazon Mobile Analytics
====================================================

Add the following import statement:
::

	#import <AWSMobileAnalytics/AWSMobileAnalytics.h> 

Integrating Amazon Mobile Analytics
-----------------------------------

The sections below explain how to integrate Mobile Analytics with your app.

Create an App in the Mobile Analytics Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Go to the `Amazon Mobile Analytics console <https://console.aws.amazon.com/mobileanalytics/home>`_ 
and create an app. Note the :code:`appId` value, as you'll need it later.

.. note::

    To learn more about working in the console, see the 
    `Amazon Mobile Analytics User Guide <http://docs.aws.amazon.com/mobileanalytics/latest/ug/>`_.

Integrate the SDK into Your App
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you haven't already done so, `download the SDK for iOS <http://aws.amazon.com/mobile/sdk/>`_,
unzip it, and include it in your application as described at :doc:`setup`. The
instructions direct you to import the headers for the services you'll be
using. For this example, you need one of the following imports:
::

	#import <AWSCore/AWSCore.h> 

Initialize the Mobile Analytics Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initialize an instance of the :command:`AWSMobileAnalytics` class. In doing so, you'll
need to provide the :code:`appId` value that you generated in the Mobile Analytics console.
The :code:`appId` is used to group your data in the Mobile Analytics console.

::

    AWSMobileAnalytics *analytics = [AWSMobileAnalytics mobileAnalyticsForAppId:@"yourAppId" identityPoolId: @"cognitoId"]; 

where "yourAppId" is the :code:`appId` value from the Amazon Mobile Analytics console and
"cognitoId" is the Cognito identity pool ID.

Add Monetization Events
~~~~~~~~~~~~~~~~~~~~~~~

The SDK for iOS provides the :code:`AWSMobileAnalyticsAppleMonetizationEventBuilder` class, which helps you
build monetization events to track purchases from Apple’s IAP Framework.

To learn more about adding monetization events, see the API reference guide
for `AWSMobileAnalyticsAppleMonetizationEventBuilder <http://docs.aws.amazon.com/AWSiOSSDK/latest/Classes/AWSMobileAnalyticsAppleMonetizationEventBuilder.html>`_.

Record Custom Events
~~~~~~~~~~~~~~~~~~~~

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

.. _Cognito Console: https://console.aws.amazon.com/cognito/home
