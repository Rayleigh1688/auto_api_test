import re
from config import context

def replace_vars(text, vars_dict):
    if not isinstance(text, str):
        return text
    pattern = re.compile(r"{{(.*?)}}")
    return pattern.sub(lambda m: str(vars_dict.get(m.group(1).strip(), m.group(0))), text)

def render_with_context(obj):
    if isinstance(obj, str):
        return replace_vars(obj, context.GLOBAL_VARS)
    elif isinstance(obj, dict):
        return {k: render_with_context(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [render_with_context(i) for i in obj]
    else:
        return obj
