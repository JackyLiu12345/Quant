# Quant

Momentum factor mining starter files:

1. Generate sample market data:
   `python generate_sample_prices.py --output sample_prices.csv`
2. Run momentum factor mining:
   `python alpha5dr.py --input sample_prices.csv --output-dir outputs`

Input CSV format requires at least:
- `date`
- `asset`
- `close`