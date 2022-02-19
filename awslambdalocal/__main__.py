from argparse import ArgumentParser

from awslambdalocal import main

def parse_args():
    parser = ArgumentParser(
        description="Run AWS Lambda function  written in Python on local machine.",
        conflict_handler='resolve')
    parser.add_argument("file",
                        metavar="FILE", 
                        type=str, 
                        help="lambda function file name")
    parser.add_argument("-e", "--event", 
                        metavar="EVENT", 
                        type=str, 
                        help="event data file name")
    parser.add_argument("-h", "--handler",
                        metavar="HANDLER",
                        type=str,
                        default="handler",
                        help="lambda function handler name, default: \"handler\"")
    parser.add_argument("-t", "--timeout",
                        metavar="TIMEOUT",
                        type=int,
                        default=3,
                        help="seconds until lambda function timeout, default: 3")
    parser.add_argument('-p', '--profile',
                        type=str,
                        help='Read the AWS profile of the file',
                        default='default')
    parser.add_argument('-r', '--region',
                        type=str,
                        help='Sets the AWS region, defaults to us-east-1',
                        default='us-east-1')
    parser.add_argument('-w', '--watch',
                        type=int,
                        help='Starts lambda-local in watch mode listening to the specified port [1-65535].')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main.run(args)