# Quant

Lightweight scaffold for quantitative alpha research/backtesting inspired by an internal strike-style workflow.

## Repository layout

- `config_template/`: reusable XML config templates for demo jobs and data loading
- `pnl/`: output placeholder for generated pnl artifacts
- `source_ref/`: optional research/reference notes
- `tool/`: minimal framework primitives (config parsing, synthetic data register, runner)
- `alpha5dr.py`: 5-day mean reversion alpha example
- `txliumom01.py`, `txliusize01.py`: optional placeholder alpha scripts
- `alphatest.py`, `alphatest2.py`: example standalone test runners
- `config.xml`, `config.load.xml`: default runnable config files
- `run.py`: entrypoint for executing configured jobs

## Setup

### Option 1: venv

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Option 2: conda

```bash
conda create -n quant python=3.11 -y
conda activate quant
```

No external package dependencies are required for this scaffold.

## Run a sample job

```bash
python run.py --config config.xml
```

You can also run sample scripts directly:

```bash
python alphatest.py
python alphatest2.py
```

## Extension notes

- Replace synthetic data generation in `tool/framework.py::DataRegister` with your private data loader.
- Keep XML structure but map `job`/`option` parsing to your internal strike-style orchestration layer.
- Add alpha modules using the same `create(alpha_id, cfg, dr)` entrypoint pattern.
