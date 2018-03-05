# Tachyon - Fast Multi-Threaded Web Discovery Tool
# Copyright (c) 2011 Gabriel Tremblay - initnull hat gmail.com
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
# Place, Suite 330, Boston, MA  02111-1307  USA


from uuid import uuid4
from urllib.parse import urlparse
from hammertime.http import Entry
from hammertime.ruleset import RejectRequest
from hammertime.rules.simhash import Simhash
import hashlib


class FilterQueries:

    def __init__(self, match_treshold=5):
        self.engine = None
        self.samples = {}
        self.match_threshold = match_treshold

    def set_engine(self, engine):
        self.engine = engine

    def set_kb(self, kb):
        kb.query_samples = self.samples

    def load_kb(self, kb):
        self.samples = kb.query_samples

    def set_child_heuristics(self, heuristics):
        self.child_heuristics = heuristics

    async def after_response(self, entry):
        url = urlparse(entry.request.url)
        if len(url.query) > 0:
            sample_simhash = await self._get_sample(url)
            if self._match(entry.response, sample_simhash):
                raise RejectRequest("Junk query response")

    async def _get_sample(self, parsed_url):
        sample_key = parsed_url.netloc + parsed_url.path
        try:
            return self.samples[sample_key]
        except KeyError:
            random_query = "{scheme}://{netloc}{path}?{query}"\
                .format(scheme=parsed_url.scheme, netloc=parsed_url.netloc, path=parsed_url.path, query=str(uuid4()))
            print("getting %s for %s" % (random_query, sample_key))
            sample = await self.engine.perform_high_priority(Entry.create(random_query), self.child_heuristics)
            self.samples[sample_key] = self._hash_response(sample.response)
            return self.samples[sample_key]

    def _match(self, response, sample_simhash):
        if "md5" in sample_simhash:
            if self._is_text(response.raw):
                return False
            else:
                return hashlib.md5(response.raw).digest() == sample_simhash["md5"]
        elif "simhash" in sample_simhash:
            if self._is_text(response.raw):
                return Simhash(response.content).distance(Simhash(sample_simhash["simhash"])) <= self.match_threshold
            else:
                return False

    def _hash_response(self, response):
        try:
            return {"simhash": Simhash(response.content).value}
        except UnicodeDecodeError:
            return {"md5": hashlib.md5(response.raw).digest()}

    def _is_text(self, response_content):
        try:
            response_content.decode("utf8")
            return True
        except UnicodeDecodeError:
            return False
