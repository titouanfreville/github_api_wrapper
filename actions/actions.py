import inquirer
from repository.repository import Repository


class Actions():

    def __init__(self, config):
        self.__rep = Repository(config)
        self.__allowed_actions = {
            'clone': lambda : self.__rep.clones(),
            'transfer': lambda : self.__rep.transfer(),
            'exit': lambda : 'exit',
            }

    def __act(self):
        questions = [
            inquirer.List(
                    'action',
                    message='What do you want to do?',
                    choices = self.__allowed_actions.keys(),
                    )
            ]
        act = inquirer.prompt(questions)

        return self.__allowed_actions[act['action']]()

    def loop(self):
        while True:
            res = self.__act()
            print(res)
            if res == 'exit':
                exit(0)

