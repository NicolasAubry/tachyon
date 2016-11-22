# Tachyon - Fast Multi-Threaded Web Discovery Tool
# Copyright (c) 2016 Delve Labs inc.
#
# GNU General Public Licence (GPL)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place,

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

import uuid

from core import database, textutils, conf
from difflib import SequenceMatcher
from core.fetcher import Fetcher

fetcher = Fetcher()


def validate_result(response_code, content, headers, queue_item, is_file=False):
    is_valid = True
    formatted_content = _get_formatted_content(content, queue_item['url'])
    is_valid = _compare_with_saved_404(formatted_content, is_file)
    #is_valid = _test_extensionless_response_code
    return is_valid


def _get_formatted_content(content, url):
    """
    Manage content decoding and conf-specified len trimming
    """

    # Decode to utf-8, stripping unknown caracters
    if not isinstance(content, str):
        content = content.decode('utf-8', 'ignore')

    # Clean up request url from content
    content = content.strip(quote_plus(url))
    content = content.strip(url)  # for unsafe sites

    if not len(content):
        content = ""  # empty content could mean something
    else:
        content = content[0:conf.file_sample_len]

    # Remove linebreaks
    content = content.strip('\r\n ')
    return content


def _compare_with_saved_404(content, is_file):
    """ Detect if the current content is contained in the 404 test database with a sufficient
    similarity ratio
    """
    for fingerprint in database.crafted_404s:
        textutils.output_debug("Testing [" + content + "]" + " against Fingerprint: [" + fingerprint + "]")
        matcher = SequenceMatcher(isjunk=None, a=fingerprint, b=content, autojunk=False)

        textutils.output_debug("Ratio " + str(matcher.ratio()))

        # This content is almost similar to a generated 404, therefore it's a 404.
        if matcher.ratio() > conf.similarity_ratio:
            textutils.output_debug("False positive detected!")
            return False

    return True


# Test different edge cases
def remove_bogus_source_control():
    #.hg #.git
    pass


def remove_bogus_dot_path():
    id = str(uuid.uuid4())
    url = conf.target_base_path + '/.' + id

    pass


def remove_bogus_dash_path():
    pass


def remove_bogus_tilde_path():
    pass


def remove_bogus_apache_dot_files():
    pass


def remove_bogus_global_dot_files():
    pass


def remove_bogus_forbidden():
    pass
