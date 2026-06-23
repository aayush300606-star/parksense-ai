import json
import sys

transcript_path = r"C:\Users\Aayus\.gemini\antigravity\brain\0df84e42-816b-4523-b9f2-631c41f97547\.system_generated\logs\transcript.jsonl"
files_seen = {}

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            if step.get('type') == 'TOOL_RESPONSE' and 'tool_calls' in step:
                # We need to find tool calls from previous steps that match this response?
                # Actually, the content of view_file response contains the file text.
                pass
            if step.get('type') == 'PLANNER_RESPONSE':
                # Just search text for the file contents
                pass
        except:
            pass

# Better logic: just search for "File Path: `file:///c:/Users/Aayus/Desktop/hackearth/parksense-app/"
import re

content = open(transcript_path, 'r', encoding='utf-8').read()

# The tool response for view_file looks like:
# "output": "Created At: ...\nCompleted At: ...\nFile Path: `file:///c:/...`\nTotal Lines: ...\nTotal Bytes: ...\nShowing lines 1 to ...\nThe following code has been modified to include a line number before every line... \n1: ..."

matches = re.finditer(r'File Path: `(file:///[^`]+)`.*?The following code has been modified.*?\\n1: (.*?)\\nThe above content shows', content, re.DOTALL)

for match in matches:
    path = match.group(1)
    file_content_with_lines = match.group(2)
    # Remove line numbers
    lines = file_content_with_lines.split('\\n')
    cleaned_lines = []
    for l in lines:
        if re.match(r'^\d+:\s', l):
            cleaned_lines.append(l.split(': ', 1)[1])
        else:
            cleaned_lines.append(l)
    
    # Save the first instance of each file we see (which would be the oldest/original)
    if path not in files_seen:
        files_seen[path] = '\n'.join(cleaned_lines)

import os
os.makedirs("recovered", exist_ok=True)
for path, text in files_seen.items():
    filename = path.split('/')[-1]
    with open(f"recovered/{filename}.txt", "w", encoding='utf-8') as f:
        # fix json string escaping
        text = text.replace('\\"', '"').replace('\\\\', '\\').replace('\\t', '\t')
        f.write(text)
        print(f"Recovered {filename} from {path}")
