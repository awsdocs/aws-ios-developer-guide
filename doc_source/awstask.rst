.. Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0
   International License (the "License"). You may not use this file except in compliance with the
   License. A copy of the License is located at http://creativecommons.org/licenses/by-nc-sa/4.0/.

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
   either express or implied. See the License for the specific language governing permissions and
   limitations under the License.

Working with AWSTask
####################

To use the SDK for iOS effectively, you'll need to work with ``AWSTask`` objects. ``AWSTask``
is a class that makes it easier to work with asynchronous operations without blocking the UI thread.

The ``AWSTask`` class is a renamed version of BFTask from the Bolts framework. For complete
documentation on Bolts, see the `Bolts-iOS repo <https://github.com/BoltsFramework/Bolts-iOS>`_.

What is AWSTask?
----------------

An ``AWSTask`` object represents the result of an asynchronous method. Using ``AWSTask``,
you can wait for an asynchronous method to return a value, and then do something with that
value after it has returned. You can chain async requests instead of nesting them. This
helps keep logic clean and code readable.

Working with Asynchronous Methods
---------------------------------

When you're working with the AWS Mobile SDK for iOS, it's important to remember that methods that return ``AWSTask`` are asynchronous. For example, ``AWSKinesisRecorder`` defines the following methods:

   .. container:: option

        Swift
            .. code-block:: swift

                open func saveRecord(_ data: Data!, streamName: String!) -> AWSTask<AnyObject>!

                open func submitAllRecords() -> AWSTask<AnyObject>!

        Objective-C
            .. code-block:: objc

                - (AWSTask *)saveRecord:(NSData *)data
                    streamName:(NSString *)streamName;

                - (AWSTask *)submitAllRecords;

These methods are asynchronous and return immediately. This means that the following code snippet may not submit ``testData`` to the Amazon Kinesis stream.

   .. container:: option

        Swift
            .. code-block:: swift

                let kinesisRecorder = AWSKinesisRecorder.default()

                let testData = "test-data".data(using: .utf8)
                _ = kinesisRecorder?.saveRecord(testData, streamName: "test-stream-name")


        Objective-C
            .. code-block:: objc

                AWSKinesisRecorder *kinesisRecorder = [AWSKinesisRecorder defaultKinesisRecorder];

                NSData *testData = [@"test-data" dataUsingEncoding:NSUTF8StringEncoding];
                [kinesisRecorder saveRecord:testData
                    streamName:@"test-stream-name"];

                [kinesisRecorder submitAllRecords];

The problem is that ``saveRecord:streamName:`` may return before it persists the record on the disk, in which case ``submitAllRecords`` won't see the saved record on disk.

Here's the correct way to submit the data.

    .. container:: option

        Swift
            .. code-block:: swift

                let kinesisRecorder = AWSKinesisRecorder.default()

                let testData = "test-data".data(using: .utf8)
                kinesisRecorder?.saveRecord(testData, streamName: "test-stream-name").continueOnSuccessWith(block: { (task:AWSTask<AnyObject>) -> AWSTask<AnyObject>? in
                    // Guaranteed to happen after saveRecord has executed and completed successfully.
                    return kinesisRecorder?.submitAllRecords()
                }).continueWith(block: { (task:AWSTask<AnyObject>) -> Any? in
                    if let error = task.error as? NSError {
                        print("Error: \(error)")
                        return nil
                    }

                    return nil
                })

        Objective-C
            .. code-block:: objc

                AWSKinesisRecorder *kinesisRecorder = [AWSKinesisRecorder defaultKinesisRecorder];

                NSData *testData = [@"test-data" dataUsingEncoding:NSUTF8StringEncoding];
                [[[kinesisRecorder saveRecord:testData
                                   streamName:@"test-stream-name"] continueWithSuccessBlock:^id(AWSTask *task) {
                    return [kinesisRecorder submitAllRecords];
                }] continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                        NSLog(@"Error: %@", task.error);
                    }
                    return nil;
                }];

Note that the ``submitAllRecords`` call is made within the ``continueWithSuccessBlock:`` because we want to execute ``submitAllRecords`` after ``saveRecord:streamName:`` successfully finishes executing. The ``continueWithBlock:`` and ``continueWithSuccessBlock:`` won't execute until the previous asynchronous call has already finished executing. Thus, in the example above, ``submitAllRecords`` is guaranteed to see the result of ``saveRecord:streamName:``.

