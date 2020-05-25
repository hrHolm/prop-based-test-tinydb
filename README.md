# Property Based Testing of TinyDB
## Content of the repository
*examples*: previous trials working with the Hypothesis framework, and official examples. 

*experiments*: evaluation done on the command generation of Hypothesis.

*htmlcov*: Coverage report

*tinydb*: TinyDB source code fetched from their repository, in order to compute coverage.

*root*: Property based tests, 'test_model_wo_bundle.py' and 'test_roundtrip.py'
## Setup
Install dependencies:
```bash
pip install -r requirements.txt
```
Run tests with:
```bash
pytest --hypothesis-show-statistics --ignore=examples 
```
Add '--cov-report html --cov' for coverage.
## Development
Pytest will only run methods prefixed with `test_`, e.g. `test_decode_inverts_encode(s)`

Preconditions are not supported when using bundles, read bottom of "Preconditions" in https://hypothesis.readthedocs.io/en/latest/stateful.html#preconditions
