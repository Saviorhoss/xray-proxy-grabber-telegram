import shutil

from git import Repo
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO = os.getenv('REPO')
IS_DEBUG = bool(int(os.getenv('DEBUG_MODE')))

if os.path.exists("./repo/.git"):
    repo = Repo("./repo/")
else:
    repo = Repo.clone_from(
        "https://mrm:{TOKEN_GITHUB}@github.com/{REPO}".format(TOKEN_GITHUB=GITHUB_TOKEN, REPO=REPO), "./repo")

with repo.config_reader() as git_config:
    try:
        mainGitEmail = git_config.get_value('user', 'email')
        mainGitUser = git_config.get_value('user', 'name')
    except:
        mainGitEmail = "None"
        mainGitUser = "None"


def changeGitUserToBot():
    with repo.config_writer() as gitConfig:
        gitConfig.set_value('user', 'email', 'bot@auto.com')
        gitConfig.set_value('user', 'name', 'Bot-auto')


def resetGitUser():
    global mainGitUser, mainGitEmail
    with repo.config_writer() as gitCnf:
        gitCnf.set_value('user', 'email', mainGitEmail)
        gitCnf.set_value('user', 'name', mainGitUser)


def getLatestRowProxies():
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "checkout", "remotes/origin/master", "proxies_row_url.txt", "proxies_active_row_url.txt"])
        shutil.copyfile("./repo/proxies_row_url.txt", "proxies_row_url.txt")
        shutil.copyfile("./repo/proxies_active_row_url.txt", "proxies_active_row_url.txt")


def getLatestActiveConfigs():
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "checkout", "remotes/origin/master", "proxies_active.txt", "proxies_active_under_1000ms.txt", "proxies_active_under_1500ms.txt", "proxies_active_no_403_under_1000ms.txt", "proxies_for_ir_server_no403_u1s.txt"])
        shutil.copyfile("./repo/proxies_active.txt", "proxies_active.txt")
        shutil.copyfile("./repo/proxies_active_under_1000ms.txt", "proxies_active_under_1000ms.txt")
        shutil.copyfile("./repo/proxies_active_under_1500ms.txt", "proxies_active_under_1500ms.txt")
        shutil.copyfile("./repo/proxies_active_no_403_under_1000ms.txt", "proxies_active_no_403_under_1000ms.txt")
        shutil.copyfile("./repo/proxies_for_ir_server_no403_u1s.txt", "proxies_for_ir_server_no403_u1s.txt")


def getLatestGoodForGame():
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "checkout", "remotes/origin/master", "proxies_for_game_row_url.txt"])
        shutil.copyfile("./repo/proxies_for_game_row_url.txt", "proxies_for_game_row_url.txt")


def commitPushRowProxiesFile(chanelUsername):
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "reset", "--hard", "origin/master"])
        repo.git.execute(["git", "pull"])
        shutil.copyfile("proxies_row_url.txt", "./repo/proxies_row_url.txt")
        shutil.copyfile("proxies_active_row_url.txt", "./repo/proxies_active_row_url.txt")
        repo.index.add(["proxies_row_url.txt", "proxies_active_row_url.txt"])
        changeGitUserToBot()
        repo.index.commit('update proxies from {}'.format(chanelUsername))
        repo.remotes.origin.push()
        resetGitUser()
        print('pushed => update proxies from {}'.format(chanelUsername))


def commitPushRActiveProxiesFile():
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "reset", "--hard", "origin/master"])
        repo.git.execute(["git", "pull"])
        shutil.copyfile("proxies_active.txt", "./repo/proxies_active.txt")
        shutil.copyfile("proxies_active_under_1000ms.txt", "./repo/proxies_active_under_1000ms.txt")
        shutil.copyfile("proxies_active_under_1500ms.txt", "./repo/proxies_active_under_1500ms.txt")
        shutil.copyfile("proxies_active_no_403_under_1000ms.txt", "./repo/proxies_active_no_403_under_1000ms.txt")
        shutil.copyfile("proxies_for_ir_server_no403_u1s.txt", "./repo/proxies_for_ir_server_no403_u1s.txt")
        repo.index.add(["proxies_active.txt", "proxies_active_under_1500ms.txt", "proxies_active_under_1000ms.txt", "proxies_active_no_403_under_1000ms.txt", "proxies_for_ir_server_no403_u1s.txt"])
        changeGitUserToBot()
        repo.index.commit('update active proxies')
        repo.remotes.origin.push()
        resetGitUser()
        print('pushed => update active proxies')


def commitPushForGameProxiesFile():
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "reset", "--hard", "origin/master"])
        repo.git.execute(["git", "pull"])
        shutil.copyfile("proxies_for_game_row_url.txt", "./repo/proxies_for_game_row_url.txt")
        repo.index.add(["proxies_for_game_row_url.txt"])
        changeGitUserToBot()
        repo.index.commit('update good for games proxies')
        repo.remotes.origin.push()
        resetGitUser()
        print('pushed => update good for games proxies')
