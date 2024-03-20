import os
from bs4 import BeautifulSoup

allCategory = ["essays", "weekly"]
allPages = []

for categoryName in allCategory:
    pagesInCategory = []
    for page in os.listdir(categoryName):
        path = f"{categoryName}/{page}"
        attrs = {
            "woodash-title": "",
            "woodash-category": "",
            "woodash-note": "",
            "woodash-tucao": "",
            "woodash-scene": "",
            "date": "",
        }
        with open(path, "r+", encoding="utf-8") as HTML:
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

            headTemplate = f"""
                            <meta charset="utf-8" />
                            <meta name="generator" content="pandoc" />
                            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                            <meta name="woodash-title" content="{attrs["woodash-title"]}">
                            <meta name="woodash-category" content="{attrs["woodash-category"]}">
                            <meta name="woodash-note" content="{attrs["woodash-note"]}">
                            <meta name="woodash-tucao" content="{attrs["woodash-tucao"]}">
                            <meta name="woodash-scene" content="{attrs["woodash-scene"]}">
                            <meta name="date" content="{attrs["date"]}" />
                            <title>Woodash * {attrs["woodash-title"]}</title>

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

pagesInCategory.sort(key=lambda x: x["date"])
allPages.extend(pagesInCategory)
allPages.sort(key=lambda x: x["date"])
