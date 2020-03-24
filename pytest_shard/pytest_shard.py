"""Shard tests to support parallelism across multiple machines."""

import hashlib


def positive_int(x):
    x = int(x)
    if x < 0:
        raise ValueError("Argument {x} must be positive".format(x=x))
    return x


def pytest_addoption(parser):
    """Add pytest-shard specific configuration parameters."""
    group = parser.getgroup("shard")
    group.addoption(
        "--shard-id", dest="shard_id", type=positive_int, default=0, help="Number of this shard."
    )
    group.addoption(
        "--num-shards",
        dest="num_shards",
        type=positive_int,
        default=1,
        help="Total number of shards.",
    )


def pytest_report_collectionfinish(config, items):
    """Log how many and, if verbose, which items are tested in this shard."""
    msg = "Running {num} items in this shard".format(num=len(items))
    if config.option.verbose > 0:
        msg += ": " + ", ".join([item.nodeid for item in items])
    return msg


def md5hash(x):
    return int(hashlib.md5(x.encode('utf8')).hexdigest(), 16)


def filter_items_by_shard(items, shard_id, num_shards):
    """Computes `items` that should be tested in `shard_id` out of `num_shards` total shards."""
    shards = [md5hash(item.nodeid) % num_shards for item in items]

    new_items = []
    for shard, item in zip(shards, items):
        if shard == shard_id:
            new_items.append(item)
    return new_items


def pytest_collection_modifyitems(config, items):
    """Mutate the collection to consist of just items to be tested in this shard."""
    shard_id = config.getoption("shard_id")
    shard_total = config.getoption("num_shards")
    if shard_id >= shard_total:
        raise ValueError("shard_num = {shard_num} must be less than shard_total = {shard_total}".format(shard_num=shard_num, shard_total=shard_total))

    items[:] = filter_items_by_shard(items, shard_id, shard_total)
