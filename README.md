# snurt

```sh
# create env
python3 -m venv .venv

# activate env
source .venv/bin/activate

# install dependencies
poetry install --no-root

# add dependencies
poetry add <package-name>

# remove dependencies
poetry remove <package-name>

# update dependencies
poetry update

# run api
python3 -m src/server

# deactivate env
deactivate
```
