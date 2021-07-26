from pathlib import Path

page_data_path = Path.joinpath(Path(__file__).parent.parent.parent, "pagedata").resolve()
api_reference_path = Path.joinpath(Path(__file__).parent.parent.parent.parent, "docs", "api_reference").resolve()
templates_path = Path.joinpath(Path(__file__).parent.parent.parent, "templates").resolve()
common_path = Path.joinpath(templates_path, "common").resolve()
constructors_path = Path.joinpath(templates_path, "constructors").resolve()
fields_path = Path.joinpath(templates_path, "fields").resolve()
properties_path = Path.joinpath(templates_path, "properties").resolve()
methods_path = Path.joinpath(templates_path, "methods").resolve()
operators_path = Path.joinpath(templates_path, "operators").resolve()

# there is almost certainly a better way to do this but eh
def convert_to_api_reference_path(*path) -> str: 
    return _join_and_verify_internal(path, api_reference_path)

def convert_to_pagedata_path(*path) -> str:   
    return _join_and_verify_internal(path, page_data_path)

def join_and_verify(start_path: str, *path) -> str:
    return _join_and_verify_internal(path, start_path)


def _join_and_verify_internal(path: list[str], start_path: str) -> str:
    current_path = start_path
    for path_component in path:
        current_path = Path.joinpath(current_path, path_component)
        if not Path.exists(current_path):
            Path.mkdir(current_path)
    
    return current_path