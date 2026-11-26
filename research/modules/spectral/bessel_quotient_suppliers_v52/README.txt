Read main.tex for BQS1--BQS23 and contracts.json for completed and retained scopes.
Draft check: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt
Build source/proof bindings: python build_metadata.py
Check existing bindings without rebuilding: python verify_hashes.py
Source declarations identify exact targets; the human proofs supply the mathematics.
