"""
    sphinxcontrib.tomlconf
    ~~~~~~~~~~~~~~~~~~~~~~

    Adding toml-based configuration for sphinx

    :copyright: Copyright 2023 by jgrey <Your email>
    :license: BSD, see LICENSE for details.
"""
from __future__ import annotations
import tomler
import sys
import pathlib as pl

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa

__version__ = "0.1"

def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    app.connect('config-inited', read_toml_config, priority=0)
    return {'version': __version__, 'parallel_read_safe': True}

def read_toml_config(app:Sphinx, config:Config) -> None:
    """ Read a sphinx config from a toml file """
    # TODO handle multiple toml files
    # TODO handle using [tools.sphinx...] in pyproject.toml
    confdir = pl.Path(config._raw_config['__file__']).parent
    toml_path = confdir / "sphinx.toml"
    namespace: dict[str, Any] = {}
    namespace['__toml_file__'] = str(toml_path)

    extensions = []

    # This makes it easy to retarget if loading from [tools.sphinx] in pyproject instead:
    data = tomler.load(toml_path).sphinx
    # Update the system path
    sys.path += [str(pl.Path(x).expanduser().absolute()) for x in data.paths.sys_paths or []]

    # Add general settings
    namespace.update(data.general.items())

    # Add paths
    namespace.update(data.paths)
    # Add templates
    namespace.update(data.templates.items())
    # Add patterns
    namespace.update(data.patterns.items())
    # add parse settings
    namespace.update(data.parsing.items())

    # add options
    namespace.update(data.options.items())
    # add highlighting
    namespace.update(data.highlight.items())
    # add reST settings
    namespace.update(data.reST.items())
    # add rst settings
    namespace.update(data.rst.items())
    # add nitpicky
    namespace.update(data.nitpicky.items())
    # add numfig
    namespace.update(data.numfig.items())
    # add math
    namespace.update(data.math.items())
    # add web
    namespace.update(data.web.items())
    # add docutils
    namespace.update(data.docutils.items())

    # add builders settings:
    for name, table in data.builder:
        namespace.update(table.items())

    # add extensions settings
    for name, table in data.ext:
        namespace.update(table.items())

    config._raw_config.update(namespace)
    if 'extensions' in data:
        config.extensions += data.extensions

    config.post_init_values()
    print("Updated config with toml info")
