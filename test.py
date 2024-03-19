import os
from bs4 import BeautifulSoup

allCategory = ["essays", "weekly"]
allPages = []

attrs = {
    "woodash-title": "",
    "woodash-category": "",
    "woodash-note": "",
    "woodash-tucao": "",
    "woodash-scene": "",
    "date": "",
}

for categoryName in allCategory:
    pagesInCategory = []
    for page in os.listdir(categoryName):
        path = f"{categoryName}/{page}"
        with open(path) as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            head = content.head

            for item in attrs.items():
                name = item[0]
                tag = head.find("meta", attrs={"name": name})
                attrs[name] = tag["content"]

            pagesInCategory.append(
                {
                    "title": attrs["woodash-title"],
                    "category": attrs["woodash-category"],
                    "note": attrs["woodash-note"],
                    "tucao": attrs["woodash-tucao"],
                    "scene": attrs["woodash-scene"],
                    "date": attrs["date"],
                    "path": path,
                }
            )
    pagesInCategory.sort(key=lambda x: x["date"])
    allPages.extend(pagesInCategory)

allPages.sort(key=lambda x: x["date"])
print(allPages)
