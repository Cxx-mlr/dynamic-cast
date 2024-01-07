---

# Dynamic Casting Utility

## Introduction

This Python module provides a dynamic casting utility that enables flexible casting of function arguments and return values based on type annotations. The utility is particularly useful for handling complex type conversions and ensuring compatibility between different data types.

## Installation

To use this dynamic casting utility, you can include it in your project by importing the `dynamic_cast` function from the module.

```python
from dynamic_cast import dynamic_cast
```

## Usage

### Basic Usage

The `dynamic_cast` function can be applied to functions to dynamically cast their arguments and return values based on the provided type annotations. It supports various scenarios, including handling iterable types, callables, and more.

```python
@dynamic_cast
def example_function(arg1: int, arg2: str) -> float:
    # Function logic here.
    return result
```

### Advanced Usage

For more advanced scenarios, the utility provides additional functionality, such as handling generic types, callable types, and class instances.

```python
@dynamic_cast
def advanced_function(arg1: List[int], arg2: Dict[str, float]) -> Tuple[str, int]:
    # Advanced function logic here.
    return result_tuple
```

## Examples.

### Dynamic Casting of Arguments.

```python
@dynamic_cast
def example_function(arg1: Union[str, int], arg2: List[float]) -> Tuple[str, List[int]]:
    # Function logic here
    return result_tuple
```

### Dynamic Casting of Class Instances

```python
class ExampleClass:
    @dynamic_cast
    def __init__(self, arg1: int, arg2: str) -> None:
        # Class initialization logic here
```

## Contributing

Feel free to contribute to the development of this dynamic casting utility. If you encounter any issues or have suggestions for improvement, please create an issue or submit a pull request.

## License

This dynamic casting utility is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---
