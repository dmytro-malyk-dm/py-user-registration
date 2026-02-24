#!/bin/bash
awslocal sqs create-queue --queue-name pdf-queue
awslocal s3 mb s3://pdf-bucket