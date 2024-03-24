from pathlib import Path
from bs4 import BeautifulSoup, Comment
from textwrap import dedent


categorys = ["essay", "weekly"]
categoryDict = {
    "essay": "杂谈",
    "weekly": "周报",
    "experience": "体验",
    "records": "琐记",
    "note": "笔记",
}
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
        self.welcome = False

    def setAttrs(self):
        with open(self.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            head = content.head

            attrs = (attr for attr in attrDict.keys())

            for attr in attrs:
                attrName = attrDict[attr]
                tag = head.find("meta", attrs={"name": attrName})
                if tag:
                    setattr(self, attr, tag["content"])

    def addWelcome(self):
        with open(self.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            welcomeMsg = """
                        欢迎来到花园杂乱无章的*苗圃*！
                        请随意看看吧。
                        """
            welcomeComment = Comment(dedent(welcomeMsg))
            if self.welcome == False:
                content.insert(0, welcomeComment)
                self.welcome = True
            else:
                comment = content.contents[0]
                if type(comment) == Comment:
                    comment.replace_with(welcomeComment)
            HTML.seek(0)
            HTML.truncate(0)
            HTML.write(content.prettify())

    def updateHead(self):
        with open(self.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            head = content.head
            headTemplate = f"""
                        <meta charset="utf-8" />
                        <meta http-equiv="Content-Language" content="zh-CN" />
                        <meta name="language" content="zh-CN" />
                        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

                        <title>Woodash * {self.title}</title>
                        <meta name="description" content="技术与美学与数字花园" />
                        <meta name="author" content="woodash" />
                        <meta name="date" content="{self.date}" />

                        <meta name="woodash-welcome" content="{self.welcome}">
                        <meta name="woodash-title" content="{self.title}">
                        <meta name="woodash-category" content="{self.category}">
                        <meta name="woodash-note" content="{self.note}">
                        <meta name="woodash-tucao" content="{self.tucao}">
                        <meta name="woodash-scene" content="{self.scene}">
                        
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
            head.append(BeautifulSoup(dedent(headTemplate), "html.parser"))
            # 写入
            HTML.seek(0)
            HTML.truncate(0)
            HTML.write(content.prettify())

    # def addReturn(self):
    #     if self.category == "index":
    #         return

    #     link = "index.html"
    #     categoryName = categoryDict[self.category]

    #     with open(self.path, "r+", encoding="utf-8") as HTML:
    #         content = BeautifulSoup(HTML, "html.parser")
    #         article = content.body.article
    #         back = f"""<a href={link} id="return">{categoryName}</a>"""
    #         article.insert(0, back)

    #         HTML.seek(0)
    #         HTML.truncate(0)
    #         HTML.write(content.prettify())


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


def updateIndex(_pages):
    def updateCategoryIndex(_pages):
        for category in categorys:
            pagesInCategory = (page for page in _pages if page.category == category)
            article = ""
            for page in pagesInCategory:
                if page.category == "index":
                    continue
                article += f"""
                          <article>
                            <div class="article-info">
                              <h2 class="article-title">
                                <a href="{page.path.name}">
                                  {page.title}
                                </a>
                              </h2>
                              <p class="article-date">
                                {page.date.replace("-", ".")}.{page.scene}
                              </p>
                            </div>
                            <p class="article-summary">
                              {page.note}
                            </p>
                          </article>
                          """
            categoryIndex = Path(f"{category}/index.html")
            with open(categoryIndex, "r+", encoding="utf-8") as HTML:
                content = BeautifulSoup(HTML, "html.parser")
                target = content.body.main
                target.clear()
                target.append(BeautifulSoup(dedent(article), "html.parser"))
                HTML.seek(0)
                HTML.truncate(0)
                HTML.write(content.prettify())

    def updateMainIndex(_pages):
        mainIndex = Path("index.html")
        article = ""
        for page in _pages:
            if page.category == "index":
                continue
            article += f"""
                      <article>
                        <h1 class="article-title">
                          <a href="{page.path}">
                            {page.title}
                          </a>
                        </h1>
                        <p class="article-date">
                          {page.date.replace("-", ".")}.{page.scene}
                        </p>
                        <p class="article-summary">
                          {page.note}
                        </p>
                      </article>
                      """
        with open(mainIndex, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            target = content.body.main.find(id="column-right")
            target.clear()
            target.append(BeautifulSoup(dedent(article), "html.parser"))
            HTML.seek(0)
            HTML.truncate(0)
            HTML.write(content.prettify())

    updateCategoryIndex(_pages)
    updateMainIndex(_pages)


pages = getPages()

for page in pages:
    page.setAttrs()
    page.addWelcome()
    page.updateHead()

pages.sort(key=lambda x: x.date, reverse=True)
updateIndex(pages)
