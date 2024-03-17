import json


def append_to_jsonl(file_path, task, options):
    data = {
        "task": task,
        "options": options
    }

    with open(file_path, "a", encoding="utf-8") as file:
        json.dump(data, file)
        file.write("\n")


# Example usage
append_to_jsonl("my_test1.jsonl", "What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"])
append_to_jsonl("my_test1.jsonl", "What is the largest planet in our solar system?", ["Earth", "Jupiter", "Mars", "Venus"])