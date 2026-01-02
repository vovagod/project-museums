from langchain_text_splitters import HTMLHeaderTextSplitter, HTMLSectionSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

url = "https://www.museumpereslavl.ru/ru/museum/exhibition/detail/b9941017-f9c0-11ef-a0c9-55a88fa2d635/#:~:text=%D0%A1%207%20%D0%BC%D0%B0%D1%80%D1%82%D0%B0,%3A%20%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%2010"

headers_to_split_on = [
    #("div", "information"),
    ("h2", "Header 2"),
]

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on)
html_header_splits = html_splitter.split_text_from_url(url)
#print(html_header_splits[1].page_content[:500])

print(f"SPLIT: {html_header_splits}")