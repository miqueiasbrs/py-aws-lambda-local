# awslambdalocal
awslambdalocal is a tool to simulate running an AWS Lambda locally, for lambda functions in Python.


## Table of Contents

* [Requirements](#requirements)
* [Installation](#install)
* [About: CLI](#about-cli)
    * [Positional Arguments](#positional-arguments)
    * [Optional Arguments](#optional-arguments)
    * [CLI Examples](#cli-examples)
* [Tutorials](#tutorials)
    * [Debug Python in VSCode](#debug-python-in-vscode)


## Requirements

* Python => 3.8
* Poetry => 1.1.12 or another package manager that supports direct git dependencies


## Install

To install awslambdalocal, we recommend adding it to your pyproject.toml in the dev-dependencies section as shown in the example below.

```bash
pip install awslambdalocal
```
**Obs.:** We recommend using Poetry. See https://python-poetry.org/docs/ 


## About: CLI

### Positional Arguments:
| Argument    | Description                                                                  |
|-------------|------------------------------------------------------------------------------|
| file        | Specify Lambda function file name                                            |

### Optional Arguments:
| Argument    | Description                                                                  |
|-------------|------------------------------------------------------------------------------|
| --help      | Show this help message and exit                                              |
| -e          | Specify Event data file name. REQUIRED without param -w                      |
| -h          | Lambda function handler name. Default is "handler"                           |
| -p          | Read the AWS profile of the file.                                            |
| -r          | Sets the AWS region, defaults to us-east-1.                                  |
| -t          | Sets lambda timeout. default: 3                                              |
| -w          | Starts lambda-local in watch mode listening to the specified port [1-65535]. |


### CLI Examples
```sh
# Simple usage
pyhton -m awslambdalocal main.py test-event.json

# Input all arguments
pyhton -m awslambdalocal main.py test-event.json -p my_profile -r my_region -h lambda_handler -t 30
```


## Tutorials
---
This session contains a collection of tutorials.

### Debug Python in VSCode
To use vscode debug with awslambdalocal follow the steps below

1. Click run and debug
2. Click create a launch.json file

    ![](https://github.com/miqueiasbrs/py-aws-lambda-local/raw/master/docs/step_1.png)
3. Choose Python

    ![](https://github.com/miqueiasbrs/py-aws-lambda-local/raw/master/docs/step_2.png)
4. Choose Module

    ![](https://github.com/miqueiasbrs/py-aws-lambda-local/raw/master/docs/step_3.png)
5. Set the module name "awslambdalocal"

    ![](https://github.com/miqueiasbrs/py-aws-lambda-local/raw/master/docs/step_4.png)
6. After this process, VSCode will create a file called launch.json in the .vscode folder located at the root of the project

    ![](https://github.com/miqueiasbrs/py-aws-lambda-local/raw/master/docs/step_5.png)
6. Copy and paste the json below into the launch.json file, this file aims to call the awslambdalocal module and passes the necessary and optional parameters as arguments

    ```json
    {
        // Use o IntelliSense para saber mais sobre os atributos possíveis.
        // Focalizar para exibir as descrições dos atributos existentes.
        // Para obter mais informações, acesse: https://go.microsoft.com/fwlink/?linkid=830387
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Lambda Local", // Debug configuration name
                "type": "python", // Type of configuration. Python, Node and etc.
                "request": "launch",
                "module": "awslambdalocal", // Module that will be called,
                "cwd": "${workspaceFolder}", // Your project's root folder
                "args": [
                    "file_python.py", // Main file that will be called by lambda
                    "your_test_event.json", //Input in json format that will be received by lambda
                    // Optional args ...
                    "-h",
                    "handler",
                    "-p",
                    "your_profile",
                    "-r",
                    "us-east-1"
                ]
            }
        ]
    }
    ```