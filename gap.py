from configparser import ConfigParser
from actions.actions import Actions


def main():
    config = ConfigParser()
    config.read('./config.ini')
    act = Actions(config)
    # rep = Repository(config)

    # rep.__init_github_connection__()
    #rep.clones()
    # rep.transfer()
    act.loop()

if __name__ == "__main__":
    main()
