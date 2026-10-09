# Commands

## Basics

- `git config --global --list` - check the global configuration of Git
- `git init` - initialize a non-bare repo (create the `.git` directory)
- `git init --bare` - initialize a bare repo (inside an empty `.git_directory`)
- `git clone <.git_url>` - copy an existing repository into your local directory (use it when you don't have the desired repository in your local project)
- `git status` - see what files are staged, what files are untracked, etc.
- `git add <file_name>` - stage file, i.e. add it to the staging area, i.e. include it in the next commit to snapshot it at this point in the version history
- `git commit -m <commit_message>` - create a snapshot of the project at particular point in time using staged files
- `git rm <file_name>` - remove the file from both the staging area and the disk
- `git rm --cached <file_name>` - remove the file only from the staging area but leave it on the disk (unstages the file completely, i.e. removes it from the staging area and tells Git to stop tracking it altogether and to treat it as an untracked file)
- `git restore <file_name>` - remove the modification of the file relative to the most recent committed version, this command works while the file is still unstaged, this command modifies the contents of the file, the discarded changes may be hard or impossible to recover
- `git restore --staged <file_name>` - unstage file for the next commit, i.e. do not include it in the next commit but in general still keep track of it, this command works while the file is already staged, this command does not modify the contents of the file

## Remotes

- `git remote add origin <.git_repository_url>` - tell the Git where to find the remote repository for the current local repository
- `git remote add upstream <.git_repository_url>` - tell the Git where to find the upstream (original) repository for your locally cloned fork repository
- `git remote -v` - list the current remote repositories (by default for every remote repository Git treats read (fetch) and write (push) URLs as distinct even though in practice usually they are the same URL)
- `git remote remove <name, e.g. origin>` - dangerous, disconnect your local repo from some other repo (e.g. your remote repo or a repo of a contributor which created a pull request for your project and you tested and verified it and then want to clean your repo from unnecessary connections)
- `git remote rename <what?, e.g. origin> <to_what?, e.g. github-backup>` - rename remote repo (safer than the command above)

## Pushing

- `git push -u origin <branch_name>` - push from the current local branch to a branch in a remote repository and set up a tracking reference between those two branches, this command should be used when first time pushing a new branch
- `git push` - push from the current local branch to the tracked branch on the remote repository, this command (which does not specify the name of the branch on the remote repository) can be used after the command with the `-u` option has been used when pushing the branch for the first time, because the `-u` option establishes a relationship (a tracking reference) between the branches
- `git push origin --delete <branch_name>` - delete the specified remote branch
- `git push origin <tag_name>` - push the specified tag to the remote repository as, by default, tags are not pushed during standard push operations
- `git push origin --tags` - push all tags to the remote repository

## Fetching

- `git fetch origin [--prune]` - fetch the updates and all other necessary information from the remote repository into your local repository, optionally you can also delete any non-existent remote-tracking references by using `--prune` which can be useful if you delete a local/remote branch but Git still remembers some pointers to that deleted branch
- `git fetch upstream` - fetch the updates from the upstream (original) repository of the locally cloned fork repository

## Merging

- `git merge <branch_name, e.g. origin/master or upstream/main>` - merge (integrate) fetched updates from a specified branch into your current branch, this is the default Standard Merge (but if it's possible in the given case, this command performs the Fast-Forward Merge, since it's faster and simpler)
- `git merge --squash <branch_name, e.g. feature-branch>` - just like above but this time it's Squash Merge

## Pulling

- `git pull` - pull the updates from the corresponding remote branch into the local branch (assuming a tracking reference is set up)

## Branching

- `git branch <branch_name>` - create a new local branch
- `git branch -d <branch_name>` - delete the specified local branch (note that branch is just a label so deleting a branch does not delete absolutely any commits whatsoever)
- `git branch -D <branch_name>` - force-delete the specified local branch, the commits that haven't been merged to your active branch will become orphaned after deleting their branch and eventually they will be deleted by Git's garbage collection system after some time
- `git branch -vv` - display various information about local branches, e.g. their tracking references
- `git branch -vv -a` - display various information about all branches
- `git branch -vv -r` - display various information about remote branches
- `git branch --set-upstream-to=<remote_name, e.g. origin/master>` - set a tracking reference, useful for example in the situation when you temporarily deconnected your local repo from your remote one and later connected them again and you want the main branch of your local repo to track the main branch of your remote repo again

## Switching

- `git switch <branch_name>` - checkout to the chosen branch
- `git switch -c <branch_name>` - create a new branch and immediately checkout it, this is equivalent to `git branch <branch_name>; git switch <branch_name>`

## Rebasing

- `git rebase <branch_name, usually main or master>` - rebase the current active branch onto the specified branch, i.e. move the base of the current branch on top of the tip of the specified branch
- `git rebase --continue` - continue the halted rebase operation, rebase operation can be halted for example when Rebase Merge causes multiple merge conflicts that you need to manually stage one by one before committing and finishing the rebase operation

## Resetting

- `git reset --soft HEAD~n` - move the `HEAD` back by `n` commits to discard `n` commits at front but preserve the changes that those commits made
  - this command is useful when you work locally and haven't shared anything yet to a remote branch
  - say you created a few commits, e.g. `featureA`, then `featureB`, then `featureC`
  - let's say you don't like the commit message of `featureC`, so you run `git reset --soft HEAD~1`; what it does is it removes the commit `featureC` from the local timeline while still preserving the changes that this commit made in your editor; what's more, it actually already puts these changes in the staging area which means that you are actually ready to commit them again with a new message
  - let's also say you don't like that commits `featureA`, `featureB` and `featureC` are separate and you want to turn them into one squashed commit instead, in that case you run `git reset --soft HEAD~3`, as a result you discard all three commits from your local timeline but you still have their changes preserved and already in the staging area which means that after running this command you can simply commit all changes with a single message as if those changes coming from three separate commits were actually made in one go, as a single commit
- `git reset [--mixed] HEAD~n` - just like the soft command above but the difference is that this command clears the staging area which means that changes will not be in the staging area after running this command
  - simpler version `git reset` clears the current staging area and can be interpreted as telling Git to "make the staging area match `HEAD`"
- `git reset --hard HEAD~n` - similar to the mixed command above but with the difference that this command not only clears the staging area but also resets the contents of the files themselves, i.e. the files are brought back to their previous versions and their changes are completely lost (warning: this command can also delete files from disk)
  - simpler version `git reset --hard` clears the current staging area and current file modifications

## Reverting

- `git revert HEAD` - discards the most recent commit by calculating the opposite changes and applying them as a new commit, this command modifies the contents of the files and immediately creates a commit
  - compared to the reset commands, revert commands keep the historical facts but make their effects disappear and undo their changes
- `git revert <commit_hash>` - just like the command above but it discards the commit specified by its hash, this command immediately creates a commit
- `git revert --no-commit <sth, e.g. HEAD~n..HEAD>` - applies reversal without immediately creating a commit, this command is useful e.g. if you want to revert `n` most recent commits with one operation without creating `n` new separate commits to apply `n` reversals
  - this command is usually useful to revert some past commits
- `git revert -m 1 <merge_commit, e.g. HEAD>` - revert the specific merge commit, usually merge commit involves the main branch and a feature branch that is integrated into it, `-m 1` tells Git to treat the main branch as the mainline parent so that Git knows what changes were brought to the main branch by the feature branch and thus calculate the opposite changes to perform the revert operation and undo the changes on the main branch

## Stashing

- `git stash save <descriptive_message>` - save work to the stack, this command does not save untracked files (e.g. newly created files) to the stack
  - `git stash push -m <descriptive_message>` is equivalent
- `git stash save -u <descriptive_message>` - save work to the stack, this command saves untracked files (e.g. newly created files) to the stack
  - `git stash push -u -m <descriptive_message>` is equivalent
- `git stash list` - display all currently stashed items on the stack
- `git stash pop` - apply the latest stash (`stash@{0}`) and remove it from the stack
- `git stash apply` - apply the latest stash (`stash@{0}`) without removing it from the stack
- `git stash apply stash@{n}` - apply the specified stash without removing it from the list
- `git stash show -p` - display what is inside the latest stash (`stash@{0}`)
- `git stash show -p stash@{n}` - display what is inside the specified stash (`diff`)
- `git stash drop` - remove the latest stash (`stash@{0}`) without applying it
- `git stash drop stash@{n}` - remove the specified stash from the stack without applying it
- `git stash clear` - permanently delete all stashed items from the stack
- `git stash branch <branch_name> stash@{n}` - create a new branch from the specified stash, i.e. create a new branch, then checkout, then apply the stash, then drop the stash if applying succeeds without any merge conflicts

## Tagging

- `git tag` - display all tags
- `git tag -d <tag>` - delete a specific tag
- `git tag -a <name, e.g. v1.0.0> -m <message, e.g. "Release version v1.0.0">` - add an annotated tag to the current commit
- `git tag -a <name, e.g. v1.0.0> <commit_hash> -m <message, e.g. "Release version v1.0.0>` - add an annotated tag to the specified commit
- `git tag <name>` - add a lightweight tag to the current commit
- `git tag <name> <commit_hash>` - add a lightweight tag to the specified commit

## Logging

- `git log --oneline --graph -n <how_many_commits?>` - show the list of commits and their hashes
- `git log <branch1>..<branch2> --oneline` - show the comparison what commits are on `branch2` but not on `branch1`
  - `..` is an operator that checks what commits are on its right operand but not on its left operand
  - examples:
    - if you are on the main branch, then `HEAD..origin/main` can tell you what commits you have not pulled yet
    - if you are on the main branch, then `origin/main..HEAD` can tell you what commits you have not pushed yet
    - `main..<feature_branch>` can tell you what commits have been added on `feature_branch` since it split off the main branch

## Reflogging

- `git reflog` - see the reference logs (reflogs are basically your action history and show you how you moved `HEAD` around (locally) by performing various Git operations)

## Showing

- `git show <sth, e.g. HEAD~n>` - display information about various Git objects, mainly commits

## Diffing

- `git diff` - show the difference between the current modifications and the most recent committed version, this command works while the file is still unstaged
- `git diff --staged` - like above but for staged files

## Cherry picking
- `git cherry-pick [-n] <hash1> <hash2>` - pick commits to apply into your current branch, `-n` prevents those commits from being applied immediately and stages the changes instead

## Bisecting

- `git bisect start` - start bisecting to pinpoint a bad commit
- `git bisect good [<hash>]` - mark the commit with the given hash as good, if hash is ommitted, this operations marks the current commit as good
- `git bisect bad [<hash>]` - mark the commit with the given hash as bad, if hash is ommitted, this operations marks the current commit as bad
- `git bisect reset` - finish bisecting and return to your original commit

## Worktrees

- `git worktree add <path to worktree directory, e.g. ../hotfix>` - create a new worktree based on the current branch and commit, the name of the new branch will be the last part of `path`, e.g. for `../hotfix` the new branch will be called `hotfix`
- `git worktree add <path to worktree directory, e.g. ../hotfix> <branch>` - create a new worktree based on the existing branch
- `git worktree add <path to worktree directory, e.g. ../hotfix> -b <branch_name> <base, e.g. main, main~2, or a commit's hash>` - create a new worktree based on the specific branch or commit and with some chosen branch name
- `git worktree remove <path to worktree directory, e.g. ../hotfix>` - remove the specified worktree, this should be typically done when you are not currently inside that worktree
- `git worktree list` - list all worktrees

## Checkouting (legacy)
- `git checkout` - legacy all-in-one command that has been split-up into other smaller and more-focused commands, it can be used for example to checkout to a specific commit and to detach `HEAD`
- `git checkout -b <name, e.g. hotfix-v1.0.1> <tag, e.g. v1.0.0>` - create a new branch off the specified tag (which points to some specific commit) or in other words, create a new branch starting at the specified tag (specified commit)

# `.gitignore` syntax
`.gitignore` files use globbing patterns (a simplified version of regular expressions) to determine which files and directories Git should ignore.

* **`#` (Comments):** Lines starting with `#` are treated as comments and ignored.
* **`/` (Directory separator):**
  * **Leading slash (`/`):** Anchors the pattern to the root directory where the `.gitignore` file lives. For example, `/logs.txt` ignores `logs.txt` in the root, but not `subfolder/logs.txt`.
  * **Trailing slash (`/`):** Tells Git to match only directories, not files. For example, `build/` ignores the `build` folder and everything inside it.
  * **No slash:** Matches files or directories with that name anywhere in the repository. For example, `debug.log` matches `debug.log` in the root or in any subfolder.
* **`*` (Wildcard):** Matches zero or more characters within a single path segment (it will not cross directory boundaries `/`). For example, `*.log` matches `app.log` and `error.log`.
* **`**` (Recursive Wildcard):** Matches zero or more directories, allowing patterns to cross directory boundaries:
  * **Leading `**/`:** Matches in any directory. For example, `**/logs` matches `logs` anywhere in the project.
  * **Trailing `/**`:** Matches everything inside a directory. For example, `abc/**` matches all files inside `abc`.
  * **Middle `/**/`:** Matches zero or more intermediate directories. For example, `a/**/b` matches `a/b`, `a/x/b`, or `a/x/y/b`.
* **`?` (Single character):** Matches exactly one character (excluding `/`). For example, `cat?` matches `cats`, but not `cat` or `catch`.
* **`[]` (Character Sets):** Matches a single character from a specified set or range:
  * `[a-z]` matches any lowercase letter.
  * `[0-9]` matches any single digit.
  * `[aeiou]` matches any vowel.
* **`!` (Negation):** Re-includes a file that was previously ignored by an earlier rule. For example: `*.log; !important.log`. Note: You cannot re-include a file if its parent directory is already ignored).

