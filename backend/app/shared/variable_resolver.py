import re


def resolve_variables(template: str, context: dict[str, str]) -> str:
    """Replace {{var}} placeholders with values from context."""
    return re.sub(
        r"\{\{([\w ]+)\}\}",
        lambda m: context.get(m.group(1).strip(), m.group(0)),
        template,
    )