Handling Errors
---------------

The ``continueWithBlock:`` and ``continueWithSuccessBlock:`` work in similar ways; both ensure that the previous asynchronous method has finished executing before the subsequent block is executed. However, they have one important difference: ``continueWithSuccessBlock:`` will be skipped if an error occurred in the previous operation, but ``continueWithBlock:`` is always executed.

For example, consider the following scenarios, which refer to the code snippet above:

``saveRecord:streamName:`` succeeded and ``submitAllRecords succeeded``. In this scenario, program flow will proceed as follows:

1. ``saveRecord:streamName:`` is successfully executed.
2. ``continueWithSuccessBlock:`` is executed.
3. ``submitAllRecords`` is successfully executed.
4. ``continueWithBlock:`` is executed.
5. Because ``task.error`` is nil, it doesn't log an error.
6. Done.

``saveRecord:streamName:`` succeeded and ``submitAllRecords`` failed. In this scenario, program flow will proceed as follows:

1. ``saveRecord:streamName:`` is successfully executed.
2. ``continueWithSuccessBlock:`` is executed.
3. ``submitAllRecords`` is executed with an error.
4. ``continueWithBlock:`` is executed.
5. Because ``task.error`` is NOT nil, it logs an error from ``submitAllRecords``.
6. Done.

``saveRecord:streamName:`` failed. In this scenario, program flow will proceed as follows:

1. ``saveRecord:streamName:`` is executed with an error.
2. ``continueWithSuccessBlock:`` is skipped and will NOT be executed.
3. ``continueWithBlock:`` is executed.
4. Because ``task.error`` is NOT nil, it logs an error from ``saveRecord:streamName:``.
5. Done.

Note that the code doesn't check for ``task.error`` in ``continueWithSuccessBlock:``, and ``NSLog(@"Error: %@", task.error);`` may print out an error from either ``submitAllRecords`` or ``saveRecord:streamName:``. This is a way to consolidate error handling logic at the end of the execution chain.

If you want each block to deal with its own errors, you can rewrite the code snippet as follows:

    .. container:: option

        Swift
            .. code-block:: swift

                let kinesisRecorder = AWSKinesisRecorder.default()

                let testData = "test-data".data(using: .utf8)
                kinesisRecorder?.saveRecord(testData, streamName: "test-stream-name").continueWith(block: { (task:AWSTask<AnyObject>) -> AWSTask<AnyObject>? in
                    if let error = task.error as? NSError {
                        print("Error from 'saveRecord:streamName:': \(error)")
                        return nil
                    }
                    return kinesisRecorder?.submitAllRecords()
                }).continueWith(block: { (task:AWSTask<AnyObject>) -> Any? in
                    if let error = task.error as? NSError {
                        print("Error from 'submitAllRecords': \(error)")
                        return nil
                    }

                    return nil
                })


        Objective-C
            .. code-block:: objc

                AWSKinesisRecorder *kinesisRecorder = [AWSKinesisRecorder defaultKinesisRecorder];

                NSData *testData = [@"test-data" dataUsingEncoding:NSUTF8StringEncoding];
                [[[kinesisRecorder saveRecord:testData
                    streamName:@"test-stream-name"] continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                        NSLog(@"Error from 'saveRecord:streamName:': %@", task.error);
                        return nil;
                    }
                    return [kinesisRecorder submitAllRecords];
                }]continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                          NSLog(@"Error from 'submitAllRecords': %@", task.error);
                    }
                    return nil;
                }];


In the Objective-C snippet above, ``NSLog(@"Error from 'saveRecord:streamName:': %@", task.error);`` only logs an error from ``saveRecord:streamName:``, and ``NSLog(@"Error from 'submitAllRecords': %@", task.error);`` logs an error from ``submitAllRecords``. By using ``continueWithBlock:`` and ``continueWithSuccessBlock:`` properly, you can flexibly control the error handling flow. The same applies to the Swift snippet, except that ``print`` is used instead of ``NSLog``.

Returning AWSTask or nil
------------------------

In the above code snippet, we return ``nil`` at the end of ``continueWithBlock:``, indicating successful execution of the block. We are required to return either ``AWSTask`` or ``nil`` in every ``continueWithBlock:`` and ``continueWithSuccessBlock:``. In most cases, Xcode warns you when you forget to return one of these values, but it won't catch all such omissions. If you forget to return ``AWSTask`` or ``nil`` and Xcode doesn't catch the error, an app crash may result.

