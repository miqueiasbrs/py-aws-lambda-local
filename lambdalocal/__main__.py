import os
import json

from time import time
from datetime import datetime
from threading import Thread
from argparse import ArgumentParser
from json.decoder import JSONDecodeError

parser = ArgumentParser()
parser.add_argument('-l', '--lambda-path', help='Specify Lambda function file name', required=True)
parser.add_argument('-e', '--event-path', help='Specify event data file name', required=True)
parser.add_argument('-hh', '--handler', help='Lambda function handler name. Default is "handler"', default='handler')
parser.add_argument('-p', '--profile', help='Read the AWS profile of the file', default='default')
parser.add_argument('-r', '--region', help='Sets the AWS region, defaults to us-east-1', default='us-east-1')
parser.add_argument('-t', '--timeout', help='Seconds until lambda function timeout. Default is 3 seconds', default=3)
args = parser.parse_args()


def get_event():
    try:
        with open(args.event_path, 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError as e:
        raise Exception(f'[event-path] - File {args.event_path} not found!')
        
    except JSONDecodeError as e:
        raise Exception(f'[event-path] - Invalid JSON on file {args.event_path} - {str(e)}')


def load_module():
    try:
        module = __import__(args.lambda_path.replace('.py', ''))
        return getattr(module, args.handler)
    except ModuleNotFoundError as e:
        raise Exception(f'Module not found {args.lambda_path}')
    except Exception as e:
        raise Exception(f'Handler not found {args.handler}')


def timeout(timeout, request_id):
    def decorator(func):
        def wrapper(*args, **kwargs):
            res = Exception(f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z {request_id} Task timed out after {timeout}.00 seconds')
            def run():
                try:
                    res = func(*args, **kwargs)
                except Exception as e:
                    res = e
            t = Thread(target=run)
            t.daemon = True

            try:
                t.start()
                t.join(timeout)
            except Exception as e:
                print ('error starting thread')
                raise e
            ret = res
            if isinstance(ret, Exception):
                print(str(ret))
            return ret
        return wrapper
    return decorator


class ContextLambda:

    function_name:          str =  None
    function_version:       str =  None
    invoked_function_arn:   str =  None
    memory_limit_in_mb:     str =  None
    log_group_name:         str =  None

    log_stream_name:        str = None
    aws_request_id:         str = None

    identity:               dict = None

    def __init__(self) -> None:
        from uuid import uuid4

        request_id = uuid4()
        self.function_name = 'LocalLambda'
        self.function_version = '$LATEST'
        self.invoked_function_arn = 'arn:aws:lambda:us-east-1:761817249596:function:LocalLambda'
        self.memory_limit_in_mb = '128'
        self.log_group_name = '/aws/lambda/LocalLambda'

        self.aws_request_id = request_id
        self.log_stream_name = f'{datetime.now().strftime("%Y/%m/%d")}/[$LATEST]{request_id}'

        self.identity = {
            'cognito_identity_id': None,
            'cognito_identity_pool_id': None
        }


try:
    event = get_event()
    module = load_module()

    os.environ["AWS_PROFILE"] = args.profile
    os.environ["AWS_DEFAULT_REGION"] = args.region

    start_time = time()
    context = ContextLambda()
    print(f'START RequestId: {context.aws_request_id} Version: $LATEST')

    def run():
        output = module(event, context)
        print(output)
    handler = timeout(timeout=args.timeout, request_id=context.aws_request_id)(run)
    handler()

    end_time = time() * 1000 - start_time * 1000
    print(f'END RequestId: {context.aws_request_id}')
    print('REPORT RequestId: {}   Duration: {:0.2f} ms    Billed Duration: {:0.0f} ms Memory Size: --- MB Max Memory Used: --- MB'.format(context.aws_request_id, end_time, end_time))
    

except Exception as e:
    print(str(e))