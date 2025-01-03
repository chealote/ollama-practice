import json
import requests
import sys
import subprocess
import re

url = "http://localhost:11434/api/chat"

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
output = subprocess.run(["git", "diff"], stdout=subprocess.PIPE)

payload["messages"].append({
    "role": "user",
    "content": output.stdout.decode("utf-8"),
    })

response = requests.post(url, json=payload, stream=True)
for line in response.iter_lines():
    if line:
        j = json.loads(line)
        sys.stdout.write(j["message"]["content"])

# TODO ask to run the full commit command
