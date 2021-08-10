from .notion_client import NotionClient

from typing import Optional

class NotionMdExporter:
    def __init__(self, key: Optional[str]=None) -> None:
        self.client = NotionClient(key=key)
        self.validated = False

    def export(self, page_id: str, export_path: str):
        self.validated = self._validation(page_id)
        if not self.validated:
            raise ValueError('Could not find the page')
        
        self._create_file(page_id=page_id, export_path=export_path)

        return

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

    def _create_file(self, page_id: str, export_path: str):
        title = self._get_title(page_id=page_id)
        content = [f'# {title}\n', '\n']

        _, res = self.client.get_blocks(page_id)
        if res['has_children']:
            _, result = self.client.get_child_blocks(page_id)
            child_blocks = result['results']
            for block in child_blocks:
                _object = block['object']
                _id = block['id']
                has_children = block['has_children']
                _type = block['type']
                tag = self._get_tag(_type)
                for text_info in block[_type]['text']:
                    _type = text_info['type']
                    text = f'{tag}{text_info[_type]["content"]}\n'
                    content.append(text)
                
                content.append('\n')
                

        
        with open(export_path, 'w', encoding='utf-8') as f:
            f.writelines(content)

    def _get_tag(self, _type: str) -> str:
        tag = ''
        if _type == 'heading_2':
            tag = '## '
        elif _type == 'heading_3':
            tag = '### '

        return tag