import configparser
import urllib.request
import os, stat

url = 'https://raw.githubusercontent.com/howon-kim/SynologyCloudFlareDDNS/refs/heads/master/cloudflare.php'
target_file = '/usr/syno/bin/ddns/cloudflare.php'

config= configparser.ConfigParser()
config.read('/etc.defaults/ddns_provider.conf')

try:
        config['Cloudflare']
        config['Cloudflare1']
except KeyError:
        config['Cloudflare']= {}
        config['Cloudflare1']= {}

config['Cloudflare']['modulepath'] = '/usr/syno/bin/ddns/cloudflare.php'
config['Cloudflare']['queryurl'] = 'https://www.cloudflare.com/'
config['Cloudflare1']['modulepath'] = '/usr/syno/bin/ddns/cloudflare.php'
config['Cloudflare1']['queryurl'] = 'https://www.cloudflare.com/'

with open('/etc.defaults/ddns_provider.conf', 'w') as configfile:
        config.write(configfile)

urllib.request.urlretrieve(url, target_file)
os.chmod(target_file, stat.S_IRUSR |  stat.S_IWUSR |  stat.S_IXUSR |  stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
