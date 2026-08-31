import re


def normalize_endpoint(path: str) -> str:
    """
    Normalize dynamic URL path values.

    Example:
    /users/101 -> /users/{id}
    /products/25/reviews/7 -> /products/{id}/reviews/{id}
    """

    parts = path.strip("/").split("/")

    normalized_parts = []

    for part in parts:
        if not part:
            continue

        # Numeric path parameter
        if part.isdigit():
            normalized_parts.append("{id}")

        # UUID-like path parameter
        elif re.fullmatch(
            r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{12}",
            part,
        ):
            normalized_parts.append("{id}")

        else:
            normalized_parts.append(part)

    return "/" + "/".join(normalized_parts)