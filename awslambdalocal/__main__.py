import json

from datetime import datetime
from argparse import ArgumentParser

parser = ArgumentParser(prog='lambdalocal', conflict_handler='resolve')
parser.add_argument('lambda_path', help='Specify Lambda function file name.')
parser.add_argument('event_path', help='Specify event data file name.')
parser.add_argument('-p', '--profile', help='Read the AWS profile of the file', default='default')
parser.add_argument('-r', '--region', help='Sets the AWS region, defaults to us-east-1', default='us-east-1')
parser.add_argument('-h', '--handler', help='Lambda function handler name. Default is "lambda_handler"', default='lambda_handler')
args = parser.parse_args()


def __load_event():
    try:
        with open(args.event_path, 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError as e:
        raise Exception(f'[event-path] - File {args.event_path} not found!')
        
    except json.decoder.JSONDecodeError as e:
        raise Exception(f'[event-path] - Invalid JSON on file {args.event_path} - {str(e)}')


def __load_module():
    try:
        module = __import__(args.lambda_path.replace('.py', ''))
        return getattr(module, args.handler)
    except ModuleNotFoundError as e:
        print(e)
        raise Exception(f'Module not found {args.lambda_path}')
    except Exception as e:
        print(e)
        raise Exception(f'Handler not found {args.handler}')


def __cxt_lambda():
    from uuid import uuid4

    request_id = uuid4()
    ctx = {
        'function_name': 'LocalLambda',
        'function_version': '$LATEST',
        'invoked_function_arn': 'arn:aws:lambda:us-east-1:761817249596:function:LocalLambda',
        'memory_limit_in_mb': '128',
        'log_group_name': '/aws/lambda/LocalLambda',
        'log_stream_name': f'{datetime.now().strftime("%Y/%m/%d")}/[$LATEST]{request_id}',
        'aws_request_id': uuid4(),
        'identity': {
            'cognito_identity_id': None,
            'cognito_identity_pool_id': None
        }
    }

    class obj:
        def __init__(self, dict1) -> None:
            self.__dict__.update(dict1)

    return obj(ctx)


# def __call_lambda(timeout, ctx):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             from time import time
#             from threading import Thread

#             def run():
#                 return func(*args, **kwargs)

#             t = Thread(target=run)
#             t.daemon = True

#             start_time = time()
#             print(f'START RequestId: {ctx.aws_request_id} Version: $LATEST')

#             t.start()
#             res = t.join(timeout)
#             print(res)

#             end_time = time() * 1000 - start_time * 1000
#             print(f'END RequestId: {ctx.aws_request_id}')
#             print('REPORT RequestId: {}   Duration: {:0.2f} ms    Billed Duration: {:0.0f} ms Memory Size: --- MB Max Memory Used: --- MB'.format(ctx.aws_request_id, end_time, end_time))

#             if t.is_alive():
#                 print(Exception(f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z {ctx.aws_request_id} Task timed out after {timeout}.00 seconds'))
#         return wrapper
#     return decorator


try:
    import os
    from time import time
    from dotenv import load_dotenv

    os.environ["AWS_PROFILE"] = args.profile
    os.environ["AWS_DEFAULT_REGION"] = args.region
    load_dotenv()

    event, module, context = __load_event(), __load_module(), __cxt_lambda()
    
    start_time = time()
    print(f'START RequestId: {context.aws_request_id} Version: $LATEST')
    print(module(event, context))
    end_time = time() * 1000 - start_time * 1000
    print(f'END RequestId: {context.aws_request_id}')
    print('REPORT RequestId: {}   Duration: {:0.2f} ms    Billed Duration: {:0.0f} ms Memory Size: --- MB Max Memory Used: --- MB'.format(context.aws_request_id, end_time, end_time))

except Exception as e:
    raise e
