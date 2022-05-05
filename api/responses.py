import typing

import yaml
from fastapi.responses import Response


class YAMLResponse(Response):
    media_type = "application/yaml"

    def render(self, content: typing.Any) -> bytes:
        return yaml.dump(
            content, sort_keys=False, Dumper=yaml.SafeDumper, encoding="utf-8"
        )
