# Ubuntu Charm

This charm provides a pristine [Ubuntu](https://ubuntu.com) cloud/server image. It does not provide any applications other than a blank cloud image for you to manage manually. It is intended for testing, development, and as a base for manual machine management.

## Usage

Deploy the charm:

```bash
juju deploy ubuntu
```

SSH to the instance:

```bash
juju ssh ubuntu/0
```

### Scaling out

This charm is not designed to be used at scale since it does not have any relations, however you can bulk add machines with `add-unit`:

```bash
juju add-unit ubuntu      # Add one more
juju add-unit -n5 ubuntu  # Add 5 at a time
```

You can also alias names to organize a set of empty instances:

```bash
juju deploy ubuntu mytestmachine1
juju deploy ubuntu mytestmachine2
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `hostname` | string | `""` | Override hostname of the machine. When empty, the default machine hostname is used. |

## Known Limitations

This charm does not provide anything other than a blank server, so it does not relate to other charms, other than subordinate charm relations.

## Development

Set up a Python virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the linter:

```bash
tox -e lint
```

Run the unit tests:

```bash
tox -e unit
```

Run the integration tests:

```bash
tox -e integration
```

## Contact

- [Upstream Ubuntu](https://ubuntu.com)
- [Bug tracker](https://github.com/canonical/charm-ubuntu/issues)
- [Ubuntu Server mailing list](https://lists.ubuntu.com/archives/ubuntu-server/)
- [Matrix](https://matrix.to/#/#charmhub-charmdev:ubuntu.com)
