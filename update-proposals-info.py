import random
import json
import requests
from markdownify import markdownify as md
from github import Github

tags_to_strip = ['a', 'b', 'img', 'strong', 'u', 'i', 'embed', 'iframe']

def loadOptions(goptions = {}):
    try:
        with open('./options.json', 'r') as f:
            options = json.load(f)
            for k in options:
                goptions[k] = options[k]
    except Exception as e:
        print(e)
        print("Error loading options.json")
    return goptions

def getIdeas(goptions):
    headers = {
        'api_token': goptions["ideascale_api_token"]
    }
    per_page = 50
    ideas = []
    for funnelStage in goptions["stages_ids"]:
        for n in range(15):
            url = goptions["ideascale_base_api_url"] + \
                goptions["ideas_stage_endpoint"].format(funnelStage, n, per_page)

            print("Requesting url: {}".format(url))
            r = requests.get(url, headers=headers)
            try:
                response = r.json()
                if (r.status_code == 200):
                    for idea in response:
                        tempIdea = {
                            "id": idea['id'],
                            "category": idea['campaignId'],
                            "comments_count": idea['commentCount'],
                            "title": idea['title'],
                            "url": idea['url'],
                            "description": md(idea['text'], strip=tags_to_strip),
                            "tags": idea['tags']
                        }
                        if 'authorInfo' in idea:
                            tempIdea['author'] = idea['authorInfo']['userName']
                        if 'customFieldsByKey' in idea:
                            # Regular challenges
                            customKeys = [
                                'requested_funds', 'problem_solution', 'relevant_experience',
                                'how_does_success_look_like_', 'importance',
                            ]
                            for k in customKeys:
                                if (k in idea['customFieldsByKey']):
                                    tempIdea[k] = md(idea['customFieldsByKey'][k], strip=tags_to_strip)
                        ideas.append(tempIdea)
                if (len(response) < per_page):
                    break
            except Exception as e:
                print("Fuck Ideascale")
                print(e)
    print("Total ideas: {}".format(len(ideas)))
    return ideas

def main():
    goptions = loadOptions()
    ideas = getIdeas(goptions)
    if (len(ideas)):
        try:
            if (goptions['github_access_token']):
                g = Github(goptions['github_access_token'])
                repo = g.get_repo(goptions['github_feedback_challenge_backend_repo'])
                contents = repo.get_contents("data/f9/proposals.json")
                with open('data/f9/proposals.json', 'w') as outfile:
                    json.dump(ideas, outfile)
                repo.update_file(contents.path, "Update proposals info", json.dumps(ideas), contents.sha)
            else:
                with open('data/f9/proposals.json', 'w') as outfile:
                    json.dump(ideas, outfile)
        except Exception as e:
            print(e)
main()
