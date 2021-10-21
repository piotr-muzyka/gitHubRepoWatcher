# Github Repo Watcher
> Python app which monitors repositories of a specific user and notifies when new git repositories are created.

![Lint workflow](https://github.com/piotr-muzyka/gitHubRepoWatcher/actions/workflows/pylint.yml/badge.svg)
![Test workflow](https://github.com/piotr-muzyka/gitHubRepoWatcher/actions/workflows/python-app.yml/badge.svg)
![Dockerfile workflow](https://github.com/piotr-muzyka/gitHubRepoWatcher/actions/workflows/docker-image.yml/badge.svg)


## Table of Contents
* [Setup](#setup)
* [Usage](#usage)
* [Room for Improvement](#room-for-improvement)
<!-- * [License](#license) -->

## Setup
Tested with:
- minikube `v1.23.2`
- kubectl  `v1.22.2`
- helm     `v3.7.0`

## Usage

The app is containerized and made available in [docker hub](https://hub.docker.com/r/pmuzyka/githubwatcher)  
The run it just with docker it needs redis running in parallel. Prior to running githubwatcher redis can be started using following command `docker run -it --rm -p 6379:6379 -d --name redis-headless redis` followed by 

### Helm chart installation

#### Redis
For redis installation bitnami helm chart in standalone architecture has been used:

Deployment steps:  
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install redis bitnami/redis --set serviceType=NodePort --set architecture=standalone --set auth.enabled=false
```

#### GITHUB WATCHER
Prior to github watcher deployment it is required to either create environment variables:
- `GITHUB_USER` - storing github username which repository will be observed,
- `GITHUB_TOKEN` - to be used to authenticate when calling Github, this allows to extend the API calls limit (unauthenticated - 60 calls per 1hour, authenticated 30 requests per minute). It can be generated via `https://github.com/settings/tokens`. Token scope required to run this app is "repo: public_repo". 

To pass those values to the helm chart, those can be set as environments and then passed to the chart with following commands: 

- Linux
```
export GITHUB_USER=<username_here>
export GITHUB_TOKEN=<token_here>
helm upgrade --install githubwatcher githubwatcher/ --values githubwatcher/values.yaml --set Values.username=$GITHUB_USER --set Values.password=$GITHUB_TOKEN
```

- Windows - PowerShell
```
$env:GITHUB_USER=<username_here>
$env:GITHUB_TOKEN=<token_here>
helm upgrade --install githubwatcher githubwatcher/ --values githubwatcher/values.yaml --set Values.username=$env:GITHUB_USER --set Values.password=$env:GITHUB_TOKEN

```

Alternatively those values can be also set directly in `values.yaml`, in such case this file shouldn't be shared or made public as it will contain a user generated token.

From github repo, helm/githubwatcher
`helm install githubwatcher githubwatcher/ --values githubwatcher/values.yaml`

## Room for Improvement
Well frankly quite a lot, just to mention a few:
- Application: 
  - catch exceptions by github access, db,
  - make redis host and port configurable (easiest fix to make those image variables or mount a configuration file and read from it)
  - improve the tests,

- periodic check: 
  - explore kubernetes cronJob way or consider using Celery for that,
  
- helm, Dockerfile:
  - make helm chart cleaner, think of a better way to pass the secrets to the chart,

- CI/CD
  - build a pipeline for building a docker image, linting it (hadolint?),
