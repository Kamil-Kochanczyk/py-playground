**CI/CD** is a set of practices that automates building, testing, and deploying software, while **GitHub Actions** is GitHub’s built-in platform designed to run those automated pipelines.

**What is CI/CD?**

CI/CD replaces manual checks and deployments with automated code pipelines:

* **Continuous Integration (CI):** Developers push code changes frequently to a shared repository. Every push automatically triggers automated builds and test suites to catch bugs immediately before code merges.
* **Continuous Delivery / Continuous Deployment (CD):** Once code passes tests, CD automates preparing or pushing those updates directly to staging environments or live production servers (e.g., AWS, Vercel).

**What is GitHub Actions?**

GitHub Actions allows you to configure CI/CD pipelines right inside your GitHub repository using **YAML configuration files** stored in a `.github/workflows/` folder.

**Key Concepts in GitHub Actions**

| Concept | What It Is | Example |
| --- | --- | --- |
| **Workflow** | The overall automated process defined in a `.yml` file. | "Run Tests & Deploy to Production" |
| **Event (`on`)** | The trigger that tells the workflow when to start. | `push`, `pull_request`, or a daily schedule |
| **Runner** | A temporary virtual machine (Ubuntu, Windows, or macOS) that runs your commands. | `runs-on: ubuntu-latest` |
| **Job** | A set of steps executed sequentially on the same runner. | `build`, `test`, or `deploy` |
| **Step** | An individual task within a job (either a shell command or a pre-built Action). | Running `npm test` |
| **Action** | Reusable, pre-packaged blocks of code created by GitHub or the community. | `actions/checkout@v4` (pulls your code into the runner) |