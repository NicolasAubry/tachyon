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

from core import database, textutils, conf
from difflib import SequenceMatcher


def validate_result(content, is_file=False):
    formatted_content = _get_formatted_content(content)
    return _compare_with_saved_404(formatted_content, is_file)


def _get_formatted_content(content):
    """
    Manage content decoding and conf-specified len trimming
    """

    # Decode to utf-8, stripping unknown caracters
    if not isinstance(content, str):
        content = content.decode('utf-8', 'ignore')

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

    # An empty file could be a proof of a hidden structure
    if is_file and content == "":
        return True


def _verify_excluded_patterns(url, is_file):
    """
    Test if the requested url match an exclusion pattern
    """
    pass


