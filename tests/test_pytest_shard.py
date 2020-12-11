"""Test pytest_shard.pytest_shard."""

import collections
import itertools

import hypothesis
from hypothesis import strategies
import pytest

from pytest_shard import pytest_shard


@hypothesis.given(strategies.integers(min_value=0))
def test_positive_int_with_pos(x):
    assert pytest_shard.positive_int(x) == x
    assert pytest_shard.positive_int(str(x)) == x


@hypothesis.given(strategies.integers(max_value=-1))
def test_positive_int_with_neg(x):
    with pytest.raises(ValueError):
        pytest_shard.positive_int(x)
    with pytest.raises(ValueError):
        pytest_shard.positive_int(str(x))


def test_positive_int_with_non_num():
    invalid = ["foobar", "x1", "1x"]
    for s in invalid:
        with pytest.raises(ValueError):
            pytest_shard.positive_int(s)


@hypothesis.given(strategies.text())
def test_sha256hash_deterministic(s):
    x = pytest_shard.sha256hash(s)
    y = pytest_shard.sha256hash(s)
    assert x == y
    assert type(x) == int


@hypothesis.given(strategies.text(), strategies.text())
def test_sha256hash_no_clash(s1, s2):
    if s1 != s2:
        assert pytest_shard.sha256hash(s1) != pytest_shard.sha256hash(s2)


MockItem = collections.namedtuple("MockItem", "nodeid")


@hypothesis.given(
    names=strategies.lists(strategies.text(), unique=True),
    num_shards=strategies.integers(min_value=1, max_value=500),
)
def test_filter_items_by_shard(names, num_shards):
    items = [MockItem(name) for name in names]

    filtered = [
        pytest_shard.filter_items_by_shard(items, shard_id=i, num_shards=num_shards)
        for i in range(num_shards)
    ]
    all_filtered = list(itertools.chain(*filtered))
    assert len(all_filtered) == len(items)
    assert set(all_filtered) == set(items)
