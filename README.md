# py-lambda-local
lambdalocal is a tool to simulate running an AWS Lambda locally, for lambda functions in Python.


## Table of Contents

* [Requirements](#requirements)
* [Installation](#install)
* [About: CLI](#about-cli)
    * [Positional Arguments](#positional-arguments)
    * [Optional Arguments](#optional-arguments)
    * [CLI Examples](#cli-examples)


## Requirements
* Python => 3.8
* Poetry => 1.1.12 or another package manager that supports direct git dependencies


## Install
To install lambdalocal, we recommend adding it to your pyproject.toml in the dev-dependencies section as shown in the example below.

```toml
[tool.poetry.dev-dependencies]
lambdalocal = { git = "https://github.com/miqueiasbrs/py-lambda-local.git", branch = "master" }
```
**Obs.:** We recommend using Poetry. See https://python-poetry.org/docs/ 


## About: CLI

### Positional Arguments:
| Argument    | Description                                                 |
|-------------|-------------------------------------------------------------|
| lambda_path | Specify Lambda function file name.                          |
| event_path  | Specify event data file name.                               |

### Optional Arguments:
| Argument    | Description                                                 |
|-------------|-------------------------------------------------------------|
| --help      | Show this help message and exit                             |
| -h          | Lambda function handler name. Default is "lambda_handler"   |
| -t          | Seconds until lambda function timeout. Default is 3 seconds |
| -p          | Read the AWS profile of the file.                           |
| -r          | Sets the AWS region, defaults to us-east-1.                 |


### CLI Examples
```sh
# Simple usage
pyhton -m lambdalocal main.py test-event.json

# Input all arguments
pyhton -m lambdalocal main.py test-event.json -p my_profile -r my_region -h lambda_handler -t 30
```