# Overview

```
Your files
    │
    ▼
Working directory (working tree; the actual files you're editing)
    │
    │ git add
    ▼
Staging area (index; "this is what I want to include in my next commit")
    │
    │ git commit
    ▼
Local repository (the history stored by Git on you computer)
    │
    │ git push
    ▼
Remote repository (usually GitHub repository, usually stored on a different machine)
```

Git is a tool for tracking (keeping track of) changes made in your project.

A local Git repository is initialized by adding a special hidden directory `.git` to the root of your project. This directory constains the information that Git needs to track the project. You don't manually modify it. Instead, you interact with it through Git commands.

File tracking dictates whether Git actively monitors a file for changes and records its history. Tracked Files are files that Git knows about and keeps a full version history of them. Untracked Files are files that have never been added to Git or files whose version history is not recorded.

Not all files should be tracked. To specify which files should be ignored by Git, a `.gitignore` file is used.

Version history is made of snapshots of your project's contents at particular points in time. You can decide what files to include in the next snapshot by adding (staging) them to Git's temporary staging area. This operation is called `add`. If you change your mind, you can remove (unstage) some of those files from the staging area if you decide that you do not want to include them in the next snapshot. When you create a snapshot, the staged files are cleaned from the staging area and their current state is saved in the version history. A snapshot is called a revision or a commit. Each commit has a unique identifier called a hash. Consecutive commits show what files were changed and how they were changed. After saving a particular commit, i.e. after performing the operation `commit`, you can modify a file and see the difference between the current file's modification and the most recent committed version of this file. From any given commit the entire project codebase at the corresponding point in time can be reconstructed.

