# Document Portal

## Project folder

Create the project folder and open it in Visual Studio Code:

```bash
mkdir my-project
cd my-project
# Open in VS Code (requires `code` in PATH)
code .
```

## Conda virtual environment setup

Recommended: create and activate a named conda environment:

```bash
# Create a named environment
conda create -n env_name python=3.10 -y

# Activate the environment
conda activate env_name

# Install Python dependencies
pip install -r requirements.txt
```

Alternative: create a path-based environment (prefix) inside the project:

```bash
conda create -p ./env python=3.10 -y
conda activate ./env
pip install -r requirements.txt
```

Notes:
- Use `-n <name>` to create a named environment or `-p <path>` to create a prefix (path) environment.
- If you use a prefix (`-p ./env`) then the activation command is `conda activate ./env`.
- Make sure the file is named `requirements.txt` (fixed typo).

## Git project commands

Initialize a repository, add a sensible `.gitignore`, and push to a remote:

```bash
# Initialize (run once)
git init

# Example: ignore environment folder or manually add env/ to the file 
echo "env/" >> .gitignore

# Stage and commit
git add .
git commit -m "Initial commit"

# Add remote (replace with your remote URL) and push
git remote add origin <REMOTE_URL>
git push -u origin main
```

If you prefer the VS Code publish flow, use the Source Control view and click "Publish to GitHub" or similar and follow the prompts.

## Troubleshooting

- If `code .` isn't found, install the "Shell Command: Install 'code' command in PATH" from the VS Code Command Palette.
- If `pip install -r requirements.txt` fails, ensure the correct conda env is activated and that `requirements.txt` exists in the project root.

---

If you'd like, I can also:
- add a `.gitignore` with common entries, or
- create a `requirements.txt` template, or
- keep this README but add a short example of how to run the project.

## requirement for this project
- LLM Models from groc(free)/openai(paid)/gemini(15 days free)/claude(paid)/huggingface(free)/oola(localo setup)
- Embedding models from openai/HF/gemini
- vecortdatabase from inmemory/ondisk/cloudbase

## run below command to initiate setup.py
pip install -e .

## Groq api link -to create api key
https://console.groq.com/keys

## Google Ai studion to create api key 
https://aistudio.google.com/

# command for executing the fast api main.py from app folder : cmd to api folder where you have this main.py file and run below command 
# uvicorn is a  application server interface
# uvicorn api.main:app --port 8080 --reload    
# uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload

## to create docker image , create docker file and docker ignore filr 
docker build -t document-portal-system .

## to run and publish docker image to docker container 
docker run -d -p 8093:8080 --name my-doc-portal document-portal-system

# make sure to keep docker desktop open and engine should be running 

# next step : CICD 

# login to AWS console and search and select ECR
# create -> https://us-east-2.console.aws.amazon.com/ecr/private-registry/repositories?region=us-east-2
# create with name documentportalliveclass
# all setting are default , select ingage scanning - > Scan on push to on 
# copy repository name and URI to notepad 

# Create IAM User on aws console search IAM 

# create users -> select user from lef side and click next 
# select attach policies radio 
# ![alt text](image.png)
# select these permissions: AmazonEC2ContainrRegistoryFullAccess, AmazonECS_fullaccess,AmazonS3Fullaccess,AmazonSSMreadonlyaccess,Cloudwatchlogsfullaccess,secretsmanagerreadwrite
# click create and verify permissions 
# click on user name and select security credential 
# copy arn, then go to access key section and click on create access key 
# select command line interface , and select checck box for cconfirmation. Click on create > next 
# get access key and secrete , note down it.
# Goto ECR > select name created > from left side check Repository > Images  = nothing as of now 

## Github 
# go to settings > secrets and variables > actions 
# click new repository secrets 
# add AWS_ACCESS_KEY_ID in name and value = your access key 
# Add another AWS_SECRET_ACCESS_KEY and its value 

# now goto git hub repo > .github>workflow> CI.yaml file check names under 'check out repo' and verify names for aws_access key and secret variable matches 

# do the same under section Configure aws credenttials as well 

# push any changes to githib and verify youur aws ECR has a image by selecting name of ECR and under images 

# now go to Github > actions and it should trigger test and it should deploy image check on actions and Buid and push docker image task and check on AWS ECR 

# On aws ECR - Image is created you can verify 

# on github actions you will see deploy to ECS fargate deploy failed 


## AWS config for secrets manager 
# create new secret , add name and add 2 keys for groq_api_key and google_api_key
# when you reenter on secrete page and click on name of secrete > click on reveal secret value to see all variable created 
# make sure to note arn name and update it in task_definition.json under .github/workflow

## AWS config for ECS
# open ECS and select Cluster from left side to create cluster 
# provide cluster name as per aws.yaml file from .github/workflow/aws.yaml
# selct infrqastructure as AWS fargate
# click create and ECS cluster has been created.

# now click on Task definition from ECS page -left pane 
# from right top side click on create new task definition -> from json 
# now copy your task-definition from .github/workflow/task-definition.json 
# paste it on AWS ECS - Task definition 
# click on create
# next click on cluster and create service , make sure service name should be same as aws.yaml file ECS_SERVICE: document-portal-service1
# now commit changes and push it to git , then check guthub> action for deployment progress
# application should be deployed 

## AWS for debugging , add incline policy for IAM user created from /Users/kiran_mac/Documents/Sunny_document_portal/incline_policy.json


# if you still dont see public ip on ECS then go to EC2>Security Groups > click on security group >  edit inbound rules > click on add rule 
# Add type as custom TCP , port range as 8080, source as custom, next text box as 0.0.0.0/0 select , description as allow public access to app 
# click on save rule 




