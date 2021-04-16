from dataclasses import dataclass


class OperationNotAllowedError(Exception):
    def __init__(self, operation: str, on: str):
        self.operation = operation
        self.on = on

    def __str__(self):
        return "OperationNotAllowedError: Operation '{}' is not allowed on '{}'".format(
            self.operation, self.on)


class NetworkError(Exception):
    pass


class CallbackAbortError(Exception):
    pass


@dataclass
class HTTPError(NetworkError):
    url: str
    status: int
    excepted_status: int = 200

    def __str__(self):
        return "HTTPError: Response status is '{}', excepted '{}' when requesting '{}'".format(
            self.status, self.excepted_status, self.url)


@dataclass
class ResponseCodeError(NetworkError):
    url: str
    code: int
    excepted_status: int = 0

    def __str__(self):
        return "ResponseCodeError: Response code is '{}', excepted '{}' when requesting '{}'".format(
            self.code, self.excepted_status, self.url)


@dataclass
class ExternalCallError(Exception):
    command: str
    exit_code: int
    stdout: str = ""
    stderr: str = ""

    def __str__(self):
        return "ExternalCallError: Returns ({}) in command '{}'. \nSTDOUT: {}\nSTDERR: {}\n".format(
            self.exit_code, self.command, self.stdout, self.stderr)
