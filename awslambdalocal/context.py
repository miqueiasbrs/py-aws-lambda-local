import uuid
import logging

from datetime import datetime, timedelta


class Context(object):

    def __init__(
        self, 
        timeout_in_seconds: int
    ) -> None:
        self.aws_request_id = uuid.uuid4()
        self.function_name = 'LambdaLocalMachine'
        self.function_version = "$LATEST"
        self.invoked_function_arn = "arn:aws:lambda:us-east-1:000000000000:function:LambdaLocalMachine"
        self.memory_limit_in_mb = "128"
        self.log_group_name = "/aws/lambda/LambdaLocalMachine"
        self.log_stream_name = f'{datetime.now().strftime("%Y/%m/%d")}/[$LATEST]{uuid.uuid4()}'
        self.identity = None
        self.client_context = None

        self._timeout_in_seconds = timeout_in_seconds
        self._duration = timedelta(seconds=timeout_in_seconds)
    
    def get_remaining_time_in_millis(self):
        if self._timelimit is None:
            raise Exception("Context not activated.")
        return millis_interval(datetime.now(), self._timelimit)

    def log(self, msg):
        print(msg)

    def _activate(self):
        self._timelimit = datetime.now() + self._duration
        return self


def millis_interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis


class ContextFilter(logging.Filter):
    def __init__(self, context):
        super(ContextFilter, self).__init__()
        self.context = context

    def filter(self, record):
        record.aws_request_id = self.context.aws_request_id
        return True
