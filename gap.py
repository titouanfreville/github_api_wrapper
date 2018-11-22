from configparser import ConfigParser
from repository.repository import Repository

def main():
    config = ConfigParser()
    config.read('./config.ini')
    rep = Repository(config)

    rep.__init_github_connection__()
    rep.clones()


if __name__ == "__main__":
    main()
