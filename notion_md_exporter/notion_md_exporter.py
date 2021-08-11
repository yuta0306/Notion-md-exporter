from .notion_client import NotionClient

import re
from typing import Dict, NoReturn, Optional, List

class NotionMdExporter:
    def __init__(self, key: Optional[str] = None) -> None:
        self.client = NotionClient(key=key)
        self.validated = False

    def export(self, page_id: str, export_path: str) -> NoReturn:
        page_id = self._parse_id(page_id=page_id)
        self.validated = self._validation(page_id)
        if not self.validated:
            raise ValueError('Could not find the page')
        
        self._create_file(page_id=page_id, export_path=export_path)

        return

    def _parse_id(self, page_id: str) -> str:
        if 'https://www.notion.so/' in page_id:
            page_id = re.sub(r'https://www.notion.so/', '', page_id)

        return page_id

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

        depth = 0
        _, res = self.client.get_blocks(page_id)
        if res.get('has_children'):
            self._generate_block(page_id, content, depth)             
        
        with open(export_path, 'w', encoding='utf-8') as f:
            f.writelines(content)

    def _get_tag(self, _type: str) -> str:
        tag = ''
        if _type == 'heading_2':
            tag = '## '
        elif _type == 'heading_3':
            tag = '### '
        elif _type == 'to_do':
            tag = '- [ ] '

        return tag

    def _generate_block(self, _id: str, content: List[str], depth: int) -> List[str]:
        _, result = self.client.get_child_blocks(_id)
        child_blocks = result.get('results')
        for block in child_blocks:
            _object = block.get('object')
            _id = block.get('id')
            has_children = block.get('has_children')
            parent_type = block.get('type')
            tag = self._get_tag(parent_type)
            indent = '&nbsp;' * (depth * 4)
            i = -1
            for i, text_info in enumerate(block[parent_type].get('text', [])):
                _type = text_info['type']
                if parent_type == 'to_do': # checkbox
                    checked = block[parent_type]['checked']
                    if checked:
                        tag = re.sub('\[\s\]', '[x]', tag)
                plane_text = text_info[_type]['content']
                link = text_info[_type]['link']
                annotation = text_info['annotations']
                annotated_text = self._decorate_text(annotation, plane_text)
                text = f'{indent}{tag}{annotated_text}\n'
                content.append(text)
            if i > -1:
                content.append('\n')

            if has_children:
                if parent_type == 'child_page':
                    title = self._get_title(page_id=_id)
                    content.append(f'# {title}\n\n')
                    self._generate_block(_id, content=content, depth=0)
                    content.append('\n\n---\n\n')
                else:
                    self._generate_block(_id, content=content, depth=depth+1)
            
    def _decorate_text(self, annotation: Dict[str, bool], plane_text: str) -> str:
        if annotation.get('bold'):
            plane_text = f'**{plane_text}**'
        elif annotation.get('italic'):
            plane_text = f'*{plane_text}*'
        elif annotation.get('strikethrough'):
            plane_text = f'~~{plane_text}~~'
        elif annotation.get('code'):
            plane_text = f'`{plane_text}`'

        return plane_text        