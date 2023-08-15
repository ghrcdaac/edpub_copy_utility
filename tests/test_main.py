import math
import unittest
from unittest.mock import MagicMock

from src_py.main import get_keys, scan_ed_pub


class FakePaginator:
    def __init__(self, key_count, page_size, start_at=0):
        self.key_count = key_count
        self.page_size = page_size
        self.page_count = int(math.ceil(self.key_count / self.page_size))
        self.start_at = start_at
        self.keys = [{'Key': f'key_{x + self.start_at}'} for x in range(self.start_at, self.key_count + self.start_at)]

    def paginate(self, **kwargs):
        index = 0
        for x in range(self.page_count):
            yield {'Contents': self.keys[index:index + self.page_size]}
            index += self.page_size


class TestMain(unittest.TestCase):
    def test_fake_paginator_1(self):
        key_count = 5
        page_size = 2
        fp = FakePaginator(key_count, page_size)
        self.assertEqual(fp.key_count, key_count)
        self.assertEqual(fp.page_size, page_size)
        self.assertEqual(fp.start_at, 0)
        self.assertEqual(len(fp.keys), key_count)

        results = []
        for x in fp.paginate():
            results.append(x)

        self.assertEqual(len(results), 3)

    def test_fake_paginator_2(self):
        key_count = 5
        page_size = 2
        start_at = 5
        fp = FakePaginator(key_count, page_size, start_at)
        self.assertEqual(fp.key_count, key_count)
        self.assertEqual(fp.page_size, page_size)
        self.assertEqual(fp.start_at, start_at)
        self.assertEqual(len(fp.keys), key_count)

        results = []
        for x in fp.paginate():
            results.append(x)

        self.assertEqual(len(results), 3)

    def test_get_keys(self):
        fake_bucket = 'fake_bucket_1'
        fake_paginator_1 = FakePaginator(5, 2)
        keys = get_keys(fake_paginator_1, fake_bucket)

        self.assertSetEqual(keys, set(x.get('Key') for x in fake_paginator_1.keys))

    def test_scan_ed_pub(self):
        scan_ed_pub(MagicMock())
