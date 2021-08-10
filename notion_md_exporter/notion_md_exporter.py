from .notion_client import NotionClient

from typing import Optional

class NotionMdExporter:
    def __init__(self, key: Optional[str]=None) -> None:
        self.client = NotionClient(key=key)
        self.validated = False

    def export(self, page_id: str):
        self.validated = self._validation(page_id)
        if not self.validated:
            raise ValueError('Could not find the page')
        
        title = self._get_title(page_id=page_id)
        return title

    def _validation(self, _id: str) -> bool:
        status_code, res = self.client.get_page(_id)
        if 200 <= status_code < 300:
            return True
        else:
            return False

    def _get_title(self, page_id: str) -> str:
        if not self.validated:
            self._validation(page_id)
        _, res = self.client.get_blocks(page_id)
        _type = res['type']
        title = res[_type]['title']

        return title

    def _create_file(self):
        pass