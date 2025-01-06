import sys
import subprocess
from ai import ask_the_AI_overlord

cmd_string = "git status"
output = subprocess.run(cmd_string.split(" "), stdout=subprocess.PIPE)
git_status_output = output.stdout.decode("utf-8")

cmd_string = "git diff"
output = subprocess.run(cmd_string.split(" "), stdout=subprocess.PIPE)
git_diff_output = output.stdout.decode("utf-8")

cmd_string = "git diff --cached"
output = subprocess.run(cmd_string.split(" "), stdout=subprocess.PIPE)
git_diff_cached_output = output.stdout.decode("utf-8")

full_status_output = f'''Given the following `git status` output:

```
{git_status_output}
```

And the current `git diff`:

```
{git_diff_output}
```

And the current `git diff --cached`:

```
{git_diff_cached_output}
```

What do you recommend as the next command for me to execute?'''

prompt_filepath = "prompt.txt"
with open(prompt_filepath, "w") as f:
    f.write(full_status_output)
    print("Written the prompt to:", prompt_filepath)

response = ask_the_AI_overlord(full_status_output)
if response is None:
    sys.exit(1)
print(response)
