from notion_md_exporter import NotionClient, NotionMdExporter

if __name__ == '__main__':
    # client = NotionClient()
    # res = client.get_page('0017d9d63e434978a35f958ac8b2f8bc')
    # print(res.json())
    # print('===')
    # status_code, result = client.get_blocks('0017d9d63e434978a35f958ac8b2f8bc')
    # print(status_code, result)
    # print('===')
    # res = client.get_child_blocks('0017d9d63e434978a35f958ac8b2f8bc')
    # print(res.json())

    exporter = NotionMdExporter()
    print(exporter.export('0017d9d63e434978a35f958ac8b2f8bc', './test.md'))