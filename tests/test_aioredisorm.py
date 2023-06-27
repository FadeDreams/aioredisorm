import pytest
import asyncio
import unittest
import aioredis
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aioredisorm import AIORedisORM



class TestAIORedisORM(unittest.IsolatedAsyncioTestCase):


    async def asyncSetUp(self):
        self.redis_client = AIORedisORM(key_prefix='my_prefix')
        await self.redis_client.connect()

    async def asyncTearDown(self):
        await self.redis_client.close()

    async def test_set_value(self):
        await self.redis_client.set_value('my_key', 'my_value', ex=1)
        result = await self.redis_client.get_value('my_key')
        self.assertEqual(result, b'my_value')

    async def test_set_hash(self):
        await self.redis_client.set_hash('my_hash', {'key1': 'value1', 'key2': 'value2', 'key3': 3}, ex=60)
        hash_result = await self.redis_client.get_hash('my_hash')
        self.assertEqual(hash_result, {b'key1': b'value1', b'key2': b'value2', b'key3': b'3'})

    async def test_set_list(self):
        await self.redis_client.delete_key('my_list')  # Delete the list before setting it
        await self.redis_client.set_list('my_list', 'value1', 'value2', 'value3')
        list_result = await self.redis_client.get_list('my_list')
        self.assertEqual(list_result, [b'value1', b'value2', b'value3'])

    async def test_set_list_with_expiration(self):
        await self.redis_client.delete_key('my_list')  # Delete the list before setting it
        await self.redis_client.set_list('my_list', 'value1', 'value2', 'value3', ex=1)
        list_result = await self.redis_client.get_list('my_list')
        self.assertEqual(list_result, [b'value1', b'value2', b'value3'])

        await asyncio.sleep(2)  # Wait for the expiration to pass

        list_result = await self.redis_client.get_list('my_list')
        self.assertEqual(list_result, [])  # The list should be empty


if __name__ == '__main__':
    unittest.main()


