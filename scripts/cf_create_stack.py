from datetime import datetime
import sys
from yaml import dump
from yaml import Dumper

import boto3
import botocore


cf = boto3.client('cloudformation', region_name='us-east-2')  # pylint: disable=C0103


def main(stack_name, template):
    'Create stack'

    template_data = _parse_template(template)

    params = {
        'StackName': stack_name,
        'TemplateBody': template_data,
    }

    try:
        print('Creating {}'.format(stack_name))
        stack_result = cf.create_stack(**params)
        waiter = cf.get_waiter('stack_create_complete')
        print("...waiting for stack to be ready...")
        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise
    else:
        print(dump(
            cf.describe_stacks(StackName=stack_result['StackId']),
            Dumper=Dumper
        ))


def _parse_template(template):
    with open(template) as template_fileobj:
        template_data = template_fileobj.read()
    cf.validate_template(TemplateBody=template_data)
    return template_data


if __name__ == '__main__':
    main(*sys.argv[1:])