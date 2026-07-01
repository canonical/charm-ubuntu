# Ubuntu Charm

This charm provides a pristine [Ubuntu](https://ubuntu.com) cloud/server image. It does not provide any applications other than a blank cloud image. It is intended for testing, development, and as a base for manual machine management.

## Usage

Deploy the charm:

```bash
juju deploy ubuntu
```

SSH to the instance:

```bash
juju ssh ubuntu/0
```

> **Note:** With Juju 4, you need to set up an SSH key before you can SSH into units. See the [Juju documentation on SSH keys](https://documentation.ubuntu.com/juju/latest/howto/manage-ssh-keys/).

### Scaling out

This charm is not designed to be used at scale since it does not have any relations. However, you can still bulk add machines:

```bash
juju add-unit ubuntu      # Add one more
juju add-unit -n 5 ubuntu  # Add 5 at a time
```

You can also alias names to manage a set of Ubuntu instances:

```bash
juju deploy ubuntu mytestmachine1
juju deploy ubuntu mytestmachine2
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `hostname` | string | `""` | Set the hostname of the machine. When empty, the default machine hostname is used. |

## Known Limitations

This charm does not provide anything other than a blank server. It does not support any relations other than subordinate charm relations.

## Contact

- Upstream Ubuntu
- [Bug tracker](https://github.com/canonical/charm-ubuntu/issues)
- [Matrix](https://matrix.to/#/#charmhub-charmdev:ubuntu.com)
