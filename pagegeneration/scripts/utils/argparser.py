import copy
from typing import Type, Union 

class ArgWrapper:
    def __init__(self, name: str, param_names: list[str], params_can_repeat: bool = False):
        self.name = name
        self.params_can_repeat = params_can_repeat
        self.template = {key: None for key in param_names}
        self.template_keys = param_names
        self.exists = False
        if not self.params_can_repeat:
            self.params = copy.deepcopy(self.template)
        else:
            self.params = []

    def __repr__(self):
        return f"{self.name}, {self.params_can_repeat}, {self.params}"

    def populate(self, args: list[str]):
        self.exists = True
        if self.params_can_repeat:
            self.params.append(self.template.copy())
            for i in range(len(args)):
                self.params[-1][self.template_keys[i]] = args[i]
        else:
            for i in range(len(args)):
                self.params[self.template_keys[i]] = args[i]
    
    @classmethod
    def get_arg_from_list(cls, args: list["ArgWrapper"], arg_name: str) -> Union["ArgWrapper", None]:
        for arg in args:
            if arg.name == arg_name:
                return arg
        return None
    
class ArgParentWrapper(ArgWrapper):
    def __init__(self, name: str, param_names: list[Union[Type[ArgWrapper], str]], params_can_repeat: bool = False):
        super().__init__(name, param_names, params_can_repeat)
        self.arg_wrappers = [val for val in param_names if isinstance(val, ArgWrapper)]
        self.template.clear()
        for param in param_names:
            if isinstance(param, ArgWrapper):
                self.template[param.name] = param
            else:
                self.template[param] = None
        if not self.params_can_repeat:
            self.params = copy.deepcopy(self.template)
        else:
            self.params = []
        self.template_keys = list(self.template.keys())

    def populate(self, args: list[str]):
        self.exists = True
        if self.params_can_repeat:
            self.params.append(copy.deepcopy(self.template))
        i = 0
        split_params = []
        current_arg = None
        for arg in args:
            parsed_arg = ArgWrapper.get_arg_from_list(self.arg_wrappers, arg)
            if parsed_arg:
                if current_arg and split_params != []:
                    if self.params_can_repeat:
                        self.params[-1][current_arg.name].populate(split_params)
                    else:
                        self.params[current_arg.name].populate(split_params)
                current_arg = parsed_arg
                split_params.clear()
            elif current_arg:
                split_params.append(arg)
            else:
                if self.params_can_repeat:
                    self.params[-1][self.template_keys[i]] = arg
                else:
                    self.params[self.template_keys[i]] = arg
            i += 1

        if self.params_can_repeat:
            self.params[-1][current_arg.name].populate(split_params)
        else:
            self.params[current_arg.name].populate(split_params)

class ArgParser:
    def __init__(self, args: list[str], desired_args: list[ArgWrapper]):
        self.parsed_args = ArgParser.parse_args(args, desired_args)
        self.args = args
    
    def __repr__(self):
        return f"{self.parsed_args}, {self.args}"

    @classmethod
    def parse_args(cls, args: list[str], desired_args: list[ArgWrapper]) -> Union[list[ArgWrapper], None]:
        split_params = []
        current_arg = None
        for arg in args:
            parsed_arg = ArgWrapper.get_arg_from_list(desired_args, arg)
            if parsed_arg:
                if current_arg and split_params != []:
                    current_arg.populate(split_params)
                current_arg = parsed_arg
                split_params.clear()
            elif current_arg:
                split_params.append(arg)
        if current_arg and split_params != []:
            current_arg.populate(split_params)
        return desired_args
                