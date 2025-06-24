"""
In a modern terminal, we often define short aliases for common commands. For example, gco might mean git checkout, or st might mean git status.

You’re given a command string like:


"gco -b new-feature"
And an alias map like:


{
  "gco": "git checkout",
  "st": "git status",
  "gl": "git log",
}
Write a function:

def expand_aliases(command: str, alias_map: Dict[str, str]) -> str:
    ...
This function should expand any known aliases at the start of the command.

In the example above, the result would be:

"git checkout -b new-feature"
"""

map = {
    "gco": "git checkout",
    "st": "git status",
    "gl": "git log",
    "gcm": "git commit -m",
}


def expand_aliases(command: str, alias_map: dict) -> str:
    # early return if the command is empty or map is empty
    if not command or not alias_map:
        return command

    # strip leading and trailing whitespace from the command
    clean_command = command.strip()

    # split the command into words and get the first word
    words = clean_command.split()
    first_word = words[0]

    # check if the first word is in the alias map
    if first_word in alias_map:
        # concatenate the alias with the rest of the command
        alias = alias_map[first_word]

        return f"{alias} {' '.join(words[1:])}" if len(words) > 1 else alias

    else:
        # if the first word is not in the alias map, return the command as is
        return command


if __name__ == "__main__":
    tests = [
        # with alias and following characters
        {"command": "gco -b new-feature", "expected": "git checkout -b new-feature"},
        {"command": "st", "expected": "git status"},  # with alias only
        {"command": "gl --oneline", "expected": "git log --oneline"},
        {"command": "git commit -m 'initial commit'",
            "expected": "git commit -m 'initial commit'"},
        {"command": "gco", "expected": "git checkout"},
        {"command": "st -v", "expected": "git status -v"},
        {"command": "gp", "expected": "gp"},
        # alias with additional args
        {"command": "gcm -a 'msg'", "expected": "git commit -m -a 'msg'"},
    ]

    for test in tests:
        result = expand_aliases(test["command"], map)
        assert result == test["expected"], f"Expected {test['expected']} but got {result}"
    print("All tests passed!")
