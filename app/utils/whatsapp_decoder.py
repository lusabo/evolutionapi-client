from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import hashlib
import hmac
import base64
import requests
import mimetypes
import random
import os

if not os.path.exists('./tmp'):
    os.makedirs('./tmp')
if not os.path.exists('./decoded'):
    os.makedirs('./decoded')

def download_using_enc_link(payload):

    filename = None

    if 'filename' in payload:
        filename = payload['filename'] or None

    mediaKey                    = payload['mediaKey']
    url                         = payload['url']
    messageType                 = payload['messageType']
    whatsappTypeMessageToDecode = payload['whatsappTypeMessageToDecode']
    mimetype                    = payload['mimetype'].split(';')[0]

    if not filename:
        filename = random.getrandbits(128)
        file_extension = mimetypes.guess_extension(mimetype)
        complete_filename = '{}{}'.format(filename, file_extension)

    print('filename: {}\nmediaKey: {}\nurl: {}\nmessageType: {}\nwhatsappTypeMessageToDecode:{} \nmimetype:{}\nextension:{}'.format(filename, mediaKey, url, messageType, whatsappTypeMessageToDecode, mimetype, file_extension))
        
    # Download .enc inside /tmp folder
    r = requests.get(url, allow_redirects=True)
    open('tmp/{}.enc'.format(filename), 'wb').write(r.content)

    def HKDF(key, length, appInfo=b""):
        key = hmac.new(b"\0"*32, key, hashlib.sha256).digest()
        keyStream = b""
        keyBlock = b""
        blockIndex = 1
        while len(keyStream) < length:
            keyBlock = hmac.new(key, msg=keyBlock+appInfo+(chr(blockIndex).encode("utf-8")), digestmod=hashlib.sha256).digest()
            blockIndex += 1
            keyStream += keyBlock
        return keyStream[:length]

    def AESUnpad(s):
        return s[:-ord(s[len(s)-1:])];

    def AESDecrypt(key, ciphertext, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv);
        plaintext = cipher.decrypt(ciphertext);
        return AESUnpad(plaintext);

    mediaKeyExpanded=HKDF(base64.b64decode(mediaKey),112, bytes(whatsappTypeMessageToDecode, encoding='utf-8'))

    mediaData=open('tmp/{}.enc'.format(filename), "rb").read()

    file= mediaData[:-10] 

    file_data_decoded = AESDecrypt(mediaKeyExpanded[16:48],file, mediaKeyExpanded[:16])

    decoded_path = f'decoded/{complete_filename}'
    with open(decoded_path, 'wb') as f:
        f.write(file_data_decoded)

    print("Decrypted [{}] [{}]".format(messageType, complete_filename))

    return decoded_path