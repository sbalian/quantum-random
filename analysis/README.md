# Analysis

To run the analysis, [install uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
cd analysis
uv sync --all-extras --all-groups
```

Next, run the script to generate the plot in `uniform.md`:

```bash
uv run generate_plot.py
```

The output is written to `random.png`.
