We welcome contributions to the Ubuntu charm!

Before working on changes, please consider [opening an issue](https://github.com/canonical/charm-ubuntu/issues) explaining your use case. If you would like to chat with us about your use cases or proposed implementation, you can reach us at [Matrix](https://matrix.to/#/#charmhub-charmdev:ubuntu.com) or [Discourse](https://discourse.charmhub.io/).

# Pull requests

Changes are proposed as [pull requests on GitHub](https://github.com/canonical/charm-ubuntu/pulls).

Pull requests should have a short title that follows the [conventional commit style](https://www.conventionalcommits.org/en/) using one of these types:

- chore
- ci
- docs
- feat
- fix
- perf
- refactor
- revert
- test

Some examples:

- feat: add support for a new Ubuntu base
- fix!: correct the handling of the update-status hook
- docs: clarify how to deploy to a specific base

We consider this project too small to use scopes, so we don't use them.

Note that the commit messages to the PR's branch do not need to follow the conventional commit format, as these will be squashed into a single commit to `master` using the PR title as the commit message.

To help us review your changes, please rebase your pull request onto the `master` branch before you request a review. If you need to bring in the latest changes from `master` after the review has started, please use a merge commit.

# Development

Install [uv](https://docs.astral.sh/uv/) and [Charmcraft](https://documentation.ubuntu.com/charmcraft/4.3/) (`sudo snap install --classic charmcraft`). The `make` targets below will set up the appropriate dependency groups on demand. `charmcraft.spread` (bundled with the Charmcraft snap) is used to run integration tests.

## Linting and formatting

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting, and [pyright](https://github.com/microsoft/pyright) for type checking:

```bash
make lint     # Check for issues
make format   # Auto-fix issues
```

You can also use [pre-commit](https://pre-commit.com/) to run checks automatically:

```bash
uvx pre-commit install
```

## Running tests

```bash
make unit          # Unit tests
make integration   # Integration tests, run in an isolated VM via Spread
```

`make integration` runs the tests with [opcli](https://github.com/canonical/charm-ci) and [Spread](https://github.com/canonical/spread/). Each job gets a fresh LXD VM, prepared with [concierge](https://github.com/canonical/concierge), and the jobs cover each supported Ubuntu base with both Juju 3 and Juju 4. The tests deploy the charm you've already packed, so build it first with `uv run --group tooling opcli artifacts build`, which writes `build/artifacts.build.yaml`. Use `make integration-debug` to drop into a shell on failure.

To run a single job, list the selectors and pass one through to Spread:

```bash
uv run --group tooling opcli spread run -- -list
uv run --group tooling opcli spread run -- integration-test-local:ubuntu-24.04:build/tests/integration/run:base_2404_juju3
```

If you already have a Juju controller and a machine cloud set up and want to skip Spread, `uv run --group tooling opcli pytest run` runs the same `tox -e integration` invocation that the Spread VM uses. It also needs the charm built first, and tests on 24.04 unless you set `BASE`, for example `BASE=22.04`.

## Developing in a workshop

The `dev` [Workshop](https://ubuntu.com/workshop) in `.workshop/` is a container with uv, `make`, the charm's development dependencies, and the [Pi](https://pi.dev) coding agent. You don't need to install any of them on your host:

```bash
sudo snap install workshop --classic  # If you don't have it already.
workshop launch dev
workshop run dev lint
```

The `format`, `lint`, and `unit` actions run the `make` targets with the same names. Extra arguments to `unit` are passed to `pytest`, so `workshop run dev unit -k test_hostname` is the same as `make unit ARGS='-k test_hostname'`. An argument containing whitespace won't survive: the `make` recipe expands `$(ARGS)` unquoted, so `-k 'test_a and not test_b'` reaches `pytest` as four arguments whether you go through the workshop or run `make` yourself. The workshop keeps its virtual environment outside the project directory, so it doesn't share or overwrite the `.venv` on your host.

The `pi` action runs Pi in the workshop, where it can reach the project directory but not the rest of your host. Pi's settings and credentials are kept in a mount, so they survive `workshop refresh`.

There's no integration test action. Spread runs the tests in an LXD VM, and the workshop has no KVM. Packing the charm also fails in the workshop, because snapd won't start in Charmcraft's nested build container. Run `make integration` on your host.

# Publishing

Every merge to `master` is packed and released to `latest/edge` by the [Publish to edge](.github/workflows/publish-edge.yaml) workflow. That workflow is also the only thing that creates GitHub releases in this repo: its final step (in `canonical/charm-ci`) tags the commit and publishes a release for the packed charm, which is why the job needs `contents: write`. Promotion to `beta`, `candidate`, or `stable` is done manually via the [Promote charm](.github/workflows/promote.yaml) workflow (Actions → Promote charm → Run workflow), which is gated by a required-reviewer approval on the `charmhub-promote` environment.

Both workflows authenticate to Charmhub using a `CHARMCRAFT_AUTH` secret. Publish to edge reads it as a **repository-level** secret: GitHub Actions forbids `environment:` on a job that calls a reusable workflow, so the credential can't be scoped to an environment there. Promote charm does run in an environment, and reads `CHARMCRAFT_AUTH` from `charmhub-promote`.

## Regenerating the `CHARMCRAFT_AUTH` secret

The exported credentials have a time-to-live (we use one year). When they expire, or if they are ever exposed, generate a new one:

1. On a machine with `charmcraft` installed and an account that has publisher rights on the `ubuntu` charm, run:

   ```bash
   charmcraft login \
     --export=auth.txt \
     --charm=ubuntu \
     --permission=package-manage \
     --permission=package-view \
     --ttl=31536000
   ```

   `--ttl` is in seconds (`31536000` = one year).

2. Copy the full contents of `auth.txt`.

3. In GitHub, update the secret in both places it lives:

   - **Settings → Secrets and variables → Actions → Repository secrets** — `CHARMCRAFT_AUTH`, used by Publish to edge.
   - **Settings → Environments → `charmhub-promote`** — `CHARMCRAFT_AUTH`, used by Promote charm.

4. Delete the local `auth.txt` (`shred -u auth.txt`) — the credentials are not encrypted.

5. Once the new secret is in place, revoke the previous credentials with `charmcraft logout` on the machine you used to create them (or via Charmhub's session management if you no longer have the token).
