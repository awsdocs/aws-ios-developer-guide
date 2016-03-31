.. Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

.. highlight:: objc

Preparing Your Apps for iOS 9
#############################

The release of iOS 9 includes changes that might impact how your apps interact with some AWS services. If you compile your apps
with Apple's iOS 9 SDK (or Xcode 7), Apple's `App Transport Security (ATS) <https://developer.apple.com/library/prerelease/ios/technotes/App-Transport-Security-Technote/>`_
feature may affect the ability of apps to connect to certain AWS service endpoints. In order to ensure affected apps continue to
successfully connect to AWS endpoints, you'll need to configure them to interact properly with Apple's ATS by adding these
properties to your ``Info.plist`` file::

    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSExceptionDomains</key>
        <dict>
            <key>amazonaws.com</key>
            <dict>
                  <key>NSThirdPartyExceptionMinimumTLSVersion</key>
                  <string>TLSv1.0</string>
                  <key>NSThirdPartyExceptionRequiresForwardSecrecy</key>
                  <false/>
                  <key>NSIncludesSubdomains</key>
                  <true/>
            </dict>
            <key>amazonaws.com.cn</key>
            <dict>
                  <key>NSThirdPartyExceptionMinimumTLSVersion</key>
                  <string>TLSv1.0</string>
                  <key>NSThirdPartyExceptionRequiresForwardSecrecy</key>
                  <false/>
                  <key>NSIncludesSubdomains</key>
                  <true/>
            </dict>
        </dict>
    </dict>

If you are not planning to recompile your apps with Apple's iOS 9 SDK (or Xcode 7) to run on iOS 9 devices,
you do not need to make any configuration changes.

Determining if Your App is Affected
===================================

If your app stops working after upgrading to Xcode 7 and iOS 9, follow these steps to determine if it affected by ATS.

1. Turn on verbose logging of the AWS Mobile SDK for iOS by calling the following line in the ``- application:didFinishLaunchingWithOptions:`` application delegate.

    **Swift**::

        @UIApplicationMain
        class AppDelegate: UIResponder, UIApplicationDelegate {

            var window: UIWindow?
            func application(application: UIApplication, didFinishLaunchingWithOptions
            launchOptions: [NSObject : AnyObject]?) -> Bool {
                ...
                AWSLogger.defaultLogger().logLevel = .Verbose
                ...

                return true
            }
        }

    **Objective-C**::

        #import <AWSCore/AWSCore.h>

        @implementation AppDelegate

        - (BOOL)application:(UIApplication *)application
        didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
            ...
            [AWSLogger defaultLogger].logLevel = AWSLogLevelVerbose;
            ...

            return YES;
        }

        @end

2. Run your app and make a request to an AWS service.

3. Search your log output for "SSL". If you find the "An SSL error has occurred and a secure connection to the server cannot be made" message, your app is affected by the ATS changes::

    2015-10-06 11:39:13.402 DynamoDBSampleSwift[14467:303540] CFNetwork SSLHandshake failed (-9824)
    2015-10-06 11:39:13.403 DynamoDBSampleSwift[14467:303540] NSURLSession/NSURLConnection HTTP load failed (kCFStreamErrorDomainSSL, -9824)
    2015-10-06 11:39:13.569 DynamoDBSampleSwift[14467:303540] CFNetwork SSLHandshake failed (-9824)
    2015-10-06 11:39:13.569 DynamoDBSampleSwift[14467:303540] NSURLSession/NSURLConnection HTTP load failed (kCFStreamErrorDomainSSL, -9824)
    Error: Error Domain=NSURLErrorDomain Code=-1200 "An SSL error has occurred and a secure connection to the server cannot be made." UserInfo={_kCFStreamErrorCodeKey=-9824, NSLocalizedRecoverySuggestion=Would you like to connect to the server anyway?, NSUnderlyingError=0x7fca343012f0 {Error Domain=kCFErrorDomainCFNetwork Code=-1200 "(null)" UserInfo={_kCFStreamPropertySSLClientCertificateState=0, _kCFNetworkCFStreamSSLErrorOriginalValue=-9824, _kCFStreamErrorDomainKey=3, _kCFStreamErrorCodeKey=-9824}}, NSLocalizedDescription=An SSL error has occurred and a secure connection to the server cannot be made., NSErrorFailingURLKey=https://dynamodb.us-east-1.amazonaws.com/, NSErrorFailingURLStringKey=https://dynamodb.us-east-1.amazonaws.com/, _kCFStreamErrorDomainKey=3}

   If you cannot find the SSL handshake error message, it is possible that another problem caused your app to stop working. Some internal
   behaviors change with major operating system updates, and it is common for previously unseen issues to surface.
   You can post the versions of Xcode, iOS, and the AWS Mobile SDK, code snippets, and steps to reproduce the issue on
   `our forum <https://forums.aws.amazon.com/forum.jspa?forumID=88>`_ or `GitHub <https://github.com/aws/aws-sdk-ios/issues>`_ so that we can assist you in identifying the issue.

Resolving the Issue
===================

If you see the SSL handshake error, follow these steps to resolve the issue.

1. Locate your ``Info.plist`` and from the context menu select **Open As** > **Source Code**.

.. image:: images/ss1.png

2. Copy and paste the ATS exception to be a direct child of the top level ``<dict>`` tag.

.. image:: images/ss2.png

After following these steps, your app should be able to access AWS endpoints while running on iOS 9.
