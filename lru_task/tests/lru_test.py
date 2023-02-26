from lru import LRUCache
import pytest

@pytest.fixture
def test_cache():
    cache = LRUCache(3)

    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')

    return cache

def test_cache_size_exceeded(test_cache):
    test_cache.set('key4', 'value4')

    assert test_cache.get('key1') == ''
    assert test_cache.get('key4') == 'value4'

def test_correct_update_logic(test_cache):
    assert test_cache.get('key1') == 'value1'

    test_cache.set('key4', 'value4')

    assert test_cache.get('key1') == 'value1'
    assert test_cache.get('key4') == 'value4'
    assert test_cache.get('key2') == ''

def test_get_set_rem_methods(test_cache):
    assert test_cache.get('key1') == 'value1'

    test_cache.set('key1', 'value4')

    assert test_cache.get('key1') == 'value4'

    test_cache.rem('key1')

    assert test_cache.get('key1') == ''