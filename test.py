import os
from bs4 import BeautifulSoup

allCategory = ["essays", "weekly"]
allPages = []

class Article:
    def __init__(self, title="", category="", note="", tucao="", scene="", date="", path=""):
        self.title = title
        self.category = category
        self.note = note
        self.tucao = tucao
        self.scene = scene
        self.date = date
        self.path = path
        
for categoryName in allCategory:
    pagesInCategory = []
    for page in os.listdir(categoryName):
        article = Article()
        article.path = f"{categoryName}/{page}"

        with open(article.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            head = content.head
            
            attrs = [attr for attr in dir(article)
                     if not attr.startswith("__")]

            for attr in attrs:
                if attr == "path":
                    continue

                if attr in ["date"]:
                    attrName = attr
                else:
                    attrName = "woodash-" + attr

                tag = head.find("meta", attrs={"name": attrName})
                setattr(article, attr, tag["content"])

            pagesInCategory.append(article)

            headTemplate = f"""
                            <meta charset="utf-8" />
                            <meta name="generator" content="pandoc" />
                            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                            <meta name="woodash-title" content="{article.title}">
                            <meta name="woodash-category" content="{article.category}">
                            <meta name="woodash-note" content="{article.note}">
                            <meta name="woodash-tucao" content="{article.tucao}">
                            <meta name="woodash-scene" content="{article.scene}">
                            <meta name="date" content="{article.date}" />
                            <title>Woodash * {article.title}</title>

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
    allPages.extend(pagesInCategory)


allPages.sort(key=lambda x: x.date)