Commiting changes usually means storing the changes in your local repository, i.e. on your local disk. It is common to use another repository as a backup repository (for one developer) or as the central repository (for teams consisting of many developers). Such repository is called a remote repository and it stores the copy of your local repository. Both local and remote repository should be in general synced with each other in some way. Remote repository is also called `origin` (it is just a conventaional nickname). Remote repositories are most often repositories stored on platforms like GitHub or GitLab, each platform having its own set of servers. But a remote repository does not have to be on another machine. You can e.g. clone a project from a local folder into another folder and then you can push changes from the new folder back to the original folder.

The operation of pushing commits from local repository to remote one is called `push`.

The operation of fetching commits from remote repository into local one is called `fetch`. This operation will download all new commits, branches, and updates from the remote repository to your local repository, but it will not touch your working tree or current code, i.e. your files will stay untouched but Git will be able to tell you for example that your local branch is several commits behind/ahead the remote one. If you want to download all updates and immediatelly integrate them into your project, i.e. change your files, the operation that you should use is called `pull`. The `pull` operation is a shorthand for the `fetch` operation followed immediatelly by the `merge` operation, where `merge` operation is just the operation of integrating the downloaded updates into your current project (your current branch).

When creating commits one can think of it as creating a timeline of the project. Such timeline can be viewed as a branch with some logical, consecutive flow of commits which start at some point in time and ends at some another point. The original branch of the project (where usually all production code and all main commits are stored) is called `main` or `master`. You can create new branches off the main branch by marking the start of a new branch at any place on the main branch, i.e. at any commit. You can also create new branches off any other branches. By creating a new branch you essentially create a new, independent, logical timeline (or subtimeline) of the project which can be used to implement and test some new, experimental feature, for example. After this new feature has proved to be working on the new branch, the commits from the new branch can be merged (integrated) into the main branch so that the main branch is aware of the new feature. After the new feature has been added, its corresponding branch can be deleted. Or, if the feature turns out to be a flop, its corresponding branch can be safely removed without affecting the main branch.

You can of course move around and inspect all your commits and branches. This is why Git has to know where in the timeline you are right now. The pointer (marker) that shows where you are right now in your Git timeline is called `HEAD`. It usually points to the current active branch which in turn points to its latest commit. You can change what `HEAD` points to to move around your project's history. The operation of moving `HEAD` around, e.g. to switch between branches or inspect older commits, is called `checkout`.

> [!NOTE]
> Formally, branch is nothing more than a simple label, a textfile.

> [!NOTE]
> Tip (of some branch) is the last commit or the most recent commit on a branch (basically it points to the most up to date code in the branch).

> [!NOTE]
> The base of a branch is the specific commit where it originally split off from another branch (like main/master). For main/master the base is just the first commit created.

> [!NOTE]
> Rebasing is the operatoin of changing the base of one branch to a new commit; it can simulate for example that you start building a new feature from the most recent code version instead of from some older version of your project. In other words: "Take my commits and pretend I made them starting from the other branch/commit."

# Merge conflicts and advanced merges
This is all related to the `merge` operation. A merge conflict happens when Git cannot automatically determine which changes to keep — usually when two branches modify the exact same line of a file in different ways. You usually have to resolve merge conflicts manually, i.e. by opening the files of interest and manually choosing the correct modifications. After that the operation can be finalized by adding and committing the resolved files.

There are four ways to merge commits from one branch (usually a feature branch) to another branch (usually the main branch):

1. Fast-Forward Merge
   * A Fast-Forward merge is the simplest type of merge in Git; it happens automatically when you try to merge Branch B into Branch A, and Branch A has no new commits since you originally created Branch B.
   * Because there are no competing changes on Branch A, Git doesn't need to combine any code; instead, it simply slides forward the branch pointer of Branch A to point to the newest commit on Branch B.
2. Standard Merge
    * This option takes all commits from your feature branch and joins them into the main branch by creating a brand-new merge commit.
    * It preserves every single commit you made on your feature branch exactly as it was, plus adds one extra "Merge PR #..." commit to tie the two branches together.
    * It can make your graph history look cluttered and non-linear but it is the default option.
3. Squash Merge
   * This option combines all the commits from your feature branch into one single commit before applying it to the main branch.
   * Git takes the total difference between feature branch and main branch, squashes all ~5, 10, or 20 WIP (Work in Progress) commits into a single new commit, and places that single commit on main branch.
   * You loose the step-by-step history of the changes when using this option.
4. Rebase Merge
   * This option takes each individual commit from your feature branch and replays them one by one onto the tip of the main branch.
   * It moves the base of your feature branch to the latest commit of main, creating a perfectly linear, straight-line history without adding an extra merge commit.
   * When feature branch is rebased onto the main branch, it can be simply merged into the main branch by fast-forwarding.
   * Note that a rebased `commit A` from `Branch A` becomes `commit A'` after rebasing it onto the main branch, i.e. Git doesn't merely copy the commits, it creates new ones (but representing the same changes), based on the original ones (but with different parents).

