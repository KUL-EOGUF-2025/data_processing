# Data Processing Pipeline

This repository contains Jupyter notebooks and scripts for data processing. The notebooks should be executed in the order they are numbered.

## Setup

This project uses `uv`, make sure to use version 3.10.12 or the parquet files will not work.

```bash
pip install uv
```

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

```bash
uv pip install -r requirements.txt
```