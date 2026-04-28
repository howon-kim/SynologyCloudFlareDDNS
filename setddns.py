import configparser
import os, stat, ssl, certifi
from urllib.request import urlopen

url = 'https://raw.githubusercontent.com/howon-kim/SynologyCloudFlareDDNS/refs/heads/master/cloudflare.php'
target_file = '/usr/syno/bin/ddns/cloudflare.php'

# 1. DDNS 프로바이더 설정 로드
config = configparser.ConfigParser()
config.read('/etc.defaults/ddns_provider.conf')

# 2. Cloudflare 섹션 10개 생성 (Cloudflare, Cloudflare1 ~ Cloudflare9)
# 리스트 컴프리헨션을 사용하여 섹션 이름 목록 생성
sections = ['Cloudflare'] + [f'Cloudflare{i}' for i in range(1, 10)]

for section in sections:
    if section not in config:
        config[section] = {}
    config[section]['modulepath'] = target_file
    config[section]['queryurl'] = 'https://www.cloudflare.com/'

# 3. 설정 파일 저장
with open('/etc.defaults/ddns_provider.conf', 'w') as configfile:
    config.write(configfile)

# 4. 안전한 SSL 다운로드 (cloudflare.php 스크립트)
with urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as response:
    with open(target_file, 'wb') as out_file:
        out_file.write(response.read())

# 5. 실행 권한 설정 (755 권한)
os.chmod(target_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                      stat.S_IRGRP | stat.S_IXGRP |
                      stat.S_IROTH | stat.S_IXOTH)

print(f"Successfully configured {len(sections)} Cloudflare sections.")
