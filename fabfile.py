from fabric.api import run, env, task, cd, sudo
from fabric.operations import get

"""
pip install fabric
how to run:
fab deploy -H root@www.jedutils.com
"""

@task
def deploy():
    prob_home = '/var/www/html/websites/toolsprj'
    with cd(prob_home):
        sudo('git pull')
        run('workon tools && ./manage.py collectstatic --noinput')
        run('workon tools && ./manage.py migrate')
        run('workon tools && gunicorn -w 2 -b 127.0.0.1:8080 -n toolsprj toolsprj.wsgi:application &')
# gunicorn -w 2 -b 127.0.0.1:8080 -n toolsprj toolsprj.wsgi:application &
