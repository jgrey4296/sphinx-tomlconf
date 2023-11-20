"""
    sphinxcontrib.tomlconf
    ~~~~~~~~~~~~~~~~~~~~~~

    Adding toml-based configuration for sphinx

    :copyright: Copyright 2017 by jgrey <Your email>
    :license: BSD, see LICENSE for details.
"""

import pbr.version

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa

__version__ = pbr.version.VersionInfo(
    'tomlconf').version_string()


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    return {'version': __version__, 'parallel_read_safe': True}
