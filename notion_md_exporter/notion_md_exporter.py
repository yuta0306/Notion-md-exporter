from .notion_client import NotionClient

from typing import Dict, NoReturn, Optional, List

class NotionMdExporter:
    def __init__(self, key: Optional[str] = None) -> None:
        self.client = NotionClient(key=key)
        self.validated = False

    def export(self, page_id: str, export_path: str) -> NoReturn:
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

        depth = 0
        _, res = self.client.get_blocks(page_id)
        if res.get('has_children'):
            self._generate_block(page_id, content, depth)
            # _, result = self.client.get_child_blocks(page_id)
            # child_blocks = result.get('results')
            # for block in child_blocks:
            #     _object = block.get('object')
            #     _id = block.get('id')
            #     has_children = block.get('has_children')
            #     _type = block.get('type')
            #     tag = self._get_tag(_type)
            #     for text_info in block[_type]['text']:
            #         _type = text_info['type']
            #         text = f'{tag}{text_info[_type]["content"]}\n'
            #         content.append(text)
                
            #     content.append('\n')
                

        
        with open(export_path, 'w', encoding='utf-8') as f:
            f.writelines(content)

    def _get_tag(self, _type: str) -> str:
        tag = ''
        if _type == 'heading_2':
            tag = '## '
        elif _type == 'heading_3':
            tag = '### '

        return tag

    def _generate_block(self, _id: str, content: List[str], depth: int) -> List[str]:
        _, result = self.client.get_child_blocks(_id)
        child_blocks = result.get('results')
        for block in child_blocks:
            _object = block.get('object')
            _id = block.get('id')
            has_children = block.get('has_children')
            _type = block.get('type')
            tag = self._get_tag(_type)
            indent = '&nbsp;' * (depth * 4)
            print(block)
            i = -1
            for i, text_info in enumerate(block[_type]['text']):
                _type = text_info['type']
                plane_text = text_info[_type]['content']
                link = text_info[_type]['link']
                annotation = text_info['annotations']
                annotated_text = self._decorate_text(annotation, plane_text)
                text = f'{indent}{tag}{annotated_text}\n'
                content.append(text)
            if i >= 0:
                content.append('\n')
            if has_children:
                self._generate_block(_id, content=content, depth=depth+1)
            
            # content.append('\n')

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