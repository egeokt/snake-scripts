"""
📜 Prompt:
You're building a safe wrapper for running shell commands. Some commands might hang or take too long, so you want to enforce a timeout.

Write a function:


def run_with_timeout(cmd: str, timeout: int = 2) -> str:
    ...
🧪 Requirements:
Run the command using subprocess.

If it completes within timeout seconds, return its stdout as a string.

If it takes longer than timeout, terminate the command and return "Timed out".

💥 Bonus:
Return stderr output if the command fails.

Handle quoted strings and multi-word commands (e.g. echo "hello world")
"""

import subprocess


def run_with_timeout(cmd: str, timeout: int = 2) -> str:
    # early return for empty string or invalid timeout
    if not cmd or not (15 > timeout > 0):
        return "Invalid command or timeout"

    # we pass the command and timeout to the subprocess
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        output = result.stdout.strip()
        return output

    except subprocess.TimeoutExpired:
        return "Timed out"

    # todo: better error handling here. maybe think about edge cases
    except:
        return "Error. Please check your input and try again."


if __name__ == "__main__":
    tests = [{"command": "sleep 2", "timeout": 5}, {"command": "sleep 4",
                                                    "timeout": 2}, {"command": 'echo "hello world"', "timeout": 5}]

    for i, test in enumerate(tests):
        print(f"running test {i}...\n")
        print(run_with_timeout(test["command"], test["timeout"]))
