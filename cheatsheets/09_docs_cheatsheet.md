# Google vs NumPy docstrings

## Practical Guidelines: When to Choose Which

Choose **Google Docstrings** if:

- You are building web services (FastAPI, Django, Flask), CLI tools, or general scripts.
- Your team values compact code and reads docstrings primarily inside the code editor.
- Functions have simple parameter signatures with short descriptions.

Choose **NumPy Docstrings** if:

- You are building data analysis, machine learning, or scientific libraries (pandas, scipy, scikit-learn).
- Your parameters require detailed mathematical explanations, array shapes (e.g., (N, D) tensors), or multi-line types.
- You heavily generate rendered HTML documentation using tools like Sphinx.

**Golden Rule**:

- Pick one format and stick to it consistently across the entire codebase or repository.
- If using Sphinx, enable sphinx.ext.napoleon to automatically parse both Google and NumPy docstrings into HTML docs.

## Examples to copy-paste

### Google

```python
def calculate_growth_rate(
    initial_value: float, final_value: float, time_period: int
) -> float:
    """Calculates the compound annual growth rate (CAGR).

    Args:
        initial_value: The starting monetary or metric value (must be > 0).
        final_value: The ending monetary or metric value.
        time_period: Number of periods (e.g., years) between start and end.

    Returns:
        The growth rate as a float (e.g., 0.05 for 5%).

    Raises:
        ValueError: If `initial_value` or `time_period` is less than or equal to zero.
    """
    if initial_value <= 0 or time_period <= 0:
        raise ValueError("initial_value and time_period must be positive.")

    return (final_value / initial_value) ** (1 / time_period) - 1
```

### NumPy

```python
def calculate_growth_rate(
    initial_value: float, final_value: float, time_period: int
) -> float:
    """Calculates the compound annual growth rate (CAGR).

    Parameters
    ----------
    initial_value : float
        The starting monetary or metric value (must be > 0).
    final_value : float
        The ending monetary or metric value.
    time_period : int
        Number of periods (e.g., years) between start and end.

    Returns
    -------
    float
        The growth rate as a float (e.g., 0.05 for 5%).

    Raises
    ------
    ValueError
        If `initial_value` or `time_period` is less than or equal to zero.
    """
    if initial_value <= 0 or time_period <= 0:
        raise ValueError("initial_value and time_period must be positive.")

    return (final_value / initial_value) ** (1 / time_period) - 1
```
