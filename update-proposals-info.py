import random
import json
import requests
from github import Github


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
    per_page = 100
    ideas = []
    for funnelStage in goptions["stages_ids"]:
        for n in range(10):
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
                            "description": idea['text']
                        }
                        if 'authorInfo' in idea:
                            tempIdea['author'] = idea['authorInfo']['userName']
                        if 'customFieldsByKey' in idea:
                            # Regular challenges
                            customKeys = [
                                'requested_funds', 'problem_solution', 'relevant_experience',
                                'challenge_brief', 'how_does_success_look_like_', 'importance',
                                'requested_funds_coti'
                            ]
                            for k in customKeys:
                                if (k in idea['customFieldsByKey']):
                                    tempIdea[k] = idea['customFieldsByKey'][k]
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
            g = Github(goptions['github_access_token'])
            repo = g.get_repo(goptions['github_feedback_challenge_backend_repo'])
            contents = repo.get_contents("data/f7/proposals.json")
            with open('data/f7/proposals.json', 'w') as outfile:
                json.dump(ideas, outfile)
            repo.update_file(contents.path, "Update proposals info", json.dumps(ideas), contents.sha)
        except Exception as e:
            print(e)
main()
