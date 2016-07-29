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
#

from collections import defaultdict

# Internal config and consts
name = "delvelabs/tachyon"
version = '2.2.2'
expected_path_responses = [200, 206, 401, 403]
expected_file_responses = [200, 206]
timeout_codes = [0, 500, 502, 503, 504]
redirect_codes = [301, 302, 303, 307]
file_sample_len = 2048

# Templates, used by plugins
path_template = {'url': '', 'timeout_count': 0, 'description': ''}

# Extensions used by crafted 404 sampling
crafted_404_extensions = ['', '.php', '.jsp', '.asp', '.html', '.rb', '.js', '.py']

# Values used to generate file list (maybe this sould be configurable)
file_suffixes = ['', '-bak', '-old', '.7z', '.bak', '.cfg', '.cnf', '.conf', '.conf.bak', '.conf.old', '.conf.orig', 
                '.config', '.csv', '.dmp', '.dump', '.inc', '.inc.old', '.inc.orig', '.ini', '.json', '.log', '.old', 
                '.passwd', '.php.bak', '.php.inc', '.php.old', '.php.orig', '.properties', '.pwd', '.rar', '.sql', 
                '.sql.bak', '.sql.old', '.tar', '.tar.bz2', '.tar.gz', '.tgz', '.txt', '.wsdl', '.xml', '.yml', '.zip', 
                '0', '1', '2', '_log', '~']

# Values used to generate executable file lookup
executables_suffixes = ['.php', '.asp', '.aspx', '.pl', '.cgi', '.cfm', '.rb', '.py']

# prefixes added to each path
path_prefixes = ['.', '-', '~']

# User config
target_host = ''
target_base_path = ''
target_port = 80
base_url = ''
is_ssl = False
json_output = False
scheme = ''
proxy_url = ''
forge_vhost='' 
debug = False
search_files = True
recursive = False
fetch_timeout_secs = 2
max_timeout_secs = 15
max_timeout_count = 500
thread_count = 250
eval_output = False
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36' # maximum compatibility
files_only = False
directories_only = False
recursive_depth_limit=2
test_plugin = None
plugins_only = False
cookies = None
allow_download = False
similarity_ratio = 0.8

# Behavioral tests
behavior_queue_size = 5
max_behavior_tries = 5

plugin_settings = defaultdict(list)
