### Unicorn Gym

Prerequisites

1. Create a an S3 bucket and upload the zip files
2. Use the S3 bucket name during the CFN

The CFN does the following
1. Dynamo DB Table
2. different S3 bucket to upload media files
2. setup S3 object event to call Lambda
3. Lambda schduled a transcribe Job and update status in DynamoDB
4. CWT event to trigger lambda when Transcribe job completes
5. Lambda updated the status and transcribe o/p in DynamoDB



