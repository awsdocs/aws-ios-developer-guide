# -*- coding: utf-8 -*-
#
# AWS Sphinx configuration file.
#
# For more information about how to configure this file, see:
#
# https://w.amazon.com/index.php/AWSDevDocs/Sphinx
#

#
# General information about the project.
#

# Optional service/SDK name, typically the three letter acronym (TLA) that
# represents the service, such as 'SWF'. If this is an SDK, you can use 'SDK'
# here.
service_name = u'Mobile SDK'

# The long version of the service or SDK name, such as "Amazon Simple Workflow
# Service", "AWS Flow Framework for Ruby" or "AWS SDK for Java"
service_name_long = u'AWS ' + service_name

# The landing page for the service documentation.
service_docs_home = u'http://aws.amazon.com/documentation/mobile-sdk/'

project = u'iOS Developer Guide'

# A short description of the project.
project_desc = u'%s %s' % (service_name_long, project)

# the output will be generated in latest/<project_basename> and will appear on
# the web using the same basename.
project_basename = 'mobile/sdkforios/developerguide'

# This name is used as the manual / PDF name. Don't include the extension
# (.pdf) here.
man_name = 'aws-ios-dg'

# The language for this version of the docs. Typically 'en'. For a full list of
# values, see: http://sphinx-doc.org/config.html#confval-language
language = u'en'

# Whether or not to show the PDF link. If you generate a PDF for your
# documentation, set this to True.
show_pdf_link = True

# Whether or not to show the language selector
show_lang_selector = True

# The link to the top of the doc source tree on GitHub. This allows generation
# of per-page "Edit on GitHub" links.
github_doc_url = 'https://github.com/awsdocs/aws-ios-developer-guide/tree/master/doc_source'

#
# Version Information
#

# The version info for the project you're documenting, acts as replacement for
# |version| and |release| substitutions in the documentation, and is also used
# in various other places throughout the built documents.

# The short X.Y version.
version = '0.0.3'

# The full version, including alpha/beta/rc tags.
release = '0.0.3'

#
# Forum Information
#

# Optional forum ID. If there's a relevant forum at forums.aws.amazon.com, then
# set the ID here. If not set, then no forum ID link will be generated.
forum_id = '88'

#
# Navlinks
#

# Extra navlinks. You can specify additional links to appear in the top bar here
# as navlink name / url pairs. If extra_navlinks is not set, then no extra
# navlinks will be generated.
#
# extra_navlinks = [
#         ('API Reference', 'http://path/to/api/reference'),
#         ('GitHub', 'http://path/to/github/project'),
#         ]
extra_navlinks = [
        ('API Reference', 'http://docs.aws.amazon.com/AWSiOSSDK/latest/'),
        ('GitHub', 'https://github.com/aws/aws-sdk-ios'),
        ('Samples', 'https://github.com/awslabs/aws-sdk-ios-samples'),
        ('Download SDK',
            'http://sdk-for-ios.amazonwebservices.com/latest/aws-ios-sdk.zip'),
    ]

#
# EXTRA_CONF_CONTENT -- don't change, move or remove this line!
#
# Any settings *below* this act as overrides for the default config content.
# Declare extlinks <http://sphinx-doc.org/latest/ext/extlinks.html> and
# additional configuration details specific to this documentation set here.

if 'extlinks' not in vars():
    extlinks = {}

# The feedback name is different than the service name...
html_theme_options['feedback_name'] = u'Mobile SDK Docs'

#-- Intersphinx mappings ------------------------------------------------------

# Mappings are used if you have more than one doc set that you'd like to refer
# to. The syntax is generally::
#
#  intersphinx_mapping = { 'mapname' : ('url', None) }
#
# For more information about intersphinx mappings, see:
#
# * http://sphinx-doc.org/latest/ext/intersphinx.html
#
aws_docs_url = 'http://' + aws_domains['documentation']
intersphinx_mapping = {
        'sdkforandroid': (aws_docs_url + '/mobile/sdkforandroid/developerguide', None),
#        'sdkforios': (aws_docs_url + '/mobile/sdkforios/developerguide', None),
        'sdkforunity': (aws_docs_url + '/mobile/sdkforunity/developerguide', None),
        'sdkforxamarin': (aws_docs_url + '/mobile/sdkforxamarin/developerguide', None),
        }

