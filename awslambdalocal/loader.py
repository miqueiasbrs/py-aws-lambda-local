import os
import sys
import uuid
import json
import timeit
import logging
import traceback
import multiprocessing

from importlib import reload

from awslambdalocal.context import Context, ContextFilter
from awslambdalocal.timeout import TimeoutException, time_limit


class FunctionLoader:
    def __init__(
        self,
        source: str,
        timeout: int,
        function_name: str
    ) -> None:
        self.timeout = timeout

        file_path = os.path.abspath(source)
        file_directory = os.path.dirname(file_path)
        sys.path.append(file_directory)

        mod_name = 'request-' + str(uuid.uuid4)
        if sys.version_info.major == 2:
            import imp
            mod = imp.load_source(mod_name, source)
        elif sys.version_info.major == 3 and sys.version_info.minor >= 5:
            import importlib
            spec = importlib.util.spec_from_file_location(mod_name, source)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = mod
            spec.loader.exec_module(mod)
        else:
            raise Exception("unsupported python version")

        self.__func = getattr(mod, function_name)

    def load(self, event: dict):
        context = Context(self.timeout)

        logger = logging.getLogger()
        logger.info("Event: {}".format(event))
        logger.info("START RequestId: {} Version: {}".format(
            context.aws_request_id, context.function_version))

        queue = multiprocessing.Queue()
        p = multiprocessing.Process(
            target=self.__execute_in_process,
            args=(queue, self.__func, event, context)
        )
        p.start()
        (result, err_type, duration) = queue.get()
        p.join()

        logger.info("END RequestId: {}".format(context.aws_request_id))
        duration = "{0:.2f} ms".format(duration)
        logger.info("REPORT RequestId: {}\tDuration: {}".format(
            context.aws_request_id, duration))
        if type(result) is TimeoutException:
            logger.error("RESULT:\n{}".format(result))
        else:
            logger.info("RESULT:\n{}".format(result))

        return (result, err_type)

    def __execute_in_process(self, queue, loader, event, context):
        start_time = timeit.default_timer()
        result, err_type = self.__execute(loader, event, context)
        end_time = timeit.default_timer()
        duration = (end_time - start_time) * 1000
        queue.put((result, err_type, duration))

    def __execute(self, func, event, context):
        err_type = None

        logger = logging.getLogger()
        log_filter = ContextFilter(context)
        logger.addFilter(log_filter)

        try:
            with time_limit(context._timeout_in_seconds):
                result = func(event, context._activate())
        except TimeoutException as err:
            result = err
            err_type = 1
        except:
            err = sys.exc_info()
            result = json.dumps({
                "errorMessage": str(err[1]),
                "stackTrace": traceback.format_tb(err[2]),
                "errorType": err[0].__name__
            }, indent=4, separators=(',', ': '))
            err_type = 0

        return result, err_type
