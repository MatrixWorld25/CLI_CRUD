# Submission Guide

## Initialize Git

```bash
git init
git status
git add .
git commit -m "Complete Task 1 CLI CRUD application"
```

## Create a Public GitHub Repository

1. Sign in to GitHub.
2. Create a new public repository.
3. Name it something clear, such as `CLI_CRUD`.
4. Do not add a README or license on GitHub if the local project already contains them.

## Push the Project

```bash
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git
git branch -M main
git push -u origin main
```

## Create GitHub Tag v1.0.0

```bash
git tag -a v1.0.0 -m "Task 1 release"
git push origin v1.0.0
```

## Create GitHub Release

1. Open the repository on GitHub.
2. Go to Releases.
3. Choose Draft a new release.
4. Select tag `v1.0.0`.
5. Add a concise release title and notes.
6. Publish the release.

## URLs to Submit

- Repository URL: `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>`
- Release URL: `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>/releases/tag/v1.0.0`

## LinkedIn Post Checklist

- Mention the project name.
- Summarize the CLI CRUD features.
- Include the GitHub repository link.
- Include the release link if required.
- Keep the post professional and concise.

## Security Checklist

- Do not commit `.env` files.
- Do not commit credentials, tokens, or API keys.
- Review `git status` before committing.
- Confirm `data/records.json` contains only intended sample data or `[]`.
- Keep the repository public only if the assignment requires it.