Make sure you always return ``AWSTask`` or ``nil``.

Executing Multiple Tasks
------------------------

If you want to execute a large number of operations, you have two options: executing in sequence or executing in parallel.

In Sequence
^^^^^^^^^^^

Let's say you want to submit 100 records to an Amazon Kinesis stream in sequence. You can do so as follows

    .. container:: option

        Swift
            .. code-block:: swift

                var task = AWSTask<AnyObject>(result: nil)

                for i in 0...100 {
                    task = task.continueOnSuccessWith(block: { (task:AWSTask<AnyObject>) -> AWSTask<AnyObject>? in
                        return kinesisRecorder!.saveRecord(String(format: "TestString-%02d", i).data(using: .utf8), streamName: "YourStreamName")
                    })
                }

                task.continueOnSuccessWith { (task:AWSTask<AnyObject>) -> AWSTask<AnyObject>? in
                    return kinesisRecorder?.submitAllRecords()
                }


        Objective-C
            .. code-block:: objc

                AWSKinesisRecorder *kinesisRecorder = [AWSKinesisRecorder defaultKinesisRecorder];

                AWSTask *task = [AWSTask taskWithResult:nil];
                for (int32_t i = 0; i < 100; i++) {
                    task = [task continueWithSuccessBlock:^id(AWSTask *task) {
                        NSData *testData = [[NSString stringWithFormat:@"TestString-%02d", i] dataUsingEncoding:NSUTF8StringEncoding];
                        return [kinesisRecorder saveRecord:testData
                                                streamName:@"test-stream-name"];
                    }];
                }

                [task continueWithSuccessBlock:^id(AWSTask *task) {
                    return [kinesisRecorder submitAllRecords];
                }];

