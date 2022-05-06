from typing import Union

import pendulum


def to_rfc7231_format(dt: Union[pendulum.DateTime, str]) -> str:
    if isinstance(dt, str):
        dt = pendulum.parse(dt)
    return dt.in_tz("GMT").format("ddd, DD MMM YYYY HH:mm:ss zz")
