This is an archive of Python source tarballs from <https://www.python.org/ftp/>,
primarily for use with `pyenv` (<https://github.com/pyenv/pyenv>) on a
disconnected network.

The `python/` directory is a mirror of a subset of
<https://www.python.org/ftp/python/>, including just the source tarball for each
mirrored version of Python.

Use in one of two ways:

- Manually copy Python source tarballs into `~/.pyenv/cache/` (flattening into
  this single directory):

      mkdir -p ~/.pyenv/cache
      for v in 3.5.10 3.6.9 3.7.13; do
          cp .../pythonsource/python/$v/Python* ~/.pyenv/cache
      done

- Set ``pyenv`` environment variables to point to `pythonsource/python/` using a
  `file://` URL:

      cd .../pythonsource/
      export PYTHON_BUILD_MIRROR_URL=file://$PWD/python
      export PYTHON_BUILD_MIRROR_URL_SKIP_CHECKSUM=1

      # Now may install any mirrored version:
      pyenv install 3.7.13

Setup ``pyenv`` according to <https://github.com/pyenv/pyenv/README.md>.
Alternatively, place the below shell function into `~/.profile` (or similar) to
selectively activate `pyenv` support on-demand (which can avoid problems when
trying to compile tools like Vim that expect to find only the system Python):

```sh
# pyenv support.
pyenvactivate() {
    if [ -d "$HOME/.pyenv" ]; then
        export PYENV_ROOT="$HOME/.pyenv"
        PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init --path)"
        eval "$(pyenv init -)"
    else
        echo "Missing $HOME/.pyenv; can't activate"
        return 1
    fi
}
```

Use `pyenvactivate` before any `pyenv install x.y.z` operation.
