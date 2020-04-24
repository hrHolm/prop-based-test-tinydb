# prop-based-test-tinydb
## Setup
Install dependencies:
```bash
pip install -r requirements.txt
```
Run tests with:
```bash
pytest --hypothesis-show-statistics --ignore=examples
```
## Development
Pytest will only run methods prefixed with `test_`, e.g. `test_decode_inverts_encode(s)`
test_model.py is WIP, but inserting faults is not being caught...