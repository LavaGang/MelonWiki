from typing import Union

class ArgWrapper:
    def __init__(self, name: str, param_names: list[str], params_can_repeat: bool = False):
        self.name = name
        self.params_can_repeat = params_can_repeat
        self.template = {key: None for key in param_names}
        self.template_keys = param_names
        self.exists = False
        if not self.params_can_repeat:
            self.params = self.template
        else:
            self.params = []

    def __repr__(self):
        return f"{self.name}, {self.params_can_repeat}, {self.params}"

    @classmethod
    def get_arg_from_list(cls, args: list["ArgWrapper"], arg_name: str) -> Union["ArgWrapper", None]:
        for arg in args:
            if arg.name == arg_name:
                return arg
        return None
    
class ArgParser:
    def __init__(self, args: list[str], desired_args: list[ArgWrapper]):
        self.parsed_args = ArgParser.parse_args(args, desired_args)
        self.args = args
    
    def __repr__(self):
        return f"{self.parsed_args}, {self.args}"

    @classmethod
    def parse_args(cls, args: list[str], desired_args: list[ArgWrapper]) -> Union[list[ArgWrapper], None]:
        state = "args"
        current_arg = None
        index = 0
        for arg in args:
            parsed_arg = ArgWrapper.get_arg_from_list(desired_args, arg)
            if parsed_arg:
                current_arg = parsed_arg
                current_arg.exists = True
                index = 0
            elif current_arg:
                try:
                    if current_arg.params_can_repeat:
                        adjusted_index = index % len(current_arg.template)
                        if adjusted_index == 0:
                            current_arg.params.append(current_arg.template.copy())
                        current_arg.params[-1][current_arg.template_keys[adjusted_index]] = arg
                    else:
                        current_arg.params[current_arg.template_keys[index]] = arg
                    index += 1
                except IndexError as err:
                    print(f"Failed to populate arg params of arg {current_arg.name}")
        return desired_args
                

