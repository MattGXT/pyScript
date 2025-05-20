import uuid
import requests
import browser_cookie3
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT

jar = browser_cookie3.chrome(domain_name='.paic.com.cn')
token = None
for cookie in jar:
    if cookie.name == 'CAS_SSO_COOKIE':
        token = cookie.value
        break

def fuck():
    res = requests.post('https://code.paic.com.cn/code_pilot/api/request', cookies={
        'CAS_SSO_COOKIE': token,
    })
    if res.ok:
        value = str(res.json()['data']).encode()
        ws_auth = res.cookies.get('ws_auth')
        JSESSIONID = res.cookies.get('JSESSIONID')
    else:
        return

    key = bytes.fromhex('6cef39eb8561d4f46fbaf66bbd8d89b6')
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    emcrpt_value = crypt_sm4.crypt_ecb(value).hex()

    with requests.post('https://code.paic.com.cn/code_pilot/api/stream/codegens', cookies={
        'CAS_SSO_COOKIE': token,
        'JSESSIONID': JSESSIONID
    }, headers={
        'Ws-Auth': ws_auth,
        'Ws-Sign': emcrpt_value,
        'Accept': '*/*'
    }, json={
        'pluginVersion': 'CHROME_2.1.15',
        'prompt': '你好，我想写一段代码',
        'messages': [],
        'knowledgeIds': [],
        'isUseOwnHistory': True,
        'isUseCodeCompletion': False,
        'commandType': 4,
        'requestId': str(uuid.uuid4()),
        'sessionId': str(uuid.uuid4())
    }, stream=True) as res:
        res.raise_for_status()
        if res.status_code == 200:
            print('成功')

print('AimaFucker已启动')
for i in range(20):
    print(f'正在循环第{i}次请求')
    fuck()
print('done!')
    
