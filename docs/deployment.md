# Deployment channels (ADR-0008 N3)

Two deployment channels exist, one per protected branch, and both are
automatic: the merge itself is the deploy trigger, so a merged pull
request never waits for a manual staging step. The split follows the
branch model (ADR-0005): `daily` is the agent blast radius, `main` is
the human boundary, and the deployment channels mirror exactly that.

| Branch  | Channel  | Trigger                                | Human role             |
| ------- | -------- | -------------------------------------- | ---------------------- |
| `daily` | staging  | every merge into `daily` (the pull request flow) | tests the staging URL |
| `main`  | release  | every human merge of `daily` into `main` | owns the release |

## The workflow contract

`.github/workflows/deploy.yml` implements the trigger:

- it runs on every push of `daily` and `main`;
- it selects the channel from the branch name (`main` deploys to the
  release channel, `daily` to staging);
- it selects the target's GitHub environment the same way, so the two
  channels stay separable in protection rules and deployment history;
- it reads one set of secrets per channel and connects to the target
  host over SSH.

The template ships the connection smoke, not the distribution: the
remote command is deliberately a bare `true`, because a repository
instantiated from this template has no product code yet. An instance
(`tools/<tool>`, `src/` product code) replaces the smoke with its real
distribution step - an rsync of the working tree, an OCI image push,
a remote build - and records the choice in its own ADR; the per-repo
implementation principle is N8's.

## Secrets per channel

The secrets carry the target, one prefix per channel:

| Secret               | Meaning                            | Notes |
| -------------------- | ---------------------------------- | ----- |
| `STAGING_SSH_KEY`    | key the runner connects with       | dedicated per channel |
| `STAGING_HOST`       | staging host, currently the OVH VPS | |
| `STAGING_USER`       | user on the staging host           | a deploy user, not root |
| `RELEASE_SSH_KEY`    | private key for the release channel | |
| `RELEASE_HOST`       | release host                       | |
| `RELEASE_USER`       | user on the release host           | |

Both channels can point at the same VPS with different directories or
services; the separation lives in the secrets and the environments,
not in the workflow.

## Staging in the loop (N3)

The night loop's morning package (N3) assumes `daily` is deployed to
the staging URL with the candidate flags on there only: the
validation console (N8) sends the owner to staging to try the
scenarios. A staging deployment that drifted behind `daily` shows up
immediately there: the deep link of a scenario is a 404 or an old
shape. Keeping staging equal to `daily` is therefore a property of
this automatic deploy, not an audit item; the deployment history of the
`staging` environment is the log to consult when it is in doubt.

## Rollback

The deployment history of each environment keeps the deployed commit
SHAs; rolling back is a redeploy of the previous SHA (revert on
`daily` or `main`, then the trigger does the rest). The release
channel adds the human safeguard anyway: a human made the merge that
triggered it.
