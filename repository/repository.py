from github import Github
from git import Repo
import getpass
import inquirer

from spinner.spin import Spinner
import sys


class Repository():
    """
    Class to manage github repositories accessible
    """

    def __init__(self, config, con=None):
        self.config = config
        self.spin = Spinner('repository spinner', color='green')
        if con:
            self.set_connection(con)
        else:
            self.__init_github_connection__()
        self.__spin_fetch_repository()
        self.spin.sp.start()
        self.spin.sp.stop()

    def __init_github_connection__(self):
        tok = self.config.get('user', 'token')
        if tok:
            try:
                self.__git = Github(tok)
                return
            except Exception as e:
                print('Token Invalid: ', e)
        user = self.config.get('user', 'name')
        if not user:
            if (sys.version_info > (3, 0)):
                user = input('No enter configured.\nUsername: ')
            else:
                user = raw_input('No enter configured.\nUsername: ')
        password = getpass.getpass('Password for user <%s>: ' % user)
        if password:
            self.__git = Github(user, password)
        else:
            print('Could not login to github')

    def get_connection(self):
        return self.__git

    def set_connection(self, git):
        self.__git = git

    def __fetch_repository(self):
        repos = list(self.__git.get_user().get_repos())
        orgs = self.__git.get_user().get_orgs()
        self.orgs = []
        self.user_id = self.__git.get_user().login
        for o in orgs:
            self.orgs.append(o.login)
            repos += list(o.get_repos())
        self.spin.sp.write('Found repositories')
        dict = { }
        dict_no_owner = { }
        for repo in repos:
            self.spin.sp.write('Adding repository %s to base' % repo.name)
            if not repo.owner in dict:
                dict[ repo.owner ] = { }
            dict[ repo.owner ][ repo.name ] = repo
            dict_no_owner[ repo.name ] = repo
        self._repos_with_owner = dict
        self._repos_without_owner = dict_no_owner

    def __spin_fetch_repository(self):
        fetch = lambda : self.__fetch_repository()
        self.spin.spin_except(fetch, description = 'Fetching repositories')

    def __select_repository(self, owned_by = None, message = 'Select repositories:'):
        if owned_by:
            reps = self._repos_with_owner[ 'owned_by' ]
        else:
            reps = self._repos_without_owner

        questions = [
            inquirer.Checkbox(
                    'select',
                    message = message,
                    choices = reps.keys(),
                    )
            ]

        return inquirer.prompt(questions)

    def __clone_list(self, repo_to_clone, base_path):
        for rep_name in repo_to_clone:
            rep = self._repos_without_owner[ rep_name ]
            url = rep.clone_url
            Repo.clone_from(url, "{0}/{1}".format(base_path, rep_name))

    def clones(self, owner = None):
        repo_to_clone = self.__select_repository(owned_by = owner, message = 'Select repositories to clone: ')

        questions = [
            inquirer.Path(
                    'base_path',
                    message='Base path for clone ?')

            ]

        base_path = inquirer.prompt(questions)
        clone = lambda : self.__clone_list(repo_to_clone['select'], base_path['base_path'])
        self.spin.spin_except(clone, 'Cloning repositories', spinner = 'arc')

    def _transfer(self, repos, new_owner):
        for r in repos:
            rep = self._repos_without_owner[r]
            rep.transfer(new_owner)

    def transfer(self, owner = None):
        repo_to_transfer = self.__select_repository(owned_by=owner, message='Select repositories to clone: ')
        questions = [
            inquirer.List(
                    'transfer_to',
                    message='Who do you wish to transfer to ?',
                    choices=self.orgs + [self.user_id]
                    )
            ]
        new_owner = inquirer.prompt(questions)

        _transfer = lambda : self._transfer(repo_to_transfer['select'], new_owner['transfer_to'])

        self.spin.spin_except(_transfer,'Transferring repositories to %s'%new_owner['transfer_to'])
