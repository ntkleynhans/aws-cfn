from datetime import datetime
import sys

import boto3
import botocore

from yaml import load, dump
from yaml import Loader, Dumper


def get_certificate_arn() -> str:
    acm = boto3.client('acm', region_name='us-east-2')  # pylint: disable=C0103
    response = acm.list_certificates(CertificateStatuses=['ISSUED'])
    return response["CertificateSummaryList"][0]["CertificateArn"]

def get_subnets(vpc_id) -> list:
    ec2 = boto3.resource('ec2', region_name='us-east-2')
    vpc = ec2.Vpc(vpc_id)
    return [sub.id for sub in vpc.subnets.all()]


def main(vpc_id):
    cert_arn = get_certificate_arn()
    subnets = get_subnets(vpc_id)
    print(cert_arn)
    print(subnets)


if __name__ == "__main__":
    main(*sys.argv[1:])