# Upstreams (tracking references)

Git lets you choose a name for a local branch that is the same as one used in a remote repository, without having known about the other one, such that they have completely different work on them. Git lets you do this, but it also provides a way to link local references to remote ones as well. A local branch can track a remote branch, which means that push and pull commands will know to push and pull commits to and from the tracked branch by default. Also `status` will tell you the status between your current local branch and the remote branch it's tracking, e.g. how many commits behind/ahead you are. When you clone a Git repository, Git will add a tracking reference to the local master branch to track the remote master branch. When you checkout from a new remote branch, Git will add a tracking reference to the created local branch to track the remote branch you checked out. However, if you create a new branch locally, and then push it to the remote repository, you have to explicitly tell Git if you want your local branch to start tracking the new remote branch. You do that with the `-u` or `--set-upstream` option when pushing the local branch to the remote repository. This is also referenced to as "adding a tracking reference". Equivalently, you can also hear that the remote branch "is the upstream with respect to" the local branch.

# Undoing changes

Undoing changes in Git is done mostly by two fundamentally different operations: `reset` and `revert`. Use `reset` for private, local work that has not yet been pushed to a remote server. Use `revert` for commits that have already been pushed to public/shared remote branches.

`reset` should be used on local changes, i.e. changes not shared with others. It alters where `HEAD` points (moves `HEAD` to a different commit) and can modify your staging area and files depending on the mode used (`--soft`, `--mixed` or `--hard`).

```
--soft
    commit moves
    staging stays
    files stay

--mixed (default mode)
    commit moves
    staging changes
    files stay

--hard
    commit moves
    staging changes
    files change
```

`reset` discards local commits. This allows you to for example redo a commit with a different commit message, squash multiple commits into one new commit, or completely discard some local changes. Note that this operation does not discard remote commits after they have already been pushed to the remote repository.

`revert`, on the other hand, is a safe, additive command. Instead of erasing commits, Git calculates the exact opposite changes of the chosen commit and applies those changes as a new commit which essentially undoes the chosen commit while still preserving the entire history of commits. This allows you to for example undo changes made by your last commit, or some past commit, or by a range of commits.

| Feature | `reset` | `revert` |
| --- | --- | --- |
| Primary Action | Rewrites history by moving `HEAD` backward | Preserves history by adding a new offsetting commit |
| Public Branches (`main`, `dev`) | Unsafe (causes conflicts for teammates who pulled the old history) | Safe (standard workflow for shared remote branches) |
| Risk Level | High (using `--hard` can lose uncommitted work) | Low (no code or history is destroyed) |
| Reflog Recoverability | Yes (using `HEAD@{n}`) | Yes (normal commit navigation) |

# Contributing to open source projects

There are two primary operations that allow developers to contribute to open source projects: `fork` and `clone`.

--- 

* Forking: creating a personal copy of someone else’s repository on the remote platform (e.g., under your GitHub account).

* Cloning: downloading a copy of a repository from the remote server onto your local computer.

---

1. Fork the Repository
   * Performed on GitHub/GitLab UI. Go to the repository page you want to work with on the web interface. Click the **Fork** button in the top right corner. This creates an exact copy of their repository under your account.

1. Clone Your Fork
   * Terminal command. Copy the URL of your forked repository and run the clone command in your local terminal.

2. Make Local Changes safely
   * Local edits. Open the files in your editor, edit them, or create new ones. You can stage, commit, and reset freely.

1. Push to Your Remote Fork
   * Terminal command. Send your local updates back to your remote copy (this is your remote copy, not the original repository belonging to someone else).

1. Propose Changes via Pull Request
   * Optional. If you want the original owner to adopt your changes, open a Pull Request (PR) from your forked repository page on GitHub.

---

* No Push Access: You cannot push directly to a repository you don't own unless the owner explicitly grants you write permissions.
* Pull Requests are Gatekept: A Pull Request is merely a request ("Hey, take a look at my code"). The repository maintainer has full control to accept, request changes, or reject it entirely.
* Local Experiments are Disposable: If you make a complete mess of your local repository, you can delete the folder on your computer, clone your fork again, and start fresh in seconds.

--- 

> [!NOTE]
> Is it possible to have nested repositories, for example your own repository and someone else's repository that you cloned inside your repository; it is not recommended to have nested repositories though as this can confuse Git; instead you can for example download-extract other repo's raw files using zip.

> [!NOTE]
> If you clone someone else's repository, edit it and try to push changes, Git will block you (unless the author has granted you access to this repository).

> [!TIP]
> If you want to preview a pull request someone else created on your project, you can create a pointer to the contributor's fork repo with `git remote add <some_name> <.git_contributor_url>`, fetch their branch with `git fetch <.git_contributor_url>`, checkout to that branch, run the tests on that branch, and delete the branch after you are done.

# Stash and worktrees

Git also has an operation called `stash`. It can be used when you are working on a specific branch and suddenly you have to checkout to a different branch to work there but you are still not fully done with your changes on your current branch and you are not ready to make a commit yet. In such case you use `stash` to save your WIP changes on a stack of unfinished work. When you are done working on the different branch and switch back to your previous branch, you can simply pop your previously saved changes from the stack and continue your work from there. `stash` can therefore be viewed as a temporary clipboard for your unifinished changes.

One more thing worth mentioning are worktrees. You manage them with the `worktree` operation. Normally when you work you work at one branch at a time and when a sudden situation appears at another branch (such as an urgent bug fix at another branch) you have to either stash your current changes or completely clone the entire repository to tackle the issue at another branch without losing your current work. This may involve a lot of Git commands and waste of time and disk space. Worktrees make it easier. Worktree is defined in Git as an object which is basically a working tree with some additional metadata information attached to it. Normally when you work, you work on the main worktree created by the `init` or the `clone` operation. You can create a new worktree beside the main worktree. Such new worktree is called a linked worktree. This new worktree allows you to work in parallel on two different branches, in two different editor windows, at the same time, on the same machine. This may be used instead of stashing your current changes to temporarily work on another branch. You can have many active worktress and work essentially on several branches at the same time. All changes made in different worktrees will be immediately visible to all other worktrees. In practice, a new worktree is just a directory containing the copy of your original repository which is pinpointed at the specific branch and  the specific commit that you used to create the worktree.

> [!NOTE]
> To prevent data corruption, Git does not allow you to be on the same branch at the same time in two different worktrees.

To summarize, Git worktree allows you to check out multiple branches of the same repository simultaneously into separate directories on your filesystem. Instead of cloning the repository multiple times (which wastes disk space and requires separate `fetch` operations), all worktrees share the same underlying `.git` directory and commit history.

