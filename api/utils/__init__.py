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
