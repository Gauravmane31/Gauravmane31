# Gauravmane31 Profile README — Setup

This profile repo is designed to work without the public `github-readme-stats.vercel.app` service.

## 1. Replace the contents of your profile repository

Use this repository as the contents of `Gauravmane31/Gauravmane31`.

## 2. Enable GitHub Actions

Go to **Settings → Actions → General** and make sure actions are allowed. Under **Workflow permissions**, allow workflows to have **Read and write permissions**. The workflow files also request `contents: write`.

## 3. Run the workflows once

Open **Actions** and manually run:

- `Update GitHub Stats`
- `GitHub-Profile-3D-Contrib`
- `Generate Contribution Snake`

The stats workflow calls the GitHub API with the built-in `GITHUB_TOKEN` and writes `profile/stats.svg` and `profile/top-langs.svg` into this repository.

The 3D workflow is based on the supplied reference repository's workflow and generates the same family of 3D contribution SVGs for `Gauravmane31`.

The snake workflow is based on the supplied reference repository's workflow, with the username changed to `Gauravmane31`. It publishes the generated SVGs to the `output` branch.

## 4. If a workflow is blocked

Check **Settings → Actions → General → Workflow permissions** and enable **Read and write permissions**. Then run the workflow again.

## 5. Project links

The README does not invent repository URLs for projects whose exact repository names were not available. Replace the marked project URLs with the actual repositories when you have them.
