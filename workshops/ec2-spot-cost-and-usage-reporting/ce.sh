#!/bin/bash 

aws ce get-cost-and-usage \
    --time-period Start=2019-09-01,End=2020-05-01 \
    --granularity MONTHLY \
    --metrics "BlendedCost" "UnblendedCost" "UsageQuantity" \
    --group-by Type=DIMENSION,Key=SERVICE Type=TAG,Key=Environment \
    --filter file://s3.json > s3.txt

aws ce get-cost-and-usage \
    --time-period Start=2020-04-01,End=2020-05-01 \
    --granularity MONTHLY \
    --metrics "BlendedCost" "UnblendedCost" "UsageQuantity" \
    --group-by Type=DIMENSION,Key=SERVICE\
    --filter file://region.json > region.txt

aws ce get-cost-and-usage \
    --time-period Start=2020-04-01,End=2020-05-01 \
    --granularity MONTHLY \
    --metrics "BlendedCost" "UnblendedCost" "UsageQuantity" \
    --group-by Type=DIMENSION,Key=USAGE_TYPE  \
    --filter file://compute.json > ec2_elb_data_transfer.txt

exit 0
