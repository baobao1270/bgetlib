import os
import sys

configuration = {
    "clear": {
        "cmd": [
            "rd /s /q build dist bgetlib.egg-info htmlcov test\\temp doc\\_build",
            "del /s /q /f .coverage"
        ],
        "require": [],
        "fail_ok": True
    },
    "makedoc": {
        "cmd": [
            "cd doc && make html",
            "cd .."
        ],
        "require": ["clear"],
    },
    "test": {
        "cmd": ["python -m unittest discover -v -s test -p *.py {args}"],
        "require": ["clear"]
    },
    "cover": {
        "cmd": ["coverage run -m unittest discover -v -s test -p *.py && coverage report && coverage html"],
        "require": ["clear"]
    },
    "build": {
        "cmd": ["python setup.py sdist bdist_wheel"],
        "require": ["cover"]
    },
    "upload": {
        "cmd": ["python -m twine upload dist/*"],
        "require": ["build"]
    }
}


def run_task(name):
    task = configuration[name]
    for require in task["require"]:
        run_task(require)
    print("Running task '{}'...".format(name))
    all_cmd = [cmd.format(args=" ".join(sys.argv[2:])) for cmd in task["cmd"]]
    for cmd in all_cmd:
        print("COMMAND:", cmd)
    print("=" * 60)
    result = 0
    for cmd in all_cmd:
        result = os.system(cmd)
        if (not task.get("fail_ok")) and (result != 0):
            print("\n\n\n" + "="*60)
            print("Abort.\n")
            sys.exit(result)
    print("\n" + "=" * 60)
    print("Finished task '{}', return '{}'.\n\n\n".format(name, result))


def main():
    if len(sys.argv) < 2:
        print("Not enough args.")
        sys.exit(-1)

    name = sys.argv[1]
    if configuration.get(name) is None:
        print("Task '{}' not found.".format(name))
        sys.exit(-2)
    run_task(name)


if __name__ == "__main__":
    main()
