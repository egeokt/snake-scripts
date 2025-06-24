"""
Command History Search (Fuzzy)
Problem:
We want to implement a fuzzy finder for command history.
Write a function that takes a history list and a search string and returns the top 3 most relevant matches.

python
def fuzzy_search(history: List[str], query: str) -> List[str]:
    ...
Example:

python
history = ["git status", "git commit -m 'init'", "npm start", "git push"]
query = "git st"
# should return something like ["git status"]
Hint: Use subsequence matching or character proximity.

["git status", "git commit -m 'init'", "npm start", "git push"]
input: "a"
# should return an empty list []

["git status", "git commit -m 'init'", "npm start", "git push"]
input: "git"
# should return ["git commit -m 'init'", "git push", "git status"]
-> do we want to sort by the character proximity or the length, or alphabetical order?

["git status", "git commit -m 'init'", "npm start", "git push"]
input: "st"
# should return ["git status", "npm start"]
-> do we want to sort by the character proximity or the length, or alphabetical order?

["git status", "git commit -m 'init'", "npm i start", "git push"]
input: "st"
# should return ["git status", "npm i start"]


1. matching function
- all the words in the query should be present in order
- we also care about when the first match occurs, so we can sort by that


2. scoring function
- we can use the index of the first match to score the results
- if there are multiple matches, we also want to consider 
- the word after the last match, so we can sort alphabetically by that

3. sort the results based on the score
and return the top 3 results.


"""


"""
Returns a dictionary with
first_match_index: the index of the first match, infinity if no match is found
word_after_last_match: the word after the last match, empty string if no match is found
"""


def match(query: str, command: str) -> dict:
    # lower the query and command words to make it case insenstivie
    query_words = query.lower().split()
    command_words = command.lower().split()

    match = float('inf')  # Start with infinity to find the minimum index
    word_after_last_match = ""
    last_match_index = -1  # Track the index of the last match so that we can return properly
    # Track the index of the last query word that had a match
    last_match_query_word_index = -1
    # early return if no match is found

    for i, query_word in enumerate(query_words):
        for j, command_word in enumerate(command_words):

            if command_word.startswith(query_word):
                # set the first match
                if j < match:
                    match = j

                if j > last_match_index:
                    last_match_index = j
                    last_match_query_word_index = i
                    word_after_last_match = command_words[j +
                                                          1] if j + 1 < len(command_words) else ""

        if last_match_query_word_index == i:
            continue

        # we don't have a match for this query word, so we can return early
        else:
            return {
                "match": float('inf'),
                "word_after_last_match": ""
            }

    # we have a match for all the query words, so we can return the match and the word after the last match
    return {
        "match": match,
        "word_after_last_match": word_after_last_match
    }


def compare_results(a: dict, b: dict) -> int:
    # Compare based on the first match index
    if a['match'] != b['match']:
        return a['match'] - b['match']

    # If the first match index is the same, compare based on the word after the last match
    return (a['word_after_last_match'] > b['word_after_last_match']) - (a['word_after_last_match'] < b['word_after_last_match'])


def simple_fuzzy_search(history: list, query: str) -> list:
    results = []

    for command in history:
        match_result = match(query, command)
        if match_result['match'] < float('inf'):
            results.append({
                'command': command,
                'match': match_result['match'],
                'word_after_last_match': match_result['word_after_last_match']
            })

    # Sort the results based on the first match index and then by the word after the last match
    results.sort(key=lambda x: (x['match'], x['word_after_last_match']))

    # Return the top 3 results
    return [result['command'] for result in results[:3]]


if __name__ == '__main__':
    history = ["git status", "git commit -m 'init'", "npm start", "git push"]
    query = "git"

    print(simple_fuzzy_search(history, query))
