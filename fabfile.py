from fabric.api import *
from fabric.contrib.files import exists

try:
    from fabtools.vagrant import vagrant
except Exception as e:
    print "fabtools package not installed, please install it using"
    print "sudo pip install fabtools"
    print "#######################################################"
    raise

from contextlib import contextmanager as _contextmanager

env.roledefs = {
    'staging': ['ubuntu@staging.blogto.com'],
    'prod': ['ubuntu@app1.internal.blogto.com',
                'ubuntu@app2.internal.blogto.com',
                'ubuntu@redis1.internal.blogto.com',
                'ubuntu@redis2.internal.blogto.com',
                'ubuntu@elasticsearch.internal.blogto.com'
                ],
    'prodapp': ['ubuntu@app1.internal.blogto.com',
                'ubuntu@app2.internal.blogto.com']
}

@task
def update_hostname():
    hostname = "blogto"
    sudo("echo %s > /etc/hostname" % hostname )
    sudo("echo 127.0.0.1 %s >> /etc/hosts" % hostname)
    sudo("/etc/init.d/hostname restart")

@task
def install_packages():
    sudo("apt-get update")
    packages = [
        'nginx', 'vim', 'htop', 'screen', 'git', 'supervisor', 'python-virtualenv',
        'python-dev', 'mercurial', "mysql-server", "postgresql", "libxslt1-dev",
        "libmysqlclient-dev", "build-essential",
        "libjpeg-dev", "libfreetype6", "libfreetype6-dev", "zlib1g-dev", "python-imaging",
        "libjpeg8", "libjpeg8-dev", "libfreetype6", "libfreetype6-dev", "zlib1g",
        "memcached", "python-software-properties", "libpq-dev",
        "binutils", "libproj-dev", "gdal-bin", "postgresql-9.1-postgis", "postgis",
        "python-psycopg2", "libgdal1-1.7.0",  "postgresql-server-dev-9.1", "proj", "openjdk-7-jre-headless"
    ]
    sudo("debconf-set-selections <<< 'mysql-server mysql-server/root_password password g'")
    sudo("debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password g'")

    sudo("apt-get install -y %s" % ' '.join(packages))

    # this is needed for PIL - the imaging library
    try:
        sudo("ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/")
        sudo("ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/")
        sudo("ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/")
    except:
        # if there is already a symlink please dont care
        pass


    # installing postgis
    sudo("locale-gen en_CA.UTF-8")
    sudo("update-locale LANG=en_CA.UTF-8")
    sudo("echo 'local all all trust' | sudo tee -a /etc/postgresql/9.1/main/pg_hba.conf")
    sudo("/etc/init.d/postgresql reload")

    if not exists("/usr/share/proj/null"):
        if not exists("/tmp/nad"):
            sudo("mkdir /tmp/nad")

        with cd("/tmp/nad"):
            sudo("wget http://download.osgeo.org/proj/proj-datumgrid-1.5.tar.gz")
            sudo("tar zxvf proj-datumgrid-1.5.tar.gz")
            sudo("nad2bin null < null.lla")
            sudo("cp null /usr/share/proj")

    # POSTGIS_SQL_PATH=/usr/share/postgresql/9.1/contrib/postgis-1.5/
    # createdb -E UTF8 template_postgis # Create the template spatial database.
    # createlang -d template_postgis plpgsql # Adding PLPGSQL language support.
    # psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"
    # psql -d template_postgis -f $POSTGIS_SQL_PATH/postgis.sql # Loading the PostGIS SQL routines
    # psql -d template_postgis -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql
    # psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;" # Enabling users to alter spatial tables.
    # psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

    with settings(warn_only=True):
        sudo("su postgres -c 'createdb -E UTF8 -T template0 --locale=en_US.utf8 template_postgis'")
        sudo("su postgres -c 'createlang -d template_postgis plpgsql'")
        sudo("""su postgres -c "echo UPDATE pg_database SET datistemplate=\\'true\\' WHERE datname=\\'template_postgis\\'\\; | psql -d postgres " """)
        sudo("su postgres -c 'psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql' ")
        sudo("su postgres -c 'psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql' ")
        sudo("""su postgres -c 'psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"' """)
        sudo("""su postgres -c 'psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"' """)
        sudo("""su postgres -c "echo CREATE ROLE blogtodbu UNENCRYPTED PASSWORD \\'r5lKBj2Mdp\\' NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN\\; | psql -d postgres" """)
        sudo("su postgres -c 'createdb -T template_postgis -O blogtodbu blogto' ")

@task
def prepare_postgres():
    with settings(warn_only=True):
        sudo("su postgres -c 'createdb -E UTF8 -T template0 --locale=en_US.utf8 template_postgis'")
        sudo("su postgres -c 'createlang -d template_postgis plpgsql'")
        sudo("""su postgres -c "echo UPDATE pg_database SET datistemplate=\\'true\\' WHERE datname=\\'template_postgis\\'\\; | psql -d postgres " """)
        sudo("su postgres -c 'psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql' ")
        sudo("su postgres -c 'psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql' ")
        sudo("""su postgres -c 'psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"' """)
        sudo("""su postgres -c 'psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"' """)
        sudo("""su postgres -c "echo CREATE ROLE blogtodbu UNENCRYPTED PASSWORD \\'r5lKBj2Mdp\\' NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN\\; | psql -d postgres" """)
        sudo("su postgres -c 'createdb -T template_postgis -O blogtodbu blogto' ")


