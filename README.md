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