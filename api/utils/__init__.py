import re
from collections import defaultdict
from functools import singledispatch

import pendulum


@singledispatch
def to_rfc7231_format(dt) -> str:
    raise NotImplementedError(f"cannot format {dt}")


@to_rfc7231_format.register
def _(dt: pendulum.DateTime):
    return dt.in_tz("GMT").format("ddd, DD MMM YYYY HH:mm:ss zz")


@to_rfc7231_format.register
def _(dt: str):
    return to_rfc7231_format(pendulum.parse(dt))


REQUEST_DIRECTIVES = {
    "max-age",
    "max-stale",
    "min-fresh",
    "no-cache",
    "no-store",
    "no-transform",
    "only-if-cached",
    "stale-if-error",
}


class DirectiveMap(defaultdict):
    def __init__(self, directives_str: str | None, *args, **kwargs):
        super().__init__(bool, *args, **kwargs)

        if directives_str:
            for d in re.sub(r"\s", "", directives_str.casefold()).split(","):
                key, _, value = d.partition("=")
                self[key] = value or True

    def __missing__(self, key):
        if key not in REQUEST_DIRECTIVES:
            raise KeyError(key)

        return super().__missing__(key)
