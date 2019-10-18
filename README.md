[![CircleCI](https://circleci.com/gh/AdamGleave/pytest-shard.svg?style=svg)](https://circleci.com/gh/AdamGleave/pytest-shard)
[![PyPI version](https://badge.fury.io/py/pytest-shard.svg)](https://badge.fury.io/py/pytest-shard)

# pytest-shard

Shards tests based on a hash of their test name enabling easy parallelism across machines, suitable for a wide variety of continuous integration services. Tests are split at the finest level of granularity, individual test cases, enabling parallelism even if all of your tests are in a single file (or even single parameterized test method).

## Features

`pytest-shard` aims for simplicity. When installed, simply run:

```
$ pytest --shard-id=I --num-shards=N
```

where `I` is the index of this shard and `N` the total number of shards. For example, to split tests across two machines:

```
# On machine 1:
$ pytest --shard-id=0 --num-shards=2
# On machine 2:
$ pytest --shard-id=1 --num-shards=2
```

The intended use case is for continuous integration services that allow you to run jobs in parallel. For CircleCI, enable [parallelism](https://circleci.com/docs/2.0/parallelism-faster-jobs/) and then use:
```
pytest --shard-id=${CIRCLE_NODE_INDEX} --num-shards=${CIRCLE_NODE_TOTAL}
```

On Travis, you must define the environment variables explicitly, but can use a [similar approach](https://docs.travis-ci.com/user/speeding-up-the-build/).

## Alternatives

[pytest-xdist](https://github.com/pytest-dev/pytest-xdist) allows you to parallelize tests across cores on a single machine, and can also schedule tests on a remote machine. I use `pytest-shard` to split tests across CI workers, and `pytest-xdist` to parallelize across CPU cores within each worker.

`pytest-shard` does not take into account the run time of tests, which can lead to suboptimal allocations. [pytest-circleci-parallelized](https://github.com/ryanwilsonperkin/pytest-circleci-parallelized) uses test run time, but can only split at the granularity of classes, and is specific to CircleCI.

Please open a PR if there are other promising alternatives that I have overlooked.

## Installation

You can install `pytest-shard` via `pip`:

```
$ pip install pytest-shard
```

## Contributions

Contributions are welcome. Test may be run using `tox`.

## License

This software is MIT licensed.
