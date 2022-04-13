To update:

- Clone (or update) `pyenv`:

    git clone https://github.com/pyenv/pyenv

- Activate `venv`:

    # One-time creation:
    python3 -m venv venv

    # Activation:
    . venv/bin/activate

- Install `httpx`:

    pip install httpx

- Double-check range of desired Python versions in `pythonsource.py`
  (`min_versions` list).

- Perform download:

    ./pythonsource.py

- Add any new source archives:

    git add python/
