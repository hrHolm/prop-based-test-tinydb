# prop-based-test-tinydb
## Setup
Install dependencies:
```bash
pip install -r requirements.txt
```
Run tests with:
```bash
pytest --hypothesis-show-statistics
```
## Development
Pytest will only run methods prefixed with `test_`, e.g. `test_decode_inverts_encode(s)`