| Scenario | How Worktrees Help |
| --- | --- |
| Hotfixes & Urgent Requests | Instead of stashing changes and switching branches on your working directory, open a new worktree in a separate folder, fix the bug, push, and delete the worktree. Your main work remains untouched. |
| Comparing & Testing Branches | Run two branches side-by-side (e.g., frontend server on branch A, backend on branch B, or testing UI differences) without re-running `npm install` or rebuilding assets every time you switch. |
| Long-Running Code Reviews | Check out a pull request into its own worktree to test and run the code locally while keeping your active feature branch open in your IDE. |
| Multi-Branch Operations | Perform time-consuming builds, benchmark tests, or database migrations on one branch in the background while continuing active development in another directory. |

# Cherry pick and bisect

Another useful operation is `cherry-pick`. This operation applies the changes introduced by one or more existing commits from another branch onto your current working branch, creating brand-new commits with new commit hashes. It does not apply all commits from another branch, just the ones you pick. Common use cases include hotfixing production with a fix sitting in a feature branch, pulling specific bug fixes without merging an unstable branch, or rescuing specific work from abandoned branches.

`bisect` is a less frequent but still useful operation. It helps you pinpoint the commit that introduced a bug. It does that using binary search instead of linear search. It asks you whether the current commit is good or bad. Then it asks you to pick other past commit as either good or bad. Then again and again until it finds the only one that remains. Each iteration halves the interval of commits to inspect. Assumption is that there is only one "bad" commit and all commits before this one are "good" and all commits after this one are also "bad".

---

> [!WARNING]
> ### The rest of the sections are either about advanced, theoretical or low-level concepts.

---

# Commit messages
A commit should represent one logical change. Useful rule: "someone reading your Git history should understand what happened without opening every file". This is why commit messages, which describe commits, are so important.

Most important conventions regarding commit messages:
- short and concise,
- 50-70 characters max,
- imperative mood ("Add feature" instead of "Adding feature" or "Added feature"),
- no period at the end,
- capitalization of the first letter.

Some teams use conventions for formatting commit messages. Conventional commits are in the form `<type>(<scope>): <short summary>`, e.g. `refactor(db): Refactor methods with too long parameter lists`. Here, `refactor()` is the keyword. In the table below you can see some other useful keywords.

| Type     | When to Use                                                    | Example                                      |
|----------|----------------------------------------------------------------|----------------------------------------------|
| `feat`   | Adding a new user-facing feature                               | `feat(auth): Add Google OAuth2 login option` |
| `fix`    | Resolving a bug or error                                       | `fix(checkout): Prevent duplicate charging on submit` |
| `docs`   | Documentation changes only                                     | `docs(readme): Add setup instructions for Docker` |
| `refactor` | Code changes that neither fix a bug nor add a feature        | `refactor(db): Optimize user query performance` |
| `style`  | Formatting, missing semicolons, line endings (no code logic changes) | `style(api): Format response handlers with Prettier` |
| `test`   | Adding missing tests or refactoring existing ones              | `test(cart): Add unit tests for discount calculation` |
| `chore`  | Build tasks, package manager configs, non-code maintenance     | `chore(deps): Update React to v19.0.0` |

# Non-Bare Repository vs Bare Repository

## Non-Bare Repository (Default)

When you initialize a repository with `git init` or clone a repository from GitHub, you create a non-bare repository.

* Structure: Consists of a working directory (your project files) plus a hidden `.git` folder containing history and tracking metadata.
* Purpose: Built for active editing, staging files, creating branches, and running code locally.
* Rule: You can make direct changes to files and create commits inside it.

```text
my-project/             <-- Working Directory (Editable Files)
├── index.html
├── app.js
└── .git/               <-- Repository Metadata
    ├── HEAD
    ├── objects/
    └── refs/
```

## Bare Repository (`--bare`)

A bare repository is initialized using the `git init --bare` flag. It contains no working directory — only the contents of what would normally be inside a `.git` folder.

* Structure: Contains raw Git metadata (`objects`, `refs`, `HEAD`, `config`), but no source code files to view or edit directly.
* Purpose: Serves as a centralized "hub" or central remote server (e.g., GitHub and GitLab use bare repositories on their backends) to receive and distribute code.
* Rule: You cannot edit code or run `git commit` inside a bare repository. You can only push to it (`git push`) or pull from it (`git pull`).

```text
my-project.git/         <-- No Working Directory (Bare)
├── HEAD
├── config
├── description
├── hooks/
├── info/
├── objects/
└── refs/
```

## Why Bare Repositories Exist

If you try to `git push` code into a non-bare repository's active branch, Git will block you by default. Pushing updates directly to a working directory where someone else might be editing files causes file corruption and merge conflicts. Bare repositories prevent this because they have no working directory to conflict with incoming pushes.

## Key Comparison

| Feature | Non-Bare Repository | Bare Repository |
| --- | --- | --- |
| **Creation Command** | `git init` | `git init --bare` |
| **Has Working Directory?** | Yes (editable source files) | No (only Git tracking files) |
| **Primary Use Case** | Local development and editing | Central remote server / hub |
| **Pushed To Directly?** | No (blocked by default) | Yes (designed for `git push`) |
| **Folder Naming Convention** | `project-name` | `project-name.git` |

# Merge commit

> [!NOTE]
> Parent commit of commit A is the commit that commit A is based on and this relationship can be visualized by a graph of timelines.

Now, suppose we have `A → B → C` and you create a branch at B:

```
        C
       /
A → B
       \
        D → E
```

There are now two lines of development: C is the next commit on main and D → E are commits on feature.

Now you do: 

```
git switch main
git merge feature
```

Git creates a merge commit:

```
        C ─────┐
       /       │
A → B          M
       \       │
        D → E ─┘
```

M has two parents:

```
M
├── parent 1: C
└── parent 2: E
```

Why?

Because M combines two histories:

```
main history:     A → B → C
                           \
                            M

feature history:  A → B → D → E
                           /
                          M
```

The merge commit needs to record: "This commit combines the work that came from C and the work that came from E." Therefore it points backward to both C and E. That's what makes it a merge commit.

Git usually assigns numbers to the parents of each merge commit. It does it based on the merge operation. In the usual situation you merge a feature branch into the main branch and in this case the main branch (i.e. the current branch) is usually `parent 1` while the feature branch is `parent 2` and both parents are thus the most recent commits from either the main branch or the feature branch.

The Git needs to know which parent of a merge commit is the mainline parent in order to perform the revert operation of this merge commit. If you tell Git that `parent 1` is the mainline parent, you're essentially telling Git: "For the purpose of this reversal, consider `parent 1` to be the mainline." Git then asks: "What changes did the merge bring to `parent 1` from the other branch?" and creates a new commit that reverses those changes to perform the revert operation.

