import os
from bs4 import BeautifulSoup

categorys = ["essays", "weekly"]
pages = []

class Page:
    def __init__(self, title="", category="", note="", tucao="", scene="", date="", path=""):
        self.title = title
        self.category = category
        self.note = note
        self.tucao = tucao
        self.scene = scene
        self.date = date
        self.path = path
        
for category in categorys:
    pagesInCategory = []
    for directory in os.listdir(category):
        page = Page()
        page.path = f"{category}/{directory}"

        with open(page.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            head = content.head
            
            attrs = [attr for attr in dir(page)
                     if not attr.startswith("__")]

            for attr in attrs:
                if attr == "path":
                    continue

                if attr in ["date"]:
                    attrName = attr
                else:
                    attrName = "woodash-" + attr

                tag = head.find("meta", attrs={"name": attrName})
                setattr(page, attr, tag["content"])

            pagesInCategory.append(page)

            headTemplate = f"""
                            <meta charset="utf-8" />
                            <meta name="generator" content="pandoc" />
                            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                            <meta name="woodash-title" content="{page.title}">
                            <meta name="woodash-category" content="{page.category}">
                            <meta name="woodash-note" content="{page.note}">
                            <meta name="woodash-tucao" content="{page.tucao}">
                            <meta name="woodash-scene" content="{page.scene}">
                            <meta name="date" content="{page.date}" />
                            <title>Woodash * {page.title}</title>

                            <link rel="icon" href="../images/favicon.ico" />

                            <link rel="preconnect" href="https://ik.imagekit.io" crossorigin />
                            <link
                            href="https://ik.imagekit.io/Woodash/SourceHanSerifSC-VF/result.css"
                            rel="stylesheet"
                            />
                            <link href="../styles/normalize.css" rel="stylesheet" />
                            <link href="../styles/basic.css" rel="stylesheet" />
                            <link href="../styles/articles.css" rel="stylesheet" />
                            <script defer src="../scripts/article/setImageSize.js"></script>
                            """

            head.clear()
            head.append(BeautifulSoup(headTemplate, "html.parser"))
            # 写入
            HTML.seek(0)
            HTML.truncate(0)
            HTML.write(content.prettify())

    pagesInCategory.sort(key=lambda x: x.date)
    pages.extend(pagesInCategory)


pages.sort(key=lambda x: x.date)
