import markdown
from lxml.builder import ElementMaker
from lxml.etree import CDATA

from api.schemas import Post

NSMAP = {
    "atom": "http://www.w3.org/2005/Atom",
}
E = ElementMaker(nsmap=NSMAP)
A = ElementMaker(namespace="http://www.w3.org/2005/Atom")


class Feed:
    def __init__(
        self,
        title: str,
        link: str,
        feed_link: str,
        posts: list[Post],
        description: str = "",
    ):
        self.title = title
        self.link = link
        self.feed_link = feed_link
        self.description = description
        self.posts = posts

    @staticmethod
    def create_item(post: Post):
        return E.item(
            E.title(post.title),
            E.description(
                CDATA(markdown.markdown(post.body, extensions=["fenced_code"]))
            ),
            E.pubDate(post.created.to_rfc822_string()),
            E.guid(f"https://blog.thoughtbank.app/posts/{post.id}"),
        )

    def to_etree(self):
        return E.rss(
            E.channel(
                E.title(self.title),
                A.link(
                    href=self.feed_link,
                    rel="self",
                    type="application/rss+xml",
                ),
                E.link(self.link),
                E.description(self.description),
                *map(self.create_item, self.posts),
            ),
            version="2.0",
        )
