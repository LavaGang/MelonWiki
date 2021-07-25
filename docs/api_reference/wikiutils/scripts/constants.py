from pathlib import Path

api_reference_path = Path(__file__).parent.parent.parent
common_path = Path.joinpath(Path(__file__).parent.parent, "common").resolve()
constructors_path = Path.joinpath(Path(__file__).parent.parent, "constructors").resolve()
fields_path = Path.joinpath(Path(__file__).parent.parent, "fields").resolve()
properties_path = Path.joinpath(Path(__file__).parent.parent, "properties").resolve()
methods_path = Path.joinpath(Path(__file__).parent.parent, "methods").resolve()
methods_path = Path.joinpath(Path(__file__).parent.parent, "methods").resolve()