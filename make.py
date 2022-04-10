import os
import sys
import yaml
import uuid
import subprocess

COLOR_ERR = "\033[31m"
COLOR_NORMAL = "\033[00m"
COLOR_HINT = "\033[01;33m"
COLOR_INPUT = "\033[36m"

makefile: dict = yaml.load(open("makefile.yaml", "rb"), Loader=yaml.Loader)

if len(sys.argv) != 2:
    print("usage: make <target>")
    sys.exit(-1)


def run_target(target_name: str):
    target_config: dict = next(filter(lambda t: t["name"] == target_name, makefile["targets"]))
    target_prerequisites = target_config.get("prerequisites", [])
    target_scripts = target_config.get("script", "echo There is no script in this target!")

    print(COLOR_HINT, end="")
    print(COLOR_HINT + f"Run target: {target_name}" + COLOR_NORMAL)
    print(COLOR_HINT + f"Target prerequisites: {target_prerequisites}" + COLOR_NORMAL)
    for prerequisite in target_prerequisites:
        run_target(prerequisite)

    script_file = str(uuid.uuid4()) + "-makefile.bat"
    print(COLOR_HINT + f"Generating scripts as {script_file}" + COLOR_NORMAL)
    with open(script_file, "w+") as f:
        f.write(target_scripts)
    subprocess.run(f"{script_file}", shell=True)
    os.remove(script_file)

    print("="*60)
    print(COLOR_HINT + f"Target {target_name} done\n" + COLOR_NORMAL)


run_target(sys.argv[1].strip())
