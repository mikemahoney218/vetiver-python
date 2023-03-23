import sys
import warnings
from pathlib import Path

from .write_fastapi import write_app
from .attach_pkgs import load_pkgs, get_board_pkgs
from .vetiver_model import VetiverModel


def vetiver_write_docker(
    app_file: str = "app.py",
    path: str = "./",
    rspm_env: bool = False,
    host: str = "0.0.0.0",
    port: str = "8080",
):

    warnings.warn(
        "vetiver_write_docker will be replaced by write_docker in v1.0.0",
        DeprecationWarning,
    )

    return write_docker(
        app_file=app_file, path=path, rspm_env=rspm_env, host=host, port=port
    )


def write_docker(
    app_file: str = "app.py",
    path: str = "./",
    rspm_env: bool = False,
    host: str = "0.0.0.0",
    port: str = "8080",
):
    """Writes a Dockerfile to run VetiverAPI in a container

    Parameters
    ----------
    app_file: str
        File containing VetiverAPI to be deployed into container
    path: str
        Path to save Dockerfile
    rspm_env: bool
        Whether or not Posit Package Manager should be used
    host: str
        Host address to run VetiverAPI from Dockerfile
    port: str
        Port to run VetiverAPI from Dockerfile

    Examples
    -------
    >>> import vetiver
    >>> import tempfile
    >>> import pins
    >>> tmp = tempfile.TemporaryDirectory()
    >>> board = pins.board_temp(allow_pickle_read=True)
    >>> X, y = vetiver.get_mock_data()
    >>> model = vetiver.get_mock_model().fit(X, y)
    >>> v = vetiver.VetiverModel(model, "my_model", prototype_data = X)
    >>> vetiver.vetiver_pin_write(board, v)
    >>> vetiver.write_app(board,
    ...     "my_model",
    ...     file = tmp.name + "/app.py") # need file for model
    >>> vetiver.write_docker(app_file = "app.py", path = tmp.name)
    """
    py_version = str(sys.version_info.major) + "." + str(sys.version_info.minor)

    if rspm_env:
        rspm = "\nRUN pip config set global.index-url https://colorado.rstudio.com/rspm/pypi/latest/simple"  # noqa
    else:
        rspm = ""

    docker_script = f"""# # Generated by the vetiver package; edit with care
# start with python base image
FROM python:{py_version}

# create directory in container for vetiver files
WORKDIR /vetiver

# copy  and install requirements
COPY vetiver_requirements.txt /vetiver/requirements.txt

#{rspm}
RUN pip install --no-cache-dir --upgrade -r /vetiver/requirements.txt

# copy app file
COPY {app_file} /vetiver/app/{app_file}

# expose port
EXPOSE {port}

# run vetiver API
CMD ["uvicorn", "app.app:api", "--host", "{host}", "--port", "{port}"]
"""

    f = open(Path(path, "Dockerfile"), "x")
    f.write(docker_script)


def prepare_docker(
    board,
    pin_name: str,
    path: str = "./",
    version=None,
    rspm_env: bool = False,
    host: str = "0.0.0.0",
    port: str = "8080",
):
    """Create all files needed for Docker

    Parameters
    ----------
    board :
        Pin board for model
    pin_name : str
        Name of pin
    path :
        Path to output
    version :
        Pin version to be used
    rspm_env: bool
        Whether or not Posit Package Manager should be used
    host: str
        Host address to run VetiverAPI from Dockerfile
    port: str
        Port to run VetiverAPI from Dockerfile

    Examples
    -------
    >>> import vetiver
    >>> import tempfile
    >>> import pins
    >>> tmp = tempfile.TemporaryDirectory()
    >>> board = pins.board_temp(allow_pickle_read=True)
    >>> X, y = vetiver.get_mock_data()
    >>> model = vetiver.get_mock_model().fit(X, y)
    >>> v = vetiver.VetiverModel(model, "my_model", prototype_data = X)
    >>> vetiver.vetiver_pin_write(board, v)
    >>> vetiver.prepare_docker(board = board, pin_name = "my_model", path = tmp.name)

    Notes
    ------
    This function uses `vetiver.get_board_pkgs(board)` for generating requirements.
    For more complex use cases, call `write_docker()`, `load_pkgs()`, and
    `write_app()` individually.
    """

    v = VetiverModel.from_pin(board=board, name=pin_name, version=version)

    write_app(
        board=board, pin_name=pin_name, version=version, file=Path(path, "app.py")
    )

    load_pkgs(v, path=Path(path, "vetiver_"), packages=get_board_pkgs(board))

    write_docker(path=path, rspm_env=rspm_env, host=host, port=port)
