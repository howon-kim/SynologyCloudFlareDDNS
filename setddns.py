import configparser
import os, stat, ssl, certifi
from urllib.request import urlopen

url = 'https://raw.githubusercontent.com/howon-kim/SynologyCloudFlareDDNS/refs/heads/master/cloudflare.php'
target_file = '/usr/syno/bin/ddns/cloudflare.php'

# 수정: DDNS 프로바이더 설정
config = configparser.ConfigParser()
config.read('/etc.defaults/ddns_provider.conf')

for section in ['Cloudflare', 'Cloudflare1', 'Cloudflare2', 'Cloudflare3', 'Cloudflare4', 'Cloudflare5']:
    if section not in config:
        config[section] = {}
    config[section]['modulepath'] = target_file
    config[section]['queryurl'] = 'https://www.cloudflare.com/'

with open('/etc.defaults/ddns_provider.conf', 'w') as configfile:
    config.write(configfile)

# 수정: 안전한 SSL 다운로드
with urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as response:
    with open(target_file, 'wb') as out_file:
        out_file.write(response.read())

# 권한 설정
os.chmod(target_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                      stat.S_IRGRP | stat.S_IXGRP |
                      stat.S_IROTH | stat.S_IXOTH)
