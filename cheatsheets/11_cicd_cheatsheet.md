## Overview

**CI/CD** is a set of practices that automates building, testing, and deploying software, while **GitHub Actions** is GitHub’s built-in platform designed to run those automated pipelines.

## What is CI/CD?

CI/CD replaces manual checks and deployments with automated code pipelines:

* **Continuous Integration (CI):** Developers push code changes frequently to a shared repository. Every push automatically triggers automated builds and test suites to catch bugs immediately before code merges.
* **Continuous Delivery / Continuous Deployment (CD):** Once code passes tests, CD automates preparing or pushing those updates directly to staging environments or live production servers (e.g., AWS, Vercel).

> [!TIP]
> CI = operations applied before new code is merged to make sure it is of good quality
>
> CD = operations applied after new code has been merged to make it quickly available

## What is GitHub Actions?

GitHub Actions allows you to configure CI/CD pipelines right inside your GitHub repository using **YAML configuration files** stored in a `.github/workflows/` folder.

## Key Concepts in GitHub Actions

GitHub Actions are written using **YAML** files and syntax. (https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started)

| Concept | What It Is | Example |
| --- | --- | --- |
| **Workflow** | The overall automated process defined in a `.yml` file. | "Run Tests & Deploy to Production" |
| **Event (`on`)** | The trigger that tells the workflow when to start. | `push`, `pull_request`, or a daily schedule |
| **Runner** | A temporary virtual machine (Ubuntu, Windows, or macOS) that runs your commands. | `runs-on: ubuntu-latest` |
| **Job** | A set of steps executed sequentially on the same runner. | `build`, `test`, or `deploy` |
| **Step** | An individual task within a job (either a shell command or a pre-built Action). | Running `npm test` |
| **Action** | Reusable, pre-packaged blocks of code created by GitHub or the community. | `actions/checkout@v4` (pulls your code into the runner) |

`${{ }}` is the expression syntax used in GitHub Actions to dynamically evaluate values, access context data, and run functions within your workflow YAML files. Expressions inside `${{ }}` are processed directly before the job is sent to a runner. Key uses:
* **Accessing Contexts**: Retrieve runtime metadata about the workflow, events, jobs, or steps using objects (contexts) like `github`, `env`, `secrets`, `steps`, and `vars`.
* **Evaluating Conditionals**: Control whether a job or step runs using `if:` statements. (Note: In if conditionals, `${{ }}` is technically optional, but if included, it must wrap the entire expression).
* **String Interpolation and Functions**: Combine strings, evaluate logic, or transform data using built-in functions like `format()`, `join()`, or `contains()`.

| Use Case | Example Syntax | Description |
|---|---|---|
| Accessing Context | `run: echo "${{ github.actor }}"` | Prints the username of the person who triggered the workflow. |
| Using Secrets | `env: API_KEY: ${{ secrets.MY_SECRET }}` | Injects a secure repository secret into an environment variable. |
| Conditional Check | `if: ${{ github.event_name == 'push' }}` | Runs a step only if the triggering event is a push. |
| Print Context Info | `GITHUB_CONTEXT: ${{ toJson(github) }}` | Pretty-prints JSON `github` object to the log |

`needs` is a keyword used to create dependencies between jobs, forcing them to run sequentially rather than in parallel.
By default, all jobs in a GitHub Actions workflow run simultaneously. When you add `needs` to a job, you tell GitHub Actions that the job must wait for the specified prerequisite job(s) to finish successfully before it can start. Capabilities:

* **Defining Order**: GitHub Actions uses `needs` to build a Directed Acyclic Graph (DAG). It maps out exactly which jobs depend on others.
  * **Single dependency**: Pass a single job ID as a string.
  * **Multiple dependencies**: Pass an array of job IDs. The dependent job will only run once all listed jobs complete successfully.
* **Passing Data Between Jobs**: A downstream job cannot natively see the environment or variables of an upstream job. However, if a job `needs` another, it gains access to the `needs` context, allowing it to share data and outputs across job boundaries.

> [!WARNING]
> * If a prerequisite job fails or is skipped, any downstream jobs that depend on it are automatically skipped by default.
> * If you want a dependent job to run even if its prerequisite fails, you must combine needs with an `always()` conditional check: `needs: build; if: always() # Runs even if 'build' fails`
> * The `needs` context only contains outputs from your direct dependencies. If Job C `needs` Job B, and Job B `needs` Job A, Job C cannot directly read outputs from Job A unless you explicitly add Job A to C's `needs` array. 