# 2-way and 3-way merges

A 2-way merge and a 3-way merge describe the algorithm Git uses behind the scenes to compare files and combine changes when performing a merge.

## The 2-Way Merge (The Old / Naive Way)

A 2-way merge compares only two snapshots:

1. The target branch file (e.g., `main`).
2. The incoming branch file (e.g., `feature`).

### The Problem with 2-Way Merging

Because a 2-way merge only looks at the two current versions, it has no memory of what the file looked like before the branches split. If a line of code is different between Branch A and Branch B, a 2-way merge cannot know who changed what, or if both people changed it.

Suppose Branch A has `color: blue` and Branch B has `color: green`.

* A 2-way algorithm sees `blue` vs. `green`.
* It cannot tell whether Branch A changed red to blue, or Branch B changed red to green, or both changed it at the same time.
* Result: it must raise a merge conflict every single time lines differ, forcing human intervention even for simple, non-overlapping updates.

## The 3-Way Merge (How Git Actually Works)

A 3-way merge solves this problem by using three snapshots instead of two:

1. Target Branch (`OURS`, e.g., `main`).
2. Incoming Branch (`THEIRS`, e.g., `feature`).
3. Common Ancestor (`BASE` — the exact commit where the two branches originally split apart).

By comparing both branches back to their common ancestor (`BASE`), Git can automatically determine who made which changes.

### How the 3-Way Logic Works

| `BASE` (Ancestor) | `OURS` (`main`) | `THEIRS` (`feature`) | Git's Automatic Decision |
| --- | --- | --- | --- |
| `color: red` | `color: red` | `color: green` | Keep `green`. (Only `feature` modified this line; `main` left it alone.) |
| `color: red` | `color: blue` | `color: red` | Keep `blue`. (Only `main` modified this line; `feature` left it alone.) |
| `color: red` | `color: blue` | `color: green` | Conflict! (Both branches modified the exact same original line differently.) |
| `color: red` | `color: red` | `color: red` | Keep `red`. (Neither branch touched it.) |

---

## How This Relates to common merge types

