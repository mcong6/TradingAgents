import json
import urllib.request
import urllib.error

file_path = '/Users/mingzhecong/.gemini/antigravity/brain/e680e0f6-4f04-43c8-bfdf-4f20367fc48e/.system_generated/steps/243/content.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

json_start = content.find('[')
json_str = content[json_start:]
forks = json.loads(json_str)
top_20 = forks[:20]

# Known repos that we already analyzed or are just translations/A-share/crypto/gui/dashboard
known_owners = ['0x0funky', 'Bronny-62', 'TheLocalLab', 'jiwoomap', 'hkwsg', 'Yung-Chih-Lo', 'tinkermend', 'MarkLo127']

unknown_forks = [f for f in top_20 if f['owner']['login'] not in known_owners]

print("Investigating commits of other forks...\n")

headers = {'User-Agent': 'Mozilla/5.0'}

for fork in unknown_forks:
    repo_name = fork['full_name']
    commits_url = f"https://api.github.com/repos/{repo_name}/commits?per_page=3"
    
    try:
        req = urllib.request.Request(commits_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            commits_data = json.loads(response.read().decode())
            print(f"--- {repo_name} (⭐ {fork['stargazers_count']}) ---")
            for c in commits_data:
                msg = c['commit']['message'].split('\n')[0] # Get first line
                print(f" - {msg}")
            print()
    except urllib.error.URLError as e:
        print(f"Failed to fetch commits for {repo_name}: {e}\n")
