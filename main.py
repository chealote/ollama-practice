import json
import requests
import sys
import subprocess
import re

# options: [ yes, no, ... ]
# answers: 0 1 2
def get_option(options=["yes", "no"]):
    prompt = "> "
    option = input(prompt).lower()
    while True:
        try:
            index = options.index(option)
            break
        except ValueError:
            print("Please answer any of these:", options)
            option = input(prompt).lower()

    return options.index(option)

def get_suggestion(payload):
    url = "http://localhost:11434/api/chat"
    try:
        response = requests.post(url, json=payload, stream=True)
    except Exception as e:
        print("ERROR: the AI failed to reply:", e)
        sys.exit(1)
    suggested_command = ""
    for line in response.iter_lines():
        if line:
            j = json.loads(line)
            suggested_command += j["message"]["content"]
    return suggested_command

payload = {
        "model": "llama3.2:1b",
        "messages": [],
        }

with open("prompt.txt") as f:
    file_content = f.read()

messages = []
role = ""
content = ""
in_content_part = False
for line in file_content.split("\n"):
    if in_content_part:
        if line == "":
            messages.append({
                "role": role,
                "content": content,
                })
            in_content_part = False
            content = ""
            role = ""
            continue
        content += line

    if re.match("role:", line):
        role = line.split(" ")[1]
    elif re.match("content:", line):
        in_content_part = True
        content += re.sub("content: *", "", line)

payload = {
        "model": "llama3.2:1b",
        "messages": messages,
        }

# TODO ask to run `git diff`
init_command_diff = "git diff --cached"

print("Run the following? (yes/no):", init_command_diff)

if get_option() != 0:
    print("You have to answer YES!")
    sys.exit(1)

output = subprocess.run(init_command_diff.split(" "), stdout=subprocess.PIPE)

payload["messages"].append({
    "role": "user",
    "content": output.stdout.decode("utf-8"),
    })

suggested_command = get_suggestion(payload)

print("")
print("The AI has spoken, it suggests the following command:")
print(suggested_command)
print("Will you run it? (yes/no/other)")
option = get_option(["yes", "no", "other"])

while option != 0:
    if option == 1:
        print("The AI will remember that...")
        sys.exit(1)

    if option == 2:
        suggested_command = get_suggestion(payload)
        print("Here's another suggestion:")
        print(suggested_command)
        print("Will you run it? (yes/no/other)")

    option = get_option(["yes", "no", "other"])
    print("You answer:", option, "and the sugg command is:", suggested_command)


commit_msg = re.findall("'[^']+'$", suggested_command)[0]
commit_cmd = re.findall("^[^']+", suggested_command)[0]
full_commit_cmd = commit_cmd.split(" ")
full_commit_cmd.append(commit_msg)

output = subprocess.run(full_commit_cmd, stdout=subprocess.PIPE)
print(output)

# TODO ask to run the full commit command
