## Overview

`dynamic-cast` is a Python utility that simplifies dynamic type conversions for function arguments and return values. Using `@dynamic_cast` and `@async_cast` decorators, this module automatically casts inputs to match type annotations, enabling flexibility in function usage and compatibility with a variety of data types.

## Key Features

- **Automatic Casting**: Convert input arguments and return values based on type annotations.
- **Support for Sync and Async Functions**: Both synchronous (`@dynamic_cast`) and asynchronous (`@async_cast`) functions are supported.
- **Iterables and Generic Types**: Handle common Python iterables and generics like `List`, `Dict`, and `Tuple`.
- **Robust Type Compatibility**: Compatible with both simple and complex data types, including callable types and class instances.

## Installation

Install `dynamic-cast` via pip:

```bash
pip install dynamic-cast
```

## Quick Start

To start dynamically casting arguments and return types in your functions, simply apply the `@dynamic_cast` or `@async_cast` decorator as shown below.

### Basic Examples

#### Synchronous Functions

```python
# Import the decorators
from dynamic_cast import dynamic_cast

@dynamic_cast
def sum_numbers(a: int, b: int) -> int:
    return a + b

# Use the function with mixed types
assert sum_numbers(1, 2) == 3
assert sum_numbers("3", "4") == 7
```

In this example, `sum_numbers` will automatically cast string inputs to integers to meet the specified type annotations.

#### Asynchronous Functions

```python
from dynamic_cast import async_cast
import asyncio

@async_cast
async def async_add(a: float, b: int) -> float:
    return a + b

# Call the function asynchronously
result = asyncio.run(async_add("1.5", 2))
assert result == 3.5
```

### Additional Examples

#### Mixed-Type Arithmetic

```python
@dynamic_cast
def multiply(a: int, b: int) -> int:
    return a * b

@dynamic_cast
def subtract(x: float, y: float) -> float:
    return x - y

assert multiply(3, "4") == 12
assert subtract("10.5", "2.5") == 8.0
```

Here, the decorators allow `multiply` and `subtract` to accept both strings and numbers by casting them as necessary.

#### String Manipulation

```python
@dynamic_cast
def concatenate(x: str, y: str) -> str:
    return x + y

@async_cast
async def async_upper(s: str) -> str:
    return s.upper()

assert concatenate("Hello, ", "World!") == "Hello, World!"
assert concatenate(1, 2) == "12"  # Automatically converts numbers to strings
assert asyncio.run(async_upper("hello")) == "HELLO"
```

### Working with Containers

```python
from typing import List, Dict, Tuple

@dynamic_cast
def advanced_function(nums: List[int], mappings: Dict[str, float]) -> Tuple[str, int]:
    return str(sum(nums)), len(mappings)

assert advanced_function(["1", "2", "3"], {"pi": "3.14", "e": "2.71"}) == ("6", 2)
```

This example demonstrates how `dynamic_cast` handles common container types, automatically converting inputs to match the function’s type annotations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
