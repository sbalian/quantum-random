# Run ruff linter
lint:
    uv run ruff check .

# Run pyright type checker
type-check:
    uv run pyright

# Run tests (extra args are passed to pytest)
[env("QRANDOM_API_KEY", "key")]
test *args:
    uv run pytest {{ args }}
