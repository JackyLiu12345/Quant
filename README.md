# Quant

Lightweight scaffold for quantitative alpha research/backtesting that keeps factor scripts in a strike-style framework.

## Repository layout

- `config_template/`: reusable XML config templates for demo jobs and data loading
- `pnl/`: output placeholder for generated pnl artifacts
- `source_ref/`: optional research/reference notes
- `strike/`: local compatibility layer (`AlphaBase`, `ConfigNode`, `DataRegister`) for demo runs
- `tool/`: config parsing and runner entry helpers
- `alpha5dr.py`, `txliumom01.py`, `txliusize01.py`: factor mining scripts using strike-style signatures
- `alphatest.py`, `alphatest2.py`: sample standalone runners
- `config.xml`, `config.load.xml`: default runnable config files
- `run.py`: entrypoint for configured jobs

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

No required external dependency is needed for demo mode. If `numpy` is installed, factors use it automatically.

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

- Replace synthetic data generation in `strike/dataregister.py` with your private data loader.
- Keep factor script structure (`create(id, cfg, dr)`, `AlphaBase`, `generate(alpha_vec, di)`) aligned with your internal strike framework.
- XML job options can be extended in `config.xml` and parsed by `tool/framework.py`.
