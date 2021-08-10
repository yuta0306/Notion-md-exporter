import requests
import os
import sys

from typing import Union, Optional

class NotionClient:
    def __init__(self, key: Optional[str]=None) -> None:
        if key is None:
            key = os.environ.get('NOTION_KEY')
            if key is None:
                raise ValueError('if key is None, global environment have NOTION_KEY.')
        
        self.key = key

    def get_page(self, page_id: str):
        headers = {
            'Notion-Version': '2021-05-13',
            'Authorization': f'Bearer {self.key}',
        }
        res = requests.get(f'https://api.notion.com/v1/pages/{page_id}',
                            headers=headers)
        return res

    def get_blocks(self, block_id: str):
        headers = {
            'Notion-Version': '2021-05-13',
            'Authorization': f'Bearer {self.key}',
        }
        res = requests.get(f'https://api.notion.com/v1/blocks/{block_id}',
                            headers=headers)
        return res

    def get_child_blocks(self, block_id: str, start_cursor: Optional[str]=None):
        headers = {
            'Notion-Version': '2021-05-13',
            'Authorization': f'Bearer {self.key}',
        }
        params = {
            'page_size': 100,
            'start_cursor': start_cursor,
        }
        res = requests.get(f'https://api.notion.com/v1/blocks/{block_id}/children',
                            headers=headers, params=params)
        return res