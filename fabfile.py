from fabric.api import local

def test():
    local("python -m unittest tests.tests -b -v")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()