* **Fast-Forward Merge:** No 3-way calculation is needed because `main` hasn't changed since `BASE`. Git just slides the pointer.
* **Standard Merge:** When `main` and `feature` have both moved forward, Git executes a 3-way merge using the common ancestor, automatically applying clean non-overlapping changes, and creates a merge commit with two parents.
* **Squash Merge:** Uses a 3-way merge behind the scenes to calculate the combined difference between your feature branch, the target branch, and their common ancestor. The only difference is that instead of saving a merge commit with two parent histories, Git simply applies that final 3-way result as a single brand-new commit on the target branch.
* **Rebase Merge:** Replay-based. For every single commit being rebased, Git internally performs a 3-way merge between the patch, the current base, and the parent commit to apply changes sequentially.
  * Reminder - Rebase Merge does create new commits.
  * Git recreates/replays the commits from one branch on top of a new base. For each commit, Git determines the changes introduced by that commit relative to its parent and attempts to apply those changes to the new base (using Git's merge machinery, with conflicts possible). Each successfully replayed commit becomes a new commit with a new parent. After all commits have been recreated, the branch reference is moved to the new tip, which can be a fast-forward.
  * The final branch movement can be a fast-forward — but the 3-way merge machinery is relevant during the replay of each commit, not during that final branch movement.

# Detached HEAD

## What Does "Detached HEAD" Mean?

In Git, `HEAD` is a pointer that tracks what you are currently looking at in your repository.

* Normal state: `HEAD` points to a branch name (like `main` or `feature`), which in turn points to the latest commit on that branch. When you make a new commit, both the branch and `HEAD` move forward together.
* Detached HEAD state: `HEAD` points directly to a specific commit hash (or tag) instead of pointing to a branch name.

```
NORMAL STATE:
HEAD ---> main ---> Commit C (new commits update both HEAD and main)

DETACHED HEAD STATE:
HEAD -------------> Commit B (new commits move HEAD, but NO branch points to them!)
          main ---> Commit C
```

When you are in a detached HEAD state, Git still allows you to edit files and make new commits. However, because no branch name is attached to those commits, they are not saved to any branch. If you switch to another branch without fixing it, those new commits can become orphaned and eventually deleted by Git's garbage collection.

## Why Did You Enter Detached HEAD?

You usually enter a detached HEAD state when you:

1. Checked out a specific commit hash directly: `git checkout a1b2c3d` or `git switch --detach a1b2c3d`.
2. Checked out a remote tracking branch directly: `git checkout origin/main`.
3. Checked out a tag or sub-release: `git checkout v1.0.0`.
4. Rebased a branch and hit a conflict mid-process.

## How to Fix It (Based on What You Want to Do)

Check your status first by running `git status`.

### Scenario A: You just explored and made NO changes (or want to throw away changes)

If you just checked out an old commit to look around and haven't made any commits you want to keep, simply switch back to your normal branch using `git switch`.

### Scenario B: You made new commits while detached and WANT TO KEEP THEM

If you made one or more commits in this state, you can preserve them by attaching a new branch name to your current position right now.

```bash
# Create and switch to a new branch at your current commit
git switch -c my-saved-work

# (Or legacy command: git checkout -b my-saved-work)
```

Now your new commits belong to `my-saved-work`. You can keep working on this branch or merge it back into `main` using standard Git commands.

### Scenario C: You already navigated away and "lost" the commits you made

If you accidentally ran `git switch main` while in a detached HEAD state, Git printed a warning with the commit hash of your lost work.

If you didn't copy that hash, you can find it using Git's history log (`reflog`):

```bash
# Look at your action history
git reflog
```

Look for the commit message you made before leaving detached HEAD (e.g., `e4f5g6h HEAD@{1}: commit: My important work`).

```bash
# Turn that commit into a permanent branch
git branch recover-my-work e4f5g6h

# Switch to your recovered branch
git switch recover-my-work
```

# Log vs Reflog

| Feature | `git log` | `git reflog` (`HEAD@{n}`) |
| --- | --- | --- |
| **Scope** | Shared commit history (pushed/pulled with remote) | Local-only history of your local actions |
| **Tracks** | Commit ancestry graph | Physical movement of `HEAD` over time |
| **Persistence** | Permanent part of the repository | Exists temporarily (typically pruned after 90 days) |

# Log vs Show vs Diff

The main difference between `git log`, `git show`, and `git diff` comes down to scope and purpose:

* `git log` is an overview of history (lists commits over time).
* `git show` is a detailed snapshot of a single object (inspects one specific commit and its changes).
* `git diff` is a comparison tool (shows file differences between two points in time or states).

| Command | Primary Focus | What It Takes as Input | Primary Output |
| --- | --- | --- | --- |
| `git log` | History / Timeline | Range of commits (or default branch) | List of commit metadata (hash, author, message) |
| `git show` | Individual Commit / Object | A single commit hash or ref (default: `HEAD`) | Metadata + exact code changes made in *that specific commit* |
| `git diff` | Comparison | Two arbitrary targets (files, commits, or branches) | Raw line-by-line additions and deletions between the two states |

# HEAD@{n}  vs  HEAD~n  vs  HEAD^n

## HEAD@{n}

`HEAD@{n}` refers to an entry in your Git reflog (reference log). While `HEAD` points to the tip of your current branch, `HEAD@{n}` tells you where `HEAD` was pointing $n$ updates ago on your local machine.

* **`HEAD`**: A pointer to your current branch and commit.
* Reflog: A private, local diary that records every time `HEAD` changes position (e.g., when you commit, checkout a branch, rebase, reset, or pull).
* **`HEAD@{0}`**: Where `HEAD` is right now.
* **`HEAD@{1}`**: Where `HEAD` was immediately before the last action.
* **`HEAD@{5}`**: Where `HEAD` was 5 actions ago.
* **`HEAD@{10 minutes ago}`**: Where `HEAD` was 10 minutes ago (you can use time-based syntax too).


Common use case:

* Recovering "Lost" Commits or Undoing a Bad Reset. If you accidentally run `git reset --hard HEAD~3` and lose commits, they aren't gone immediately. Look up where you were before the reset in `git reflog` (e.g., `HEAD@{1}`), and restore it:
```bash
git reset --hard HEAD@{1}
```

## HEAD~n

`HEAD~` is a shortcut in Git used to navigate backward through parent commits in your commit history. While `HEAD@{}` looks back at your action history (where you were locally), `HEAD~` looks back at the commit ancestry tree (the actual chain of commits).

The tilde symbol (`~`) means "go back $n$ generations along the current commit path". For different branches the same $n$ can yield different commits because each branch can be viewed as a separate timeline.

* **`HEAD`**: Your current commit.
* **`HEAD~`** (or **`HEAD~1`**): The immediate parent of your current commit (1 step back).
* **`HEAD~2`**: The grandparent commit (2 steps back).
* **`HEAD~3`**: The great-grandparent commit (3 steps back).

Common use cases:

* Undoing the Last Commit (Keep Your Code). If you committed too early or forgot to include a file, move `HEAD` back 1 commit while leaving your file changes intact in your workspace:
```bash
git reset HEAD~1
```

* Viewing an Older Commit. See what changed 2 commits ago without switching branches:
```bash
git show HEAD~2
```

Quick rule of thumb: Use `HEAD~n` when you want to move back $n$ steps in straight line history.

## HEAD^n

`HEAD^` is a shortcut used to select which parent of a merge commit to follow. While `HEAD~` walks straight back through time (1st parent, 2nd grandparent, etc.), `HEAD^` moves sideways across branches at the point where two branches merged together. Usage of `HEAD^` is realtively rare because `HEAD~` always chooses the first parent of each merge commit which is what you usually want, but, still, `HEAD^` is useful to know.

> [!NOTE]
> Sometimes `^` can be treated as an escape character in your terminal which will make Git not understand simple commands such as `git show HEAD^2`. To overcome this issue use double quotes `"`, e.g. `git show "HEAD^2"`.

A standard commit has 1 parent. A merge commit has 2 or more parents because it combines two branches.

* `HEAD^` (or `HEAD^1`): The 1st parent commit (the branch you were standing on when you ran `git merge`).
* `HEAD^2`: The 2nd parent commit (the branch that got merged in).
* `HEAD^3`: The 3rd parent commit (only applies to rare "octopus" merges of 3+ branches).

Common use cases:

* Inspecting What Was Merged In. If you just completed a merge onto `main` and want to inspect the tip of the feature branch that was brought in, view `HEAD^2`:
```bash
git show HEAD^2
```

* Diffing Against the Merged Branch. To see all changes introduced specifically by the incoming branch during a merge:
```bash
git show HEAD^1..HEAD^2
```

* Restoring State Before a Merge. If a merge caused unintended conflicts or issues and you want to point your workspace back to the state of `main` right before the merge:
```bash
git reset --hard HEAD^1
```

## Summary Comparison

You can chain these symbols together to navigate anywhere in a commit graph:

* `HEAD^2~2`: Go to the 2nd parent of a merge commit, then step back 2 generations down that branch line.
* `HEAD~2^2`: Go back 2 commits along the current line, then select the 2nd parent of that commit.

| Concept | What it tracks | Key Question It Answers |
| --- | --- | --- |
| `HEAD@{n}` | Local action history (Reflog) | *"Where was I working 10 minutes ago?"* |
| `HEAD~n` | Direct line ancestor generations | *"What was the commit 3 steps back on this branch?"* |
| `HEAD^n` | Alternate parent branches at a merge point | *"Which branch was merged into this commit?"* |

# Operators - `..` vs `...`

## The Double-Dot Operator (`..`)

The `..` operator selects commits reachable from the second point, but NOT from the first point.


```bash
git log A..B
```

"Show me everything in commit B that is not in commit A."

Common use cases:

1. Previewing Unpushed Commits:
See what you have committed locally that hasn't been pushed to the remote branch yet:
```bash
git log origin/main..main
```

2. Reviewing Incoming Updates:
See what changes exist on the remote branch that you haven't merged into your current branch yet:
```bash
git log main..origin/main
```

Omitting `HEAD`:
* If you leave off one side, Git defaults to `HEAD`:
  * `git log origin/main..` means `origin/main..HEAD` (local commits not on remote).
  * `git log ..origin/main` means `HEAD..origin/main` (remote commits not on local).

## The Triple-Dot Operator (`...`)

The `...` operator behaves differently depending on whether you are using it with `git log` or `git diff`.

### Behavior in `git log` (Symmetric Difference)

In `git log`, `A...B` selects commits that are reachable from either `A` or `B`, but NOT from both. It isolates the unique work done on both branches since they diverged.

```text
C1---C2---C3  (Branch A)
       \
        D1---D2  (Branch B)
```

* `git log A...B` yields: `C3`, `D1`, and `D2` (ignoring the common history `C1` and `C2`).

Adding `--left-right` clarifies which commit belongs to which side:

```bash
git log --left-right A...B
```

* `< C3` means it belongs to A; `> D1` means it belongs to B.

### Behavior in `git diff` (Common Ancestor Diff)

In `git diff`, `A...B` compares the tip of `B` with the common ancestor (merge base) of `A` and `B`.

* `git diff main feature` compares `main` and `feature` directly, including any new changes made on `main`.
* `git diff main...feature` shows only the changes introduced on the `feature` branch since it originally branched off `main` (ignoring new commits on `main`).

## Summary Matrix

| Command | Query / Meaning |
| --- | --- |
| `git log A..B` | What commits are in `B` that are NOT in `A`? |
| `git log A...B` | What commits are unique to `A` OR `B` (excluding shared history)? |
| `git diff A..B` | What is the total file difference between state `A` and state `B`? |
| `git diff A...B` | What changes did `B` introduce since it branched off from `A`? |

# Tags and releases

Git tags act as permanent bookmarks attached to specific commits in your repository history. Then, GitHub's releases wrap those tags in user-facing distribution packages.

* Git Tag: A core Git feature. It points to a specific commit SHA (e.g., `v1.0.0`). Unlike branches, tags do not move as you make new commits.
  * Lightweight Tag: A simple pointer to a commit (like a branch that doesn't move).
  * Annotated Tag: A full Git object containing tagger name, email, date, GPG signature, and a tagging message. Recommended for production software releases.


* GitHub Release: A GitHub-specific wrapper around a Git tag. It adds a UI layer with markdown release notes, user download links (`.zip`/`.tar.gz`), attached binary assets (executables, compiled `.apk`/`.exe` files), and pre-release flags.

Most teams follow Semantic Versioning (SemVer) for tag names: `vMAJOR.MINOR.PATCH` (e.g., `v2.1.4`).

* MAJOR: Breaking changes.
* MINOR: New backward-compatible features.
* PATCH: Backward-compatible bug fixes.

In real software development, you often need to release a critical hotfix to production (`v1.0.1`) while your main branch contains unfinished features for the next release (`v1.1.0`).

| Scenario Step | Command / Action | Purpose |
| --- | --- | --- |
| **1. Checkout Tag** | `git checkout -b hotfix-v1.0.1 v1.0.0` | Creates a new branch off the published `v1.0.0` tag. |
| **2. Apply Fix** | Fix the bug, `git add .`, `git commit -m "Fix: Critical crash"` | Resolves the issue on the isolated hotfix branch. |
| **3. Tag Hotfix** | `git tag -a v1.0.1 -m "Hotfix release v1.0.1"` | Creates the new patch version tag. |
| **4. Deploy & Merge** | `git push origin v1.0.1`, `git checkout main`, `git merge hotfix-v1.0.1` | Deploys the fix and backports changes to main line. |

# Hooks

**Hooks** are custom scripts which fire off when certain important actions occur.

**Pre-commit hooks** are automated scripts that execute every time you run `git commit`, right before Git saves your changes. If any hook checks fail—such as an unformatted file, a trailing space, or a syntax error—Git cancels the commit so you can fix the issue locally before pushing code to your repo.

While Git natively supports custom shell scripts inside `.git/hooks/`, managing them across multiple developer machines is tricky. The Python ecosystem solves this with **`pre-commit`**, a multi-language package manager dedicated to configuring, installing, and running hooks via a simple YAML config file, `.pre-commit-config.yaml`.

When you run the `pre-commit install` command, it writes a small script into your repository's hidden `.git/hooks/pre-commit` file.

Once that script is in place:

* Git automatically triggers `pre-commit` every single time you execute `git commit`.
* It automatically creates and manages isolated environments for all the tools (like Ruff) listed in your `.pre-commit-config.yaml`.

| Scenario | What to Run | Why |
| --- | --- | --- |
| **Cloning a repo to a new machine/folder** | `pre-commit install` | `.git/hooks/` is ignored by Git, so each clone/developer needs to link it once. |
| **Edited `.pre-commit-config.yaml`** | *Nothing!* | Pre-commit detects changes and downloads new hook environments automatically on your next `git commit`. |
| **Updating hooks to newer versions** | `pre-commit autoupdate` | Updates the `rev:` tags in `.pre-commit-config.yaml` to the latest releases. |
| **Testing hooks without committing** | `pre-commit run --all-files` | Manually runs all hooks across the whole codebase immediately. |

To skip hooks temporarily during a certain commit, run `git commit -m "Message" --no-verify`.

> [!TIP]
> The best use case for pre-commit hooks is **detecting secrets** so that they are never leaked into the public repo upon committing new changes.

## Bonus: `detect-secrets`

An example tool to use as a pre-commit hook for detecting leaked secrets is the `detect-secrets` package. It blocks the commit if it detects that a potential secret might be exposed in the commit. It also provides a few other useful utilities.

Workflow:

* `detect-secrets scan > .secrets.baseline`
  * creates the `.secrets.baseline` file
  * this file stores the results of the scan that `detect-secrets` performs on the currently tracked files (files exposed to the version control system) to find all potential secrets that might be exposed/leaked in those files
  * this file contains candidates that `detect-secrets` found and considers them to be real secrets which shouldn't be exposed
* `detect-secrets audit .secrets.baseline`
  * audit each candidate in the `.secrets.baseline` found in the previous step
  * `detect-secrets` might incorrectly mark some non-secrets as real secrets so you have to manually approve each candidate that `detect-secrets` found
  * do it one-by-one by marking each candidate manually as either the true secret or as the false-positive
  * for example:
    * initial scan -> 10 potential secrets found
    * after manual audit -> 7 entries marked as false-positives and 3 entries marked as real secrets
* commit the `.secrets.baseline` to the version control system
  * committing this file allows every team member to see the current state of the repo, i.e. what things are considered to be potential secrets, how many among those are false-positives and how many among those are real secrets which are really exposed and need to be taken care of (e.g. by secret rotation)
* perform other work and commit it
  * don't forget to have `detect-secrets` set up as the pre-commit hook
  * `detect-secrets` will allow you to commit changes as long as during pre-commit hook it doesn't detect any NEW real secrets being leaked, i.e. any NEW secrets not currently stored in the `.secrets.baseline`
  * this allows the pre-commit hook to focus on detecting NEW secrets while the known ones are already recorded and stored in the `.secrets.baseline`
  * *this way, you create a separation of concern: accepting that there may currently be secrets hiding in your large repository (this is what we refer to as a baseline), but preventing this issue from getting any larger, without dealing with the potentially gargantuan effort of moving existing secrets away*
  * this also prevents `detect-secrets` from complaining about false-positives on every commit
* take care of each real secret stored in the `.secrets.baseline` file when you have time and possibility to do so
  * candidates marked by you as real secrets in the audit need to be taken care of eventually
  * for example, you choose one real secret entry from the `.secrets.baseline` and check in which file it is exposed, you open that file and remove the secret from that file and perform secret rotation to immediately invalidate that previously exposed secret
* `detect-secrets scan --baseline .secrets.baseline`, `detect-secrets audit .secrets.baseline`
  * after taking care of some of the real secrets, update the `.secrets.baseline` so that it reflects your updates
* commit the updated `.secrets.baseline` again
  * this way other team members will know that some real secrets have been taken care of and will see which still remain
* and so on...
