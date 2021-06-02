import sys

import boto3

from yaml import dump, Dumper


def main(stack_name, change_set_name):
    cf = boto3.client('cloudformation', region_name='us-east-2')
    response = cf.describe_change_set(ChangeSetName=change_set_name, StackName=stack_name)
    print(dump(response, Dumper=Dumper))

    """
    response = cf.execute_change_set(
        ChangeSetName='update-with-elb',
        StackName=stack_name,
    )
    print(dump(response, Dumper=Dumper))
    waiter = cf.get_waiter('stack_update_complete')
    print("...waiting for stack to update...")
    waiter.wait(StackName=stack_name)
    """

if __name__ == "__main__":
    main(*sys.argv[1:])