## Example scenarios

* Docker
  * automatically tag, build, push a Docker image to your Docker Hub registry, and scan it for vulnerabilities
* Python
  * automatically lint, format, typecheck, build, test and publish your Python package to an index

These scenarios can be configured to happen automatically on every:

* commit push,
* pull request,
* tag push,
* ...

## Deployments and environments

> [!IMPORTANT]
> GitHub **deployments** are first-class API objects and tracking features in GitHub that represent a specific version or release of your codebase being shipped to a target environment (such as `production`, `staging`, or `development`).

> [!NOTE]
> `production`, `staging` and `development` refer to the lifecycle of a software: `development` (devs) -> `staging` (test users) -> `production` (real users).

> [!IMPORTANT]
> GitHub Actions **Environments** are used to control and protect deployment targets (such as `production`, `staging`, or `development`). They allow you to apply protection rules—like requiring manual approval or restricting which git branches can deploy—and to isolate environment-specific secrets and configuration variables.

> [!TIP]
> When you run a GitHub Actions workflow job that targets a specific `environment` using the environment key, GitHub automatically creates a deployment record, tracks its lifecycle, and logs its history.

Key features:

* **Environment Protection Rules**: Require human reviewers to approve a workflow run before a job proceeds to sensitive environments.
* **Environment Secrets & Variables**: Store secrets (e.g., AWS keys, database passwords) and variables (e.g., API endpoints) that are scoped specifically to a targeted environment, preventing non-production jobs from accessing production keys.
* **Deployment Branch Policies**: Limit which branches or tags can deploy to a specific environment (e.g., only allowing the `main` branch to deploy to `production`).
* **Deployment Tracking**: Automatically logs deployments under the **Deployments** tab on GitHub, giving you visibility into what commit or image is deployed where.

## Security

> [!WARNING]
> When publishing your code try to use **Trusted Publishing** with **OIDC** (**Open ID Connect**) instead of manually generated **API tokens**.
>
> *The traditional way to publish a Python package is to generate an API token on PyPI, store it as a secret in your system (or on your local machine), and pass it to your upload tool. This workflow has several weaknesses: tokens are long-lived, portable, have big scope and must be stored somewhere.*
>
> *Trusted Publishing is the modern, preferred way:*
>
> * *You configure a trusted publisher on PyPI, specifying which CI provider, repository, and workflow are allowed to upload your package.*
> * *When the CI workflow runs, it requests a short-lived OIDC token from the CI provider (e.g., GitHub). This token contains signed claims about the workflow: which repository it belongs to, which workflow file triggered it, and which branch or tag initiated the run.*
> * *The upload tool (e.g., `uv publish`) sends this OIDC token to PyPI’s token-minting endpoint.*
> * *PyPI verifies the OIDC token’s signature against the CI provider’s public keys and checks that the claims match the trusted publisher configuration. If everything matches, PyPI mints a short-lived, scoped API token and returns it.*
> * *The upload tool uses that short-lived token to upload the package through the normal upload API. The token expires within minutes.*
> * *No secret is stored in CI. No token exists between workflow runs. The credential is created on-demand, scoped to a single job, and expires within minutes.*

> [!TIP]
> Try to always include a GitHub Actions Environment when setting up your trusted publisher for your project, e.g. in PyPI/TestPyPI.

> [!WARNING]
> In CI/CD, Python packaging, and GitHub Actions, an **attestation** is a cryptographically signed statement attached to a software build (like a **.tar.gz** package or a **.whl** package or a Docker image). It acts as a digital birth certificate that proves where, how, and by whom an artifact was generated.
> 
> Don't confuse it with Trusted Publishing and OIDC:
> 
> * attestation = birth certificate of a package (repo = ..., commit = ..., workflow = ..., etc.)
> * Trusted Publishing = access/verification process
> * OIDC = proof that package is coming from this repo/workflow/branch)
>
> An attestation proves:
> * Provenance: Which source code repository, commit hash, workflow, and build environment produced this file?
> * Integrity: Has the compiled file been altered or tampered with since it was built?
> * Identity: Was it built by an authorized, automated process rather than a malicious actor's local machine?
>
> Pros:
> * Supply chain defense: If an attacker steals a maintainer's token or gains partial credentials, they cannot easily impersonate an official GitHub release workflow, e.g. if an attacker compromises a maintainer’s credentials or uploads a malicious package with a matching name, consumers can verify that the file's hash and signature do not match the expected repository source
> * Zero maintenance: GitHub and PyPI automatically handle temporary tokens
