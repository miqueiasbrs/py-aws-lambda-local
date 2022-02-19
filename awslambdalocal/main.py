import os
import sys
import logging

from dotenv import load_dotenv

from awslambdalocal.loader import FunctionLoader


logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')


def run(args):
    set_environment_variables(args.profile, args.region)

    if args.watch:
        start_lambda_watch(args)
    else:
        start_lambda(args)


def start_lambda(args):
    from awslambdalocal.event import read_event
    e = read_event(args.event)
    (result, err_type) = FunctionLoader(
        source=args.file,
        function_name=args.handler,
        timeout=args.timeout
    ).load(e)

    if err_type is not None:
        sys.exit(1)


def start_lambda_watch(args):
    from awslambdalocal import server

    loader = FunctionLoader(
        source=args.file,
        function_name=args.handler,
        timeout=args.timeout
    )
    server.start(loader, args.watch)


def set_environment_variables(profile, region):
    os.environ["AWS_PROFILE"] = profile
    os.environ["AWS_DEFAULT_REGION"] = region
    load_dotenv()
