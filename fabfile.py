import os
import tempfile
from will import VERSION
from fabric.api import *

WHITELIST_DIRS = [".git", ]
WHITELIST_FILES = [".gitignore", ]

CTAG = os.environ.get("CTAG", "")

DOCKER_BUILDS = [
    {
        "ctagname": "mlove/will:%(CTAG)s" % os.environ,
        "dir": "will/will-py2/",
        "production": True
    },
]
DOCKER_PATH = os.path.join(os.getcwd(), "docker")


def _splitpath(path):
    path = os.path.normpath(path)
    return path.split(os.sep)


def docker_build():
    print("Building Docker Images...")
    with lcd(DOCKER_PATH):
        for c in DOCKER_BUILDS:
            local("docker build --build-arg repo=https://github.com/mike-love/will --build-arg branch=release/personal -t %(ctagname)s %(dir)s" % c)


def docker_tag():
    print("Building Docker Releases...")
    with lcd(DOCKER_PATH):

        local("docker tag %(ctagname)s mlove/will:latest" %
                filter(lambda x: x["default"], DOCKER_BUILDS))


def docker_push():
    print("Pushing Docker to Docker Cloud...")
    with lcd(DOCKER_PATH):
        local("docker login -u $DOCKER_USER -p $DOCKER_PASS")
        for c in DOCKER_BUILDS:
            local("docker push %(ctagname)s" %c)
        local("docker push mlove/will:latest")

def docker_deploy():
    docker_build()
    docker_tag()
    docker_push()
