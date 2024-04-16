from pathlib import Path
from textwrap import dedent, indent
from bs4 import BeautifulSoup
from bs4 import Comment
from bs4.formatter import HTMLFormatter


categorys = ["notes", "weekly", "essays", "experience", "records"]
categoryDict = {
    "essays": "杂谈",
    "weekly": "周报",
    "experience": "体验",
    "records": "琐记",
    "notes": "笔记",
}
attrDict = {
    "note": "woodash-note",
    "tucao": "woodash-tucao",
    "scene": "woodash-scene",
    "date": "date",
}

ignoreList = ["半燃其零・钻木求火码后记"]

directory = Path(".")


class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v


class Page:
    def __init__(
        self,
        title="",
        category="",
        note="",
        tucao="",
        scene="",
        date="",
        path="",
        style="",
    ):
        self.title = title
        self.category = category
        self.note = note
        self.tucao = tucao
        self.scene = scene
        self.date = date

        self.path = path
        self.style = style

    def setAttrs(self):
        def setStyles(self, _head):
            head = _head
            styleList = head.find_all("link", rel="stylesheet")
            styleList = map(str, styleList)
            self.style = styleList

        def setTitle(self):
            self.title = Path(self.path).stem

        def setSummaryForWeekly(self, _body):
            if self.category and self.category != "weekly":
                return

            titles = _body.find_all("h2")
            titles = map(lambda x: x.string.strip(), titles)
            ignoreList = ["索引", "生活", "摘录", "网页", "创作", "图像", "结"]
            summary = [title for title in titles if title not in ignoreList]
            self.note = "/".join(summary)

        def setForIndex(self):
            if Path(self.path).stem != "index":
                return

            def setCategoryForIndex(self):
                self.category = "index"

            def setTitleForIndex(self):
                categoryName = str(Path(self.path).parent)
                self.title = categoryDict[categoryName]

            setCategoryForIndex(self)
            setTitleForIndex(self)

        def setMeta(self, _head, _attrDict):
            head = _head
            attrDict = _attrDict
            attrs = (attr for attr in attrDict.keys())

            for attr in attrs:
                attrName = attrDict[attr]
                tag = head.find("meta", attrs={"name": attrName})
                if tag:
                    setattr(self, attr, tag["content"])

            if "index" in str(self.path):
                self.category = "index"

        with open(self.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            head = content.head
            body = content.body

            setTitle(self)
            setForIndex(self)
            setStyles(self, head)
            setSummaryForWeekly(self, body)
            setMeta(self, head, attrDict)

    def edit(self):

        def editHead(self, _head):
            def addWelcome(self, _head):
                welcomeMsg = """
                          欢迎来到花园杂乱无章的*苗圃*！
                          请随意看看吧。
                          """
                welcomeComment = Comment(dedent(welcomeMsg))
                hasComment = type(content.contents[0]) == Comment
                if not hasComment:
                    content.insert(0, welcomeComment)
                else:
                    comment = content.contents[0]
                    comment.replace_with(welcomeComment)

            def updateHead(self, _head):
                headTemplate = f"""
                                <meta charset="utf-8" />
                                <meta http-equiv="Content-Language" content="zh-CN" />
                                <meta name="language" content="zh-CN" />
                                <meta name="viewport" content="width=device-width, initial-scale=1.0" />

                                <title>Woodash * {self.title}</title>
                                <meta name="description" content="技术与美学与数字花园" />
                                <meta name="author" content="woodash" />
                                <meta name="date" content="{self.date}" />

                                <meta name="woodash-note" content="{self.note}">
                                <meta name="woodash-tucao" content="{self.tucao}">
                                <meta name="woodash-scene" content="{self.scene}">
                                
                                <link rel="icon" href="../images/favicon.ico" />
                                <link rel="preconnect" href="https://ik.imagekit.io" crossorigin />
                                """
                headTemplate = dedent(headTemplate)
                for style in self.style:
                    headTemplate += f"""{style}"""
                    headTemplate += "\n"

                headTemplate += dedent(
                    f"""
                            <script defer src="../scripts/article/setImageSize.js"></script>
                            """
                )
                headTemplate = indent(headTemplate, "  ")
                head.clear()
                head.append((headTemplate))

            head = _head

            updateHead(self, head)
            addWelcome(self, head)

        def editBody(self, _body, _ignoreList):
            if self.category == "index":
                return
            if self.title in _ignoreList:
                return

            def setDate(self, _body):
                dateTag = _body.find(id="article-header-date")
                dateTag.string = self.date.replace("-", ".")

            def setBoard(self, _body, _categoryDict):
                link = "index.html"
                categoryName = _categoryDict[self.category]

                article = _body.article

                boardString = f"""
                            <a href="{link}" id="return">{categoryName}</a>
                            <img src="../images/asterisk.svg" id="asterisk" alt="" />
                        """
                boardString = indent(dedent(boardString), "    ")
                hasBoard = _body.find(id="board")
                if not hasBoard:
                    boardTag = content.new_tag("div", id="board")
                    boardTag.string = boardString
                    article.insert(0, boardTag)
                else:
                    board = article.find(id="board")
                    board.string = boardString
                
                board.prettify() 

            def setContents(self, _body):
                if self.category != "weekly":
                    return
                article = _body.article

                hasContents = article.find(id="索引")
                if not hasContents:
                    contentsTag = content.new_tag("section", id="索引", _class="level2")
                    articleHeader = article.header
                    articleHeader.insert_after(contentsTag)
                else:
                    contentsTag = article.find(id="索引")

                titles = article.find_all(class_="level2")
                contentsTag = content.new_tag("section")
                contentsTag["id"] = "索引"
                contentsTag["class"] = "level2"

                def turnIntoListItem(_titleTag):
                    name = _titleTag.h2.string.strip()
                    id = _titleTag.get("id")
                    string = f'<li><a href="#{id}">{name}</a></li>'
                    return string

                contentsTag.string = f"""<h2>索引</h2>
                                                <ul>
                                                {"".join(map(turnIntoListItem, titles))}
                                                </ul>"""

            body = _body

            setBoard(self, body, categoryDict)
            setContents(self, body)
            setDate(self, body)

        with open(self.path, "r+", encoding="utf-8") as HTML:
            content = BeautifulSoup(HTML, "html.parser")
            head = content.head
            body = content.body

            editHead(self, head)
            editBody(self, body, ignoreList)

            HTML.seek(0)
            HTML.truncate(0)
            HTML.write(content.prettify(formatter=None))


def getPages(_category, _directory):
    category = _category
    directory = _directory
    categoryDir = directory / category

    def createPage(_fileName, _category):
        a = Page(path=Path(_fileName), category=_category)
        a.setAttrs()
        a.edit()

        return Page(path=Path(_fileName), category=_category)

    pages = list(map(lambda x: createPage(x, category), categoryDir.iterdir()))
    pages.sort(key=lambda x: x.date, reverse=True)

    return pages


def updateCategoryIndex(_pages, _category):
    article = ""
    for page in _pages:
        newString = f"""
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
        article = "".join([article, newString])
    categoryIndex = Path(f"{_category}/index.html")
    with open(categoryIndex, "r+", encoding="utf-8") as HTML:
        content = BeautifulSoup(HTML, "html.parser")
        header = content.body.main.header

        oldArticles = content.find_all("article")
        for oldArticle in oldArticles:
            oldArticle.extract()

        header.insert_after(BeautifulSoup(dedent(article), "html.parser"))
        HTML.seek(0)
        HTML.truncate(0)
        HTML.write(content.prettify(formatter=None))


def updateMainIndex(_pages):
    mainIndex = Path("index.html")
    article = ""
    for page in _pages:
        newString = f"""
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
        article = "".join([article, newString])
    with open(mainIndex, "r+", encoding="utf-8") as HTML:
        content = BeautifulSoup(HTML, "html.parser")
        target = content.body.main.find(id="column-right")
        target.clear()
        target.append(BeautifulSoup(dedent(article), "html.parser"))
        HTML.seek(0)
        HTML.truncate(0)
        HTML.write(content.prettify(formatter=None))


allPages = []

for category in categorys:
    categoryPages = getPages(category, directory)
    # updateCategoryIndex(categoryPages, category)
    # allPages.extend(categoryPages)


# allPages.sort(key=lambda x: x.date, reverse=True)
# updateMainIndex(allPages)
