import inspect

def parse_positional_only(argument, annotation, args: list, kwargs: dict):
    print(f"positional only: {argument} {annotation}")
    args.append(annotation(argument))

def parse_positional_or_keyword(argument, annotation, args: list, kwargs: dict):
    print(f"positional or keyword: {argument} {annotation}")
    if "=" in argument:
        key, value = argument.split("=")
        args.append(annotation(value))
    else:
        args.append(annotation(argument))

def parse_var_positional(argument, annotation, args: list, kwargs: dict):
    print(f"var positional: {argument} {annotation}")
    args.extend([annotation(arg) for arg in argument])

def parse_keyword_only(argument, annotation, args: list, kwargs: dict):
    print(f"keyword only: {argument} {annotation}")
    key, value = argument.split("=")
    kwargs[key] = annotation(value)

def parse_var_keyword(argument, annotation, args: list, kwargs: dict):
    print(f"var keyword: {argument} {annotation}")
    for arg in argument:
        key, value = arg.split("=")
        kwargs[key] = annotation(value)

command_registry = {}

def command(func):
    command_registry[func.__name__] = func
    return func

def run_command(command: str):
    command_split = command.split(" ")

    preffix = command_split[0][0]
    command_name = command_split[0][1:]

    if command_name not in command_registry:
        print(f"Error: Command '{command_name}' not found.")
        return

    func = command_registry[command_name]

    signature = inspect.signature(func)
    parameters = signature.parameters

    index = 1
    args = list(); kwargs = dict()
    for pname, param in parameters.items():
        if index >= len(command_split):break

        argument = command_split[index]

        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            parse_positional_only(argument, param.annotation, args, kwargs)
            index += 1
        elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            parse_positional_or_keyword(argument, param.annotation, args, kwargs)
            index += 1
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            vars = []
            while index < len(command_split):
                argument = command_split[index]
                if "=" in argument:
                    break
                else:
                    vars.append(argument)
                    index += 1
            parse_var_positional(vars, param.annotation, args, kwargs)
        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
            parse_keyword_only(argument, param.annotation, args, kwargs)
            index += 1
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            vars = []
            while index < len(command_split):
                argument = command_split[index]
                vars.append(argument)
                index += 1
            parse_var_keyword(vars, param.annotation, args, kwargs)

    func(*args, **kwargs)

@command
def command(a: int, b: int, /, c: float, d: str, *args: int, e: int, **kwargs: int):
    print(f"running command({a=}, {b=}, {c=}, {d=}, {args=}, {e=}, {kwargs=})")

run_command("!command 1 0 c=3 4 5 6 7 e=8 f=9 g=10 h=-1 q=-99")