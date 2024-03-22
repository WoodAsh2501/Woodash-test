from bs4 import BeautifulSoup, Comment
from pathlib import Path

categorys = ["essays", "weekly"]
attrDict = {
    "title": "woodash-title",
    "category": "woodash-category",
    "note": "woodash-note",
    "tucao": "woodash-tucao",
    "scene": "woodash-scene",
    "welcome": "woodash-welcome",
    "date": "date",
}

folder = Path(".")

class Page:
    welcome = False

    def __init__(
        self, title="", category="", note="", tucao="", scene="", date="", path=""
    ):
        self.title = title
        self.category = category
        self.note = note
        self.tucao = tucao
        self.scene = scene
        self.date = date
        self.path = path

    def setAttrs(self):
        with open(self.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            head = content.head

            attrs = [attr for attr in attrDict.keys()]

            for attr in attrs:
                attrName = attrDict[attr]
                tag = head.find("meta", attrs={"name": attrName})
                if tag:
                    setattr(self, attr, tag["content"])

                # pagesInCategory.append(page)

    def addWelcome(self):
        with open(self.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            welcomeMsg = """
欢迎来到花园杂乱无章的*苗圃*！
请随意看看吧。
"""
            welcomeComment = Comment(welcomeMsg)
            if self.welcome == False:

                content.insert(0, welcomeComment)
                self.welcome = True
            else:
                comment = content.contents[0]
                if type(comment) == Comment:
                    comment.replace_with(welcomeComment)
                # self.welcome = True
            HTML.seek(0)
            HTML.truncate(0)
            HTML.write(content.prettify())

    def updateHead(self):
        with open(self.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            head = content.head
            headTemplate = f"""
                        <meta charset="utf-8" />
                        <meta name="generator" content="pandoc" />
                        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                        <meta name="woodash-welcome" content="{self.welcome}">
                        <meta name="woodash-title" content="{self.title}">
                        <meta name="woodash-category" content="{self.category}">
                        <meta name="woodash-note" content="{self.note}">
                        <meta name="woodash-tucao" content="{self.tucao}">
                        <meta name="woodash-scene" content="{self.scene}">
                        <meta name="date" content="{self.date}" />
                        <title>Woodash * {self.title}</title>
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


def getPages():
    _pages = []
    for category in categorys:
        # pagesInCategory = []
        categoryDir = folder / category

        for fileName in categoryDir.iterdir():
            page = Page()
            page.path = Path(fileName)
            _pages.append(page)

    return _pages


pages = getPages()
pages.sort(key=lambda x: x.date)

for page in pages:
    page.setAttrs()
    page.addWelcome()
    page.updateHead()
