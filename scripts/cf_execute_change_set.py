import sys
import time
import boto3
from yaml import dump, Dumper


def _wait(stack_name, change_set_name, retry=3, wait_time=15):
    cf = boto3.client('cloudformation', region_name='us-east-2')
    print("...waiting for change set create complete...")
    for x in range(retry):
        response = cf.describe_change_set(ChangeSetName=change_set_name, StackName=stack_name)
        if response['Status'] != 'CREATE_COMPLETE':
            time.sleep(wait_time)
        else:
            print(dump(response, Dumper=Dumper))
            return
    print(dump(response, Dumper=Dumper))    
    raise ValueError()


def main(stack_name, change_set_name):
    _wait(stack_name, change_set_name)

    cf = boto3.client('cloudformation', region_name='us-east-2')
    response = cf.execute_change_set(
        ChangeSetName=change_set_name,
        StackName=stack_name,
    )
    print(dump(response, Dumper=Dumper))
    waiter = cf.get_waiter('stack_update_complete')
    print("...waiting for stack to update...")
    waiter.wait(StackName=stack_name)


if __name__ == "__main__":
    main(*sys.argv[1:])
