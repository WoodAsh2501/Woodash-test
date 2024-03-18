import os
import datetime
from bs4 import BeautifulSoup

allCategory = ["essays", "weekly"]

allPages = []

for categoryName in allCategory:
    pagesInCategory = []
    for page in os.listdir(categoryName):
        path = f'{categoryName}/{page}'
        with open(path) as HTML:
            content = BeautifulSoup(HTML, 'html.parser')
            head = content.head
            title = head.find("title").string

            categoryTag = head.find("meta", attrs={"name": "woodash-category"})
            category = categoryTag["content"]

            dateTag = head.find("meta", attrs={"name": "date"})
            # 我发现不用datetime也行
            # dateString = dateTag["content"]
            # date = datetime.datetime.strptime(dateString, "%Y-%m-%d")
            date = dateTag["content"]
            pagesInCategory.append({"title": title,
                             "category": category,
                             "date": date,
                             "path": path
                             }) 
    pagesInCategory.sort(key=lambda x: x["date"])
    allPages.extend(pagesInCategory)

allPages.sort(key=lambda x: x["date"])
print(allPages)
