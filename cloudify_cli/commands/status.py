########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

"""
Handles 'cfy status'
"""

from cloudify_cli.logger import lgr
from cloudify_rest_client.exceptions import CloudifyClientError
from cloudify_cli import utils


def status():
    management_ip = utils.get_management_server_ip()
    lgr.info('Getting management services status... [ip={0}]'
             .format(management_ip))

    client = utils.get_rest_client(management_ip)
    try:
        status_result = client.manager.get_status()
    except CloudifyClientError:
        status_result = None
    if status_result:
        services = []
        for service in status_result['services']:
            state = service['instances'][0]['state'] \
                if 'instances' in service and \
                   len(service['instances']) > 0 else 'unknown'
            services.append({
                'service': service['display_name'].ljust(30),
                'status': state
            })
        pt = utils.table(['service', 'status'], data=services)
        utils.print_table('Services:', pt)
        return True
    else:
        lgr.info('REST service at management server {0} is not responding!'
                 .format(management_ip))
        return False