class OperationNotAllowedError(Exception):
    def __init__(self, operation:str, on:str):
        self.operation = operation;
        self.on = on;
    def __str__(self):
        return "OperationNotAllowedError: Operation '{}' is not allowed on '{}'".format(
            self.operation, self.on);
#end class OperationNotAllowedError

class NetworkError(Exception):
    def __init__(self):
        pass;
    def __str__(self):
        return "NetworkError: (Base NetworkError)";
#end class NetworkError

class HTTPError(NetworkError):
    def __init__(self, status, url, exceptedStatus=200):
        self.status = status;
        self.url = url;
        self.exceptedStatus = exceptedStatus;
    def __str__(self):
        return "HTTPError: Response status is '{}', excepted '{}' when requesting '{}'".format(
            self.status, self.exceptedStatus, self.url);
#end class HTTPError

class ResponseCodeError(NetworkError):
    def __init__(self, code, url, exceptedCode=0):
        self.code = code;
        self.url = url;
        self.exceptedCode = exceptedCode;
    def __str__(self):
        return "ResponseCodeError: Response code is '{}', excepted '{}' when requesting '{}'".format(
            self.code, self.exceptedCode, self.url);
#end class ResponseCodeError

class ExternalCallError(Exception):
    def __init__(self, cmd:str, exitcode:str, stdout:str = "", stderr:str = ""):
        self.cmd = cmd;
        self.exitcode = exitcode;
        self.stdout = stdout;
        self.stderr = stderr;
    def __str__(self):
        return "ExternalCallError: Returns ({}) in command '{}'. \nSTDOUT: {}\nSTDERR: {}".format(
            self.exitcode, self.cmd, self.stdout, self.stderr);
#end class ExternalCallError
