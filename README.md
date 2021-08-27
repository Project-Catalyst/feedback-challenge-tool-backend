# CA tool backend

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
- `ideascale_base_api_url` the Ideascal API base url, like
`https://cardano.ideascale.com/a/rest`
- `assess_funnel_stage_ids` the ids tf the funnel stages to query
- `assess_funnel_endpoint` the endpoint for `getAssessmentResults`.


## Usage

Launch the script with:

```
python3 update-assessments-count.py
```

Optionally set a cronjob to regularly update the file.
