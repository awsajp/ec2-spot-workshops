jp:~/environment/ec2-spot-workshops/workshops/ecr-image-scanning/webapp (master) $ aws ecr describe-image-scan-findings \
>     --repository-name ecr-demo-scan/web  \
>     --image-id imageTag=$GIT_SHA
{
    "imageScanFindings": {
        "findings": [],
        "imageScanCompletedAt": "2020-07-27T07:32:44+00:00",
        "vulnerabilitySourceUpdatedAt": "2020-07-02T03:32:02+00:00",
        "findingSeverityCounts": {}
    },
    "registryId": "000474600478",
    "repositoryName": "ecr-demo-scan/web",
    "imageId": {
        "imageDigest": "sha256:34a54737fce6863c0e5997f794550d4aae68538c00c350834e969ec4f2a5adb2",
        "imageTag": "cf06d1a"
    },
    "imageScanStatus": {
        "status": "COMPLETE",
        "description": "The scan was completed successfully."
    }
}

