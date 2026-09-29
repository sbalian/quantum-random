# quantum-random

Python library for quantum random numbers, fetched from the [ANU Quantum Random Numbers Server](https://quantumnumbers.anu.edu.au).

## Commands

```bash
# Install with all extras and dev dependencies
uv sync --all-extras --all-groups

# Run tests (sets a dummy QRANDOM_API_KEY; extra args go to pytest)
just test

# Type check
just type-check

# Lint
just lint
```

Recipes are defined in `justfile`.

## Structure

- `src/qrandom/` — library source
  - `_api.py` — HTTP client for the ANU API
  - `_generator.py` — `random.Random` subclass backed by quantum randomness
  - `_cli.py` — `qrandom-init` CLI for storing the API key
  - `_util.py` — XDG config path utilities
  - `numpy.py` — optional numpy/randomgen integration
- `tests/` — pytest tests
- `analysis/` — notebooks/scripts (not part of the package)

## CI

GitHub Actions runs tests across Python 3.10–3.14 on Linux, macOS, and Windows, plus a lint job pinned to 3.12. Python versions are managed via `UV_PYTHON` and `UV_MANAGED_PYTHON=1` env vars set at the job level. CI installs `just` via `extractions/setup-just` and runs the same recipes.

## Notes

- API key is read from `QRANDOM_API_KEY` env var or a config file (`qrandom.ini`) in `QRANDOM_CONFIG_DIR` (defaults to XDG config home)
- Use `click.unstyle()` on `result.output` in CLI test assertions to handle ANSI codes consistently across platforms