extlinks.update({
    # links to API pages or other non-standard guide links.
    'pol-dg': (aws_docs_url + '/lex/latest/developerguide/%s.html', ''),
    'lex-dg': (aws_docs_url + '/polly/latest/dg/%s.html', '')
})

# ** added by extra conf file: default_extlinks.py **
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

# External link (intersphinx + extlink) definitions

# this is used throughout.
aws_docs_url = 'https://docs.aws.amazon.com/'

# intersphinx locations - with these, you can specify :ref: links directly into
# various guides. For example:
#
#  :ref:`tke-ug:allow-lam-to-assume-an-iam-role`
#
# You just specify the guide name as the first parameter in the <link>, and then
# the reference name as the second parameter. The title of the referenced
# section will be used as the title of the link.
#
# For more information, see: http://www.sphinx-doc.org/en/stable/ext/intersphinx.html

if 'sphinx.ext.intersphinx' not in extensions:
    extensions.append('sphinx.ext.intersphinx')

if 'intersphinx_mapping' not in locals():
    intersphinx_mapping = {}

intersphinx_mapping.update({
    'androiddg': (aws_docs_url + 'mobile/sdkforandroid/developerguide', None),
    'cppdg': (aws_docs_url + 'sdk-for-cpp/v1/developer-guide', None),
    'godg': (aws_docs_url + 'sdk-for-go/v1/developer-guide', None),
    'iosdg': (aws_docs_url + 'mobile/sdkforios/developerguide', None),
    'javadg': (aws_docs_url + 'sdk-for-java/v1/developer-guide', None),
    'netdg2': (aws_docs_url + 'sdk-for-net/v2/developer-guide', None),
    'netdg3': (aws_docs_url + 'sdk-for-net/v3/developer-guide', None),
    'pstug': (aws_docs_url + 'powershell/latest/userguide', None),
    'rubydg': (aws_docs_url + 'sdk-for-ruby/v2/developer-guide', None),
    'tkeug': (aws_docs_url + 'toolkit-for-eclipse/v1/user-guide', None),
    'tkvug': (aws_docs_url + 'toolkit-for-visual-studio/latest/user-guide', None),
    'unitydg': (aws_docs_url + 'mobile/sdkforunity/developerguide', None),
    'xamarindg': (aws_docs_url + 'mobile/sdkforxamarin/developerguide', None),
    })

# default extlinks.
#
# You can use them in your document source by specifying a link to an API entry like this::
#
#     The :swf-api:`DescribeWorkflowExecution` action returns the taskPriority
#     of the workflow.
#
# A link will be created to the SWF API reference, pointing to the action described in the role's
# text.
#
# You can also specify link text that's different from the link address by enclosing the address in
# angle-brackets, such as:
#
#    :rande:`SWF <swf>`
#
# This is useful when the link address is cased differently than the desired output text, or when
# you want the link to appear differently than the standard presentation.
#
# The links in this file are meant to be available to all guides and shared among them. To add
# non-shared or more specific extlinks of your own, add them to the end of your ``conf.py`` file
# like this::
#
#     extlinks['my-link-role'] = ('link_url', 'link_prefix')
#
# For more information, see: http://sphinx-doc.org/ext/extlinks.html

if 'sphinx.ext.extlinks' not in extensions:
    extensions.append('sphinx.ext.extlinks')

if 'extlinks' not in locals():
    extlinks = {}

# a function to add guide extlinks
def get_guide_extlinks():
    """add extlinks for all of the entries in ../_includes/guide_links.txt"""
    import re
    guide_extlinks = {}
    guide_links_file = open('_includes/guide_links.txt')
    guide_links_contents = guide_links_file.read()
    guide_links_file.close()
    m = '.. _(.*):\s+(.*)/'
    matches = re.findall(m, guide_links_contents)
    for i in matches:
        guide_extlinks[str.lower(i[0])] = (i[1] + '/%s.html', '')
    return guide_extlinks

extlinks.update(get_guide_extlinks())

