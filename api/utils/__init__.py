from functools import singledispatch

import pendulum


@singledispatch
def to_rfc7231_format(dt: pendulum.DateTime) -> str:
    return dt.in_tz("GMT").format("ddd, DD MMM YYYY HH:mm:ss zz")


@to_rfc7231_format.register
def _(dt: str) -> str:  # type: ignore[misc]
    dt_obj = pendulum.parse(dt)
    if not isinstance(dt_obj, pendulum.DateTime):
        raise ValueError("not datetime")
    return to_rfc7231_format(dt_obj)
