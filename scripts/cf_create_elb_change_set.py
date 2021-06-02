import sys

import boto3

from yaml import dump, Dumper


def get_certificate_arn() -> str:
    acm = boto3.client('acm', region_name='us-east-2')  # pylint: disable=C0103
    response = acm.list_certificates(CertificateStatuses=['ISSUED'])
    return response["CertificateSummaryList"][0]["CertificateArn"]


def get_subnets(vpc_id) -> list:
    ec2 = boto3.resource('ec2', region_name='us-east-2')
    vpc = ec2.Vpc(vpc_id)
    return [sub.id for sub in vpc.subnets.all()]


def get_security_group(vpc_id, sg_name) -> str:
    ec2 = boto3.resource('ec2', region_name='us-east-2')
    vpc = ec2.Vpc(vpc_id)
    return [sg.id for sg in vpc.security_groups.filter(GroupNames=[sg_name,])][0]


def _parse_template(template):
    cf = boto3.client('cloudformation', region_name='us-east-2')
    with open(template) as template_fileobj:
        template_data = template_fileobj.read()
    cf.validate_template(TemplateBody=template_data)
    return template_data


def main(stack_name, stack_template, vpc_id, sg_name):
    cert_arn = get_certificate_arn()
    subnets = get_subnets(vpc_id)
    sg = get_security_group(vpc_id, sg_name)
    template = _parse_template(stack_template)

    cf = boto3.client('cloudformation', region_name='us-east-2')
    response = cf.create_change_set(
        ChangeSetName='update-with-elb',
        StackName=stack_name,
        TemplateBody=template,
        Parameters=[
            {
                'ParameterKey': 'VPC',
                'ParameterValue': vpc_id,
            },
            {
                'ParameterKey': 'SubnetA',
                'ParameterValue': subnets[0],
            },
            {
                'ParameterKey': 'SubnetB',
                'ParameterValue': subnets[1],
            },
            {
                'ParameterKey': 'SubnetC',
                'ParameterValue': subnets[2],
            },
            {
                'ParameterKey': 'SecurityGroup',
                'ParameterValue': sg,
            },
            {
                'ParameterKey': 'CertificateArn',
                'ParameterValue': cert_arn,
            },
        ],
    )
    print(dump(response, Dumper=Dumper))

if __name__ == "__main__":
    main(*sys.argv[1:])