# the only things that should be here are extlinks that don't fit the standard
# pattern of 'guide_url/%s.html'
extlinks.update({
    # links to API pages or other non-standard guide links.
    'cog-api': (aws_docs_url + 'cognitoidentity/latest/APIReference/API_%s.html', ''),
    'ec2-api': (aws_docs_url + 'AWSEC2/latest/APIReference/API_%s.html', ''),
    'emr-api': (aws_docs_url + 'ElasticMapReduce/latest/API/API_%s.html', ''),
    'github': ('https://github.com/%s', ''),
    'gloss': (aws_docs_url + 'general/latest/gr/glos-chap.html#%s', ''),
    'iam-api': (aws_docs_url + 'IAM/latest/APIReference/API_%s.html', ''),
    'lam-api': (aws_docs_url + 'lambda/latest/dg/API_%s.html', ''),
    'r53-api': (aws_docs_url + 'Route53/latest/APIReference/API_%s.html', ''),
    's3-bucket-api': (aws_docs_url + 'AmazonS3/latest/API/RESTBucket%s.html', ''),
    's3-object-api': (aws_docs_url + 'AmazonS3/latest/API/RESTObject%s.html', ''),
    's3-service-api': (aws_docs_url + 'AmazonS3/latest/API/RESTService%s.html', ''),
    'sdk-doc-examples' : ('https://github.com/awsdocs/aws-doc-sdk-examples/tree/master/%s', ''),
    'sdk-net-api': (aws_docs_url + 'sdkfornet/v3/apidocs/items/%s.html', ''),
    'sns-api': (aws_docs_url + 'sns/latest/api/API_%s.html', ''),
    'sqs-api': (aws_docs_url + 'AWSSimpleQueueService/latest/APIReference/API_%s.html', ''),
    'sts-api': (aws_docs_url + 'STS/latest/APIReference/API_%s.html', ''),
    'swf-api': (aws_docs_url + 'amazonswf/latest/apireference/API_%s.html', ''),

    # AWS Blogs. Specify the URL past the initial address.
    # Ex. :blog:`developer/category/java`
    'blog': ('https://aws.amazon.com/blogs/%s', ''),

    # AWS Management Console links - Specify the service TLA.
    # Ex. :console:`IAM console <iam>`
    'console': ('https://console.aws.amazon.com/%s/home', ''),

    # Ex. :forum:`Mobile Developer forum <88>`
    'forum': ('https://forums.aws.amazon.com/forum.jspa?forumID=%s', ''),

    # Ex. :forum:`Amazon S3 pricing <s3>`
    'pricing': ('https://aws.amazon.com/%s/pricing/', ''),

    # AWS Regions and Endpoints - Specify the service TLA.
    # Ex. :rande:`Regions and Endpoints: SWF <swf>`
    'rande': (aws_docs_url + 'general/latest/gr/rande.html#%s_region', ''),

    })

# ** end of content from default_extlinks.py **
# ** added by extra conf file: default_includes.py **
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Although you can include files like this:
#
#  .. include _includes/common_includes.txt
#
# Adding this to the rst_prolog/rst_epilog would break includes for topics that exist in
# subdirectories of the 'source' directory.
#
# Instead, we simply gather the information that exists in the default include locations and make
# *that* the rst_epilog.

import os, codecs

# start with a newline, in case the file doesn't end with one...
rst_epilog = '\n'

common_includes = [
    '_includes/common_includes.txt',
    '_includes/guide_links.txt',
    '_includes/service_links.txt',
    '_includes/region_includes.txt',
    '_includes.txt'
    ]

for i in common_includes:
    if os.path.exists(i):
        f = codecs.open(i, 'r', 'utf-8')
        rst_epilog += f.read()
        f.close()

if 'exclude_patterns' not in vars():
    exclude_patterns = []

exclude_patterns += ['README.*', '**/README.*']

# ** end of content from default_includes.py **
# ** added by extra conf file: default_setup.py **
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

# default setup. This is where you can add custom config values and so on.

if 'sphinx.ext.intersphinx' not in extensions:
    extensions.append('sphinx.ext.ifconfig')

def setup(app):
    app.add_config_value('audience', 'public', 'env')

# ** end of content from default_setup.py **
