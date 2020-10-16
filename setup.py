# type: ignore

# NOTE: We need to include this file even though we're using the
#       newer "setup.cfg" + "pyproject.toml" approach, since some
#       tools (notably, "pex") rely on the existince of "setup.py"

import setuptools


setuptools.setup()
