def convert_string_to_work_in_html(orig: str) -> str:
    return orig.replace("<", "&lt;").replace(">", "&gt;")

def convert_string_to_work_in_id(orig: str) -> str:
    return orig.replace("<", "lt").replace(">", "gt").replace(",", "").replace("(", "").replace(")", "").replace(" ", "-").lower()

def convert_string_to_work_in_link(orig: str) -> str:
    return orig.replace(" ", "%20")