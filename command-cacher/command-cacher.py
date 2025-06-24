"""
Problem:
You’re building a local cache system for expensive shell commands (e.g., git status). Write a class CommandCache that caches a command’s output for 10 seconds.


CommandCache.get("git status") should:
- run the command if it hasn't been run in the last 10 seconds
- return the cached output if it's still valid

Bonus:
Handle stderr
Allow async fetching in background


- are we doing this for every command or jsut git commands?
- always 10 secs?
- For the purposes of this question, I want to add the output as string to the cache
or should I add the output as a list of lines? maybe we want to do some processing?


git status
"
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        ../command_cacher/
"

git branch
"
* main
"


git log --oneline
"
2a51a95 (HEAD -> main, origin/main) add simple-fuzzy-search
e603aa9 add ls command output parser
7859226 initial commit
ec27c44 Initial commit
"


1. CommandCache class
2. __init__ method to initialize the cache
3. get method to fetch the command output
4. run the command if it's not in the cache or if it's expired
5. store the command output in the cache with a timestamp
6. handle stderr by capturing it and storing it in the cache




"""
import subprocess
import time


class CommandCache:
    def __init__(self):
        self.cache = {}

    # Initialize an empty cache dictionary
    def get(self, command: str) -> str:
        current_time = time.time()
        if command in self.cache:
            cached_output, timestamp = self.cache[command]
            if current_time - timestamp < 10:  # Check if cache is still valid
                return cached_output

        # Run the command and cache the output
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()
            if output:  # Only cache non-empty outputs
                self.cache[command] = (output, current_time)
            return output
        except subprocess.CalledProcessError as e:
            # Handle stderr
            return f"Error running command: {e.stderr.strip()}"


if __name__ == '__main__':
    cache = CommandCache()

    # Example usage
    command = "git status"
    output = cache.get(command)
    print(f"Output of '{command}':\n{output}\n")

    # Wait for 5 seconds and try again
    time.sleep(5)
    output = cache.get(command)
    print(f"Output of '{command}' after 5 seconds:\n{output}\n")

    # Wait for another 6 seconds (total 11 seconds) and try again
    time.sleep(6)
    output = cache.get(command)
    print(f"Output of '{command}' after 11 seconds:\n{output}\n")
