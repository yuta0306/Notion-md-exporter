from notion_md_exporter import NotionClient

if __name__ == '__main__':
    client = NotionClient()
    # res = client.get_page('0017d9d63e434978a35f958ac8b2f8bc')
    # print(res.json())
    # print('===')
    # res = client.get_blocks('0017d9d63e434978a35f958ac8b2f8bc')
    # print(res.json())
    # print('===')
    res = client.get_child_blocks('0017d9d63e434978a35f958ac8b2f8bc')
    print(res.json())