@task
def install_elasticsearch():
    try:
        run("dpkg -l | grep openjdk-7")
    except:
        sudo('apt-get install -y openjdk-7-jre-headless')

    try:
        run("dpkg -l | grep elasticsearch")
    except:
        sudo("echo 'deb http://packages.elasticsearch.org/elasticsearch/0.90/debian stable main'  > /etc/apt/sources.list.d/elasticsearch.list")
        sudo("wget -O - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | apt-key add -")
        sudo("apt-get update")
        sudo("apt-get install elasticsearch")

@task
def install_mongodb():
    try:
        run("dpkg -l | grep mongodb")
    except:
        sudo("apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10")
        sudo("echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list")
        sudo("apt-get update")
        sudo("apt-get install mongodb-10gen")

@task
def install_redis():
    try:
        run("dpkg -l | grep redis-server")
    except:
        sudo("sudo add-apt-repository -y ppa:rwky/redis")
        sudo("apt-get update")
        sudo("apt-get install -y redis-server")

def we_are_in_vagrant():
    if not exists('/vagrant'):
        try:
            run('cat /etc/passwd | grep vagrant')
        except:
            return False
    return True

@task
def create_virtualenv_ssh(branch="staging"):
    if not exists('/blogto'):
        sudo('mkdir /blogto')
        sudo('chown -R ubuntu.ubuntu /blogto')

    with cd('/blogto'):
        try:
            run('git clone git@codebasehq.com:hippofoundry/blogto/api-platform.git .')
        except:
            print "couldnt clone git repo, are you sure public key is added ?"
            print "----------------------------------------------------------"
            print get('~/.ssh/id_rsa.pub')
            return
    with cd('/blogto'):
        run('git fetch')
        run('git checkout -b staging origin/staging')
        run('git pull origin articles')

    _create_virtualenv()

def _create_virtualenv():
    if not exists('/blogto/env'):
        run('virtualenv /blogto/env')

    with cd("/blogto"):
        try:
            run("./env/bin/easy_install -U distribute")
        except:
            run("./env/bin/pip install -U distribute")
        run('./env/bin/pip install -r /blogto/requirements.txt')
        run('./env/bin/pip uninstall django-tastypie django-simple-captcha -y')
        run('./env/bin/pip install exifread PIL django-tastypie django-simple-captcha')

@task
def create_virtualenv():
    # are we in vagrant
    if not we_are_in_vagrant():
        raise Exception('we arent in vagrant - run create_virtualenv_ssh')
    _create_virtualenv()

@task
def restore_postgresql():
    if not exists("/blogto/data"):
        run('mkdir /blogto/data')

    with cd('/blogto/data'):
        if not exists('/blogto/data/postgresql.dump'):
            run('wget -c https://s3.amazonaws.com/blogTO-BACKUPS/blogto-dev-dumps/postgresql.dump.gz')

        if not exists("/blogto/data/postgresql.dump"):
            run('gunzip postgresql.dump.gz')

    with cd("/blogto/data"):
        sudo('su postgres -c "cat /blogto/data/postgresql.dump | psql "')

@task
def restore_mysql():
    if not exists("/blogto/data"):
        run('mkdir /blogto/data')

    with cd('/blogto/data'):
        if not exists('/blogto/data/blogto_site-mysql.dump'):
            run('wget -c https://s3.amazonaws.com/blogTO-BACKUPS/blogto-dev-dumps/blogto_site-mysql.dump.gz')
            run('gunzip blogto_site-mysql.dump.gz')

    with cd("/blogto/data"):
        try:
            run('echo show databases | mysql -u root -pg | grep blogto_site')
        except:
            sudo("mysqladmin create -u root -pg blogto_site")
            sudo('mysql blogto_site -u root -pg < blogto_site-mysql.dump')

@task
def prepare_project():
    with cd("/blogto"):
        with cd("blogto"):
            if not exists("settings_local.py"):
                run("ln -s settings_local.py.ex settings_local.py")
    sudo("rm /etc/nginx/sites-enabled/default")
    sudo("ln -s /blogto/conf/nginx-vagrant.conf /etc/nginx/sites-enabled/default")
    sudo("/etc/init.d/nginx restart")
    run("mkdir -p /blogto/blogto/ratings/logs/")

    try:
        run("cat ~/.inputrc | grep completion-ignore-case")
    except:
        run("echo set completion-ignore-case On >> ~/.inputrc")
        run("echo \C-p: history-search-backward >> ~/.inputrc")
        run("echo \C-n: history-search-forward >> ~/.inputrc")

@task
def deploy_staging():
    if not exists('/etc/nginx/proxy.conf'):
        sudo('ln -s /blogto/conf/nginx-proxy.conf /etc/nginx/proxy.conf')

    if not exists('/etc/nginx/sites-enabled/nginx_staging.conf'):
        sudo('ln -s /blogto/conf/nginx_staging.conf /etc/nginx/sites-enabled/nginx_staging.conf')

    try:
        run('dpkg -l | grep supervisor')
    except:
        sudo('apt-get install supervisor')

    if not exists('/etc/supervisor/conf.d/celeryd_staging.conf'):
        sudo('ln -s /blogto/conf/celeryd_staging.conf /etc/supervisor/conf.d/celeryd_staging.conf')

    if not exists('/etc/supervisor/conf.d/supervisor-uwsgi.conf'):
        sudo('ln -s /blogto/conf/supervisor-uwsgi.conf /etc/supervisor/conf.d/supervisor-uwsgi.conf')

    if not exists('/blogto/logs'):
        run('mkdir /blogto/logs')

    if not exists('/blogto/pids'):
        run('mkdir /blogto/pids')

    with cd('/blogto'):
        run('git reset --hard')
        run('git pull origin staging')

