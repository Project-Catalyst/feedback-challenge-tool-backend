# FeedbackChallenge tool backend

This repo contains a utility to update the count of assessments received by
proposals in Project Catalyst. These data are intended to be consumed by the
[CA tool](https://github.com/Project-Catalyst/ca-tool).

## Configuration

Install requirements with:

```
pip3 install -r requirements.txt
```

Copy `options.json.template` to `options.json` and set:

- `github_access_token` the Github token used to push the updates to the json
file. You have to create the token from Github Profile -> Settings -> Developer
Settings -> Personal Access Token. The token needs the `repo` scopes and you
need to have write access to the repository.
- `ideascale_api_token` the API token used to fect data from the Ideascale API.
- `ideascale_base_api_url` the Ideascale API base url, like
`https://cardano.ideascale.com/a/rest`
- `stages_ids` the ids of the stages to use to pull the proposals.
- `ideas_stage_endpoint` the endpoint to get all the proposal per stage.


## Usage

Launch the script with:

```
python3 update-proposals-info.py
```

Optionally set a cronjob to regularly update the file.
