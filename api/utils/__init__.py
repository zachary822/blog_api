from pendulum import DateTime


def to_rfc7231_format(dt: DateTime) -> str:
    return dt.in_tz("GMT").format("ddd, DD MMM YYYY HH:mm:ss zz")
