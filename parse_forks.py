import json

file_path = '/Users/mingzhecong/.gemini/antigravity/brain/e680e0f6-4f04-43c8-bfdf-4f20367fc48e/.system_generated/steps/243/content.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of the JSON array
json_start = content.find('[')
if json_start != -1:
    json_str = content[json_start:]
    try:
        forks = json.loads(json_str)
        # Assuming the API returned them sorted by stars (sort=stargazers)
        top_20 = forks[:20]
        for i, fork in enumerate(top_20):
            name = fork.get('full_name', 'Unknown')
            stars = fork.get('stargazers_count', 0)
            desc = fork.get('description', 'No description provided.')
            # Replace newlines in description for cleaner output
            if desc:
                desc = desc.replace('\n', ' ').replace('\r', '')
            print(f"{i+1}. **{name}** (⭐ {stars}): {desc}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
else:
    print("Could not find JSON data in the file.")
