# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

# default setup. This is where you can add custom config values and so on.

if 'sphinx.ext.intersphinx' not in extensions:
    extensions.append('sphinx.ext.ifconfig')

def setup(app):
    app.add_config_value('audience', 'public', 'env')

