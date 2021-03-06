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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
############

from . import env
from . import logger
from .cli import cfy
from .commands import dev
from .commands import ssh
from .commands import use
from .commands import init
from .commands import logs
from .commands import nodes
from .commands import agents
from .commands import events
from .commands import groups
from .commands import status
from .commands import install
from .commands import plugins
from .commands import recover
from .commands import upgrade
from .commands import teardown
from .commands import profiles
from .commands import rollback
from .commands import bootstrap
from .commands import snapshots
from .commands import uninstall
from .commands import workflows
from .commands import blueprints
from .commands import executions
from .commands import deployments
from .commands import node_instances
from .commands import maintenance_mode


@cfy.group(name='cfy')
@cfy.options.verbose(expose_value=True)
@cfy.options.version
def _cfy(verbose):
    """Cloudify's Command Line Interface

    Note that some commands are only available if you're using a manager.
    You can use a manager by running the `cfy use` command and providing
    it with the IP of your manager (and ssh credentials if applicable).

    To activate bash-completion. Run: `eval "$(_CFY_COMPLETE=source cfy)"`

    Cloudify's working directory resides in ~/.cloudify. To change it, set
    the variable `CFY_WORKDIR` to something else (e.g. /tmp/).
    """
    cfy.set_cli_except_hook(verbose)


def _register_commands():
    """Register the CLI's commands.

    Here is where we decide which commands register with the cli
    and which don't. We should decide that according to whether
    a manager is currently `use`d or not.
    """
    # Manager agnostic commands
    _cfy.add_command(use.use)
    _cfy.add_command(init.init)
    _cfy.add_command(status.status)
    _cfy.add_command(recover.recover)  # Recovers a manager. Doesn't require it
    _cfy.add_command(profiles.profiles)
    _cfy.add_command(bootstrap.bootstrap)

    # Manager only commands
    _cfy.add_command(dev.dev)
    _cfy.add_command(ssh.ssh)
    _cfy.add_command(logs.logs)
    _cfy.add_command(agents.agents)
    _cfy.add_command(events.events)
    _cfy.add_command(plugins.plugins)
    _cfy.add_command(upgrade.upgrade)
    _cfy.add_command(teardown.teardown)
    _cfy.add_command(rollback.rollback)
    _cfy.add_command(snapshots.snapshots)
    _cfy.add_command(maintenance_mode.maintenance_mode)

    _cfy.add_command(nodes.nodes)
    _cfy.add_command(groups.groups)

    _cfy.add_command(workflows.workflows)
    _cfy.add_command(blueprints.blueprints)
    _cfy.add_command(executions.executions)
    _cfy.add_command(deployments.deployments)

    deployments.deployments.add_command(deployments.manager_create)
    deployments.deployments.add_command(deployments.manager_delete)
    deployments.deployments.add_command(deployments.manager_update)
    deployments.deployments.add_command(deployments.manager_list)

    executions.executions.add_command(executions.manager_cancel)
    executions.executions.add_command(executions.manager_list)
    executions.executions.add_command(executions.manager_get)

    # Commands which should be both in manager and local context
    # But change depending on the context.
    if env.is_manager_active():
        _cfy.add_command(install.manager)
        _cfy.add_command(uninstall.manager)
        _cfy.add_command(node_instances.manager)

        deployments.deployments.add_command(deployments.manager_inputs)
        deployments.deployments.add_command(deployments.manager_outputs)

        executions.executions.add_command(executions.manager_start)
    else:
        _cfy.add_command(install.local)
        _cfy.add_command(uninstall.local)
        _cfy.add_command(node_instances.local)

        deployments.deployments.add_command(deployments.local_inputs)
        deployments.deployments.add_command(deployments.local_outputs)

        executions.executions.add_command(executions.local_start)

_register_commands()
logger.configure_loggers()

if __name__ == '__main__':
    _cfy()
