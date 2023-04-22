import typing

import yaml
from fastapi.responses import Response
from lxml import etree


class YAMLResponse(Response):
    media_type = "application/yaml"

    def render(self, content: typing.Any) -> bytes:
        return yaml.dump(content, sort_keys=False, Dumper=yaml.SafeDumper, encoding="utf-8")


class RSSResponse(Response):
    media_type = "application/rss+xml"

    def render(self, content: typing.Any) -> bytes:
        return etree.tostring(content, xml_declaration=True, encoding="utf-8")
