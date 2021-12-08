# Deliveroo Webscraping

To start running the scraper:
```bash
python main.py
```
It also contains interactive cells if you wish to rerun the scraper without opening a new instance of the browser.

## Testing
to run all the tests, edit `run_tests.sh` to replace `python3` with your python version e.g. `python3.8`, then run the following:
```bash
chmod +x run_tests.sh
./run_tests.sh
```
## Pushing updates

To fix a bug or add a new feature (basically any updates), follow the steps:

1. Pull from `dev` branch.
2. Checkout to new branch under `{feature_name}` or `fix_{bug_name}`.
3. Once you are satisfied with the changes, push them.
4. Open a new pull request to `dev` with title matching branch name. If possible, describe your changes in the request.
5. Lastly, assign a reviewer!