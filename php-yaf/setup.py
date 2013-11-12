import subprocess
import sys
import setup_util
from os.path import expanduser

home = expanduser("~")

def start(args, logfile):
  setup_util.replace_text("php-yaf/app/conf/application.ini", "host=localhost", "host="+ args.database_host +"")
  setup_util.replace_text("php-yaf/deploy/nginx.conf", "root .*\/FrameworkBenchmarks", "root " + home + "/FrameworkBenchmarks")

  try:
    subprocess.check_call("sudo chown -R www-data:www-data php-yaf", shell=True)
    subprocess.check_call("sudo php-fpm --fpm-config config/php-fpm.conf -g " + home + "/FrameworkBenchmarks/php-yaf/deploy/php-fpm.pid", shell=True)
    subprocess.check_call("sudo /usr/local/nginx/sbin/nginx -c " + home + "/FrameworkBenchmarks/php-yaf/deploy/nginx.conf", shell=True)
    return 0
  except subprocess.CalledProcessError:
    return 1

def stop(logfile):
  try:
    subprocess.call("sudo /usr/local/nginx/sbin/nginx -s stop", shell=True)
    subprocess.call("sudo kill -QUIT $( cat php-yaf/deploy/php-fpm.pid )", shell=True)
    subprocess.check_call("sudo chown -R $USER:$USER php-yaf", shell=True)
    return 0
  except subprocess.CalledProcessError:
    return 1