In this case, the key is to concatenate a series of tasks by reassigning ``task``.

    .. container:: option

        Swift
            .. code-block:: swift

                task.continueOnSuccessWith { (task:AWSTask<AnyObject>) -> AWSTask<AnyObject>? in

        Objective-C
            .. code-block:: objc

                task = [task continueWithSuccessBlock:^id(AWSTask *task) {

In Parallel
^^^^^^^^^^^

You can execute multiple methods in parallel by using ``taskForCompletionOfAllTasks:`` as follows.

    .. container:: option

        Swift
            .. code-block:: swift

                var tasks = Array<AWSTask<AnyObject>>()
                for i in 0...100 {
                    tasks.append(kinesisRecorder!.saveRecord(String(format: "TestString-%02d", i).data(using: .utf8), streamName: "YourStreamName")!)
                }

                AWSTask(forCompletionOfAllTasks: tasks).continueOnSuccessWith(block: { (task:AWSTask<AnyObject>) -> AWSTask<AnyObject>? in
                    return kinesisRecorder?.submitAllRecords()
                }).continueWith(block: { (task:AWSTask<AnyObject>) -> Any? in
                    if let error = task.error as? NSError {
                        print("Error: \(error)")
                        return nil
                    }

                    return nil
                })

        Objective-C
            .. code-block:: objc

                AWSKinesisRecorder *kinesisRecorder = [AWSKinesisRecorder defaultKinesisRecorder];

                NSMutableArray *tasks = [NSMutableArray new];
                for (int32_t i = 0; i < 100; i++) {
                    NSData *testData = [[NSString stringWithFormat:@"TestString-%02d", i] dataUsingEncoding:NSUTF8StringEncoding];
                    [tasks addObject:[kinesisRecorder saveRecord:testData
                                                      streamName:@"test-stream-name"]];
                }

                [[AWSTask taskForCompletionOfAllTasks:tasks] continueWithSuccessBlock:^id(AWSTask *task) {
                    return [kinesisRecorder submitAllRecords];
                }];

Here we create an instance of ``NSMutableArray``, put all of our tasks in it, and then pass it to ``taskForCompletionOfAllTasks:``, which is successful only when all of the tasks are successfully executed. This approach may be faster, but it may consume more system resources. Also, some AWS services, such as Amazon DynamoDB, throttle a large number of certain requests. Choose a sequential or parallel approach based on your use case.

Executing a Block on the Main Thread
------------------------------------

By default, ``continueWithBlock:`` and ``continueWithSuccessBlock:`` are executed on a background thread. But in some cases (for example, updating a UI component based on the result of a service call), you need to execute an operation on the main thread. To execute an operation on the main thread, you can use Grand Central Dispatch or ``AWSExecutor``.

Grand Central Dispatch
^^^^^^^^^^^^^^^^^^^^^^

You can use ``dispatch_async(dispatch_get_main_queue(), ^{...});`` to execute a block on the main thread. In the following example, we create a ``UIAlertView`` on the main thread when record submission fails:

    .. container:: option

        Swift
            .. code-block:: swift

                let kinesisRecorder = AWSKinesisRecorder.default()

                let testData = "test-data".data(using: .utf8)
                kinesisRecorder?.saveRecord(testData, streamName: "test-stream-name").continueOnSuccessWith(block: { (task:AWSTask<AnyObject>) -> AWSTask<AnyObject>? in
                    return kinesisRecorder?.submitAllRecords()
                }).continueWith(block: { (task:AWSTask<AnyObject>) -> Any? in
                    if let error = task.error as? NSError {
                        DispatchQueue.main.async(execute: {
                            let alertController = UIAlertView(title: "Error!", message: error.description, delegate: nil, cancelButtonTitle: "OK")
                            alertController.show()
                        })
                        return nil
                    }

                    return nil
                })


        Objective-C
            .. code-block:: objc

                AWSKinesisRecorder *kinesisRecorder = [AWSKinesisRecorder defaultKinesisRecorder];

                NSData *testData = [@"test-data" dataUsingEncoding:NSUTF8StringEncoding];
                [[[kinesisRecorder saveRecord:testData
                                   streamName:@"test-stream-name"] continueWithSuccessBlock:^id(AWSTask *task) {
                    return [kinesisRecorder submitAllRecords];
                }] continueWithBlock:^id(AWSTask *task) {
                    if (task.error) {
                        dispatch_async(dispatch_get_main_queue(), ^{
                            UIAlertView *alertView =
                                [[UIAlertView alloc] initWithTitle:@"Error!"
                                                           message:[NSString stringWithFormat:@"Error: %@", task.error]
                                                          delegate:nil
                                                 cancelButtonTitle:@"OK"
                                                 otherButtonTitles:nil];
                            [alertView show];
                        });
                    }
                    return nil;
                }];

AWSExecutor
^^^^^^^^^^^

Another option is to use ``AWSExecutor``.

    .. container:: option

        Swift
            .. code-block:: swift

                let kinesisRecorder = AWSKinesisRecorder.default()

                let testData = "test-data".data(using: .utf8)
                kinesisRecorder?.saveRecord(testData, streamName: "test-stream-name").continueOnSuccessWith(block: { (task:AWSTask<AnyObject>) -> AWSTask<AnyObject>? in
                    return kinesisRecorder?.submitAllRecords()
                }).continueWith(executor: AWSExecutor.mainThread(), block: { (task:AWSTask<AnyObject>) -> Any? in
                    if let error = task.error as? NSError {
                        let alertController = UIAlertView(title: "Error!", message: error.description, delegate: nil, cancelButtonTitle: "OK")
                        alertController.show()
                        return nil
                    }

                    return nil
                })


        Objective-C
            .. code-block:: objc

                AWSKinesisRecorder *kinesisRecorder = [AWSKinesisRecorder defaultKinesisRecorder];

                NSData *testData = [@"test-data" dataUsingEncoding:NSUTF8StringEncoding];
                [[[kinesisRecorder saveRecord:testData streamName:@"test-stream-name"]
                          continueWithSuccessBlock:^id(AWSTask *task) {
                      return [kinesisRecorder submitAllRecords];
                }] continueWithExecutor:[AWSExecutor mainThreadExecutor] withBlock:^id(AWSTask *task) {
                    if (task.error) {
                        UIAlertView *alertView =
                            [[UIAlertView alloc] initWithTitle:@"Error!"
                                    message:[NSString stringWithFormat:@"Error: %@", task.error]
                                    delegate:nil
                                    cancelButtonTitle:@"OK"
                                    otherButtonTitles:nil];
                        [alertView show];
                    }
                    return nil;
                }];

In this case, ``withBlock:`` (Objective-C) or ``block:`` (Swift) is executed on the main thread.