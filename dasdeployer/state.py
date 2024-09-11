from transitions import Machine, State
from transitions.extensions import GraphMachine
# from ui import UiElements

class DasDeployer:
    states = [
        State('none'),
        State('startup'),
        State('select project'),
        State('main'),
        State('deploy in progress'),
        State('deploy finished'),
        State('turn keys'),
        State('push to deploy'),
        State('toggle keys'),
        State('diagnostic'),
    ]

    transitions = [
        {'trigger': 'init', 'source': 'none', 'dest': 'startup'},
        {'trigger': 'multiple_projects', 'source': 'startup', 'dest': 'select project'},
        {'trigger': 'one_project', 'source': 'startup', 'dest': 'main'},
        {'trigger': 'project_selected', 'source': 'select project', 'dest': 'main'},
        {'trigger': 'deploy_with_keys', 'source': 'main', 'dest': 'turn keys'},
        {'trigger': 'ready_to_deploy', 'source': 'turn keys', 'dest': 'push to deploy'},
        {'trigger': 'ready_to_deploy', 'source': 'main', 'dest': 'push to deploy'},
        {'trigger': 'toggle_down', 'source': 'push to deploy', 'dest': 'main'},
        {'trigger': 'toggle_down', 'source': 'turn keys', 'dest': 'main'},
        {'trigger': 'enter_diagnostic', 'source': 'main', 'dest': 'diagnostic'},
        {'trigger': 'exit_diagnostic', 'source': 'diagnostic', 'dest': 'main'},
        {'trigger': 'enter_toggle_keys', 'source': 'main', 'dest': 'toggle keys'},
        {'trigger': 'exit_toggle_keys', 'source': 'toggle keys', 'dest': 'main'},
        {'trigger': 'deploy', 'source': 'push to deploy', 'dest': 'deploy in progress'},
        {'trigger': 'deploy_finished', 'source': 'deploy in progress', 'dest':'deploy finished'},
        {'trigger': 'toggle_down', 'source': 'deploy in progress', 'dest': 'main'},
        {'trigger': 'toggle_down', 'source': 'deploy finished', 'dest': 'main'},
        # {}
    ]

    def __init__(self):
        # self.ui = ui

        self.machine = Machine(
            model=self,
            states=DasDeployer.states,
            transitions=DasDeployer.transitions,
            initial='none',
        )

        # self.machine.add_transition(
        #     trigger='init', source='none', dest='startup'
        # )
        # self.machine.add_transition(
        #     trigger='multiple_projects', source='startup', dest='select project'
        # )
        # self.machine.add_transition(
        #     trigger='one_project', source='startup', dest='main'
        # )
        # self.machine.add_transition(
        #     trigger='project_selected', source='select project', dest='main'
        # )
        # self.machine.add_transition(
        #     trigger='deploy_with_keys', source='main', dest='turn keys'
        # )
        # self.machine.add_transition(
        #     trigger='keys_turned', source='turn keys', dest='push to deploy'
        # )
        # self.machine.add_transition

# das = DasDeployer()
# graph = GraphMachine(model=das, states=DasDeployer.states, transitions=DasDeployer.transitions, initial='none')
# graph.get_graph().draw('diagram.png', prog='dot')
