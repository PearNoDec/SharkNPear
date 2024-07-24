import hashlib
import base64
import hmac
import jwt
import datetime
from Crypto.Cipher import AES, DES, DES3, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import urllib.parse
import json
import traceback

AES_MODES = {
    "CBC": AES.MODE_CBC,
    "ECB": AES.MODE_ECB,
    "CTR": AES.MODE_CTR,
    "OFB": AES.MODE_OFB,
    "CFB": AES.MODE_CFB
}

PADDING_STYLES = {
    "Pkcs7": "pkcs7",
    "NoPadding": "none",
    "ZeroPadding": "zero",
    "Iso97971": "iso7816",
    "AnsiX923": "x923",
    "Iso10126": "iso10126"
}

DES_MODES = {
    "CBC": DES.MODE_CBC,
    "ECB": DES.MODE_ECB,
    "CTR": DES.MODE_CTR,
    "OFB": DES.MODE_OFB,
    "CFB": DES.MODE_CFB
}

DES3_MODES = {
    "CBC": DES3.MODE_CBC,
    "ECB": DES3.MODE_ECB,
    "CTR": DES3.MODE_CTR,
    "OFB": DES3.MODE_OFB,
    "CFB": DES3.MODE_CFB
}

def update_hashes(input_text, is_uppercase):
    try:
        if input_text:
            hashes = {
                "MD5": hashlib.md5(input_text.encode()).hexdigest(),
                "MD5_Middle": hashlib.md5(input_text.encode()).hexdigest()[8:24],
                "Sha1": hashlib.sha1(input_text.encode()).hexdigest(),
                "Sha256": hashlib.sha256(input_text.encode()).hexdigest(),
                "Sha512": hashlib.sha512(input_text.encode()).hexdigest()
            }
        else:
            hashes = {
                "MD5": "",
                "MD5_Middle": "",
                "Sha1": "",
                "Sha256": "",
                "Sha512": ""
            }

        if is_uppercase:
            hashes = {k: v.upper() for k, v in hashes.items()}

        return hashes
    except Exception as e:
        return f"出现错误：{e}"

def url_encode(url_input):
    try:
        return urllib.parse.quote(url_input)
    except Exception as e:
        return f"出现错误：{e}"

def url_decode(input_text):
    try:
        return urllib.parse.unquote(input_text)
    except Exception as e:
        return f"出现错误：{e}"

def base64_encode(input_text):
    try:
        return base64.b64encode(input_text.encode()).decode()
    except Exception as e:
        return f"出现错误：{e}"

def base64_decode(input_text):
    try:
        return base64.b64decode(input_text).decode()
    except Exception as e:
        return f"出现错误：{e}"

def aes_encrypt(mode, padding, key, iv, data, key_size, input_mode, output_mode):
    try:
        padding = PADDING_STYLES[padding]
        key = key[:key_size // 8]
        if input_mode == "Hex":
            data = bytes.fromhex(data)
        elif input_mode == "Base64":
            data = b64decode(data)
        else:
            data = data.encode()

        if mode != "ECB":
            cipher = AES.new(key, AES_MODES[mode], iv=iv)
        else:
            cipher = AES.new(key, AES_MODES[mode])

        if padding != "none":
            data = pad(data, AES.block_size, style=padding)

        encrypted_data = cipher.encrypt(data)

        if output_mode == "Hex":
            return encrypted_data.hex()
        elif output_mode == "Base64":
            return b64encode(encrypted_data).decode()
        else:
            return "数据加密（二进制输出不可显示）"
    except Exception as e:
        return f"出现错误：{e}"

def aes_decrypt(mode, padding, key, iv, data, key_size, input_mode, output_mode):
    try:
        padding = PADDING_STYLES[padding]
        key = key[:key_size // 8]
        if input_mode == "Hex":
            data = bytes.fromhex(data)
        elif input_mode == "Base64":
            data = b64decode(data)
        else:
            data = data.encode()

        if mode != "ECB":
            cipher = AES.new(key, AES_MODES[mode], iv=iv)
        else:
            cipher = AES.new(key, AES_MODES[mode])

        decrypted_data = cipher.decrypt(data)

        if padding != "none":
            decrypted_data = unpad(decrypted_data, AES.block_size, style=padding)

        if output_mode == "Hex":
            return decrypted_data.hex()
        elif output_mode == "Base64":
            return b64encode(decrypted_data).decode()
        else:
            return decrypted_data.decode()
    except Exception as e:
        return f"出现错误：{e}"

def des_encrypt(mode, padding, key, iv, data, input_mode, output_mode):
    try:
        padding = PADDING_STYLES[padding]
        key = key[:8]
        if input_mode == "Hex":
            data = bytes.fromhex(data)
        elif input_mode == "Base64":
            data = b64decode(data)
        else:
            data = data.encode()

        if mode != "ECB":
            cipher = DES.new(key, DES_MODES[mode], iv)
        else:
            cipher = DES.new(key, DES_MODES[mode])
        if padding != "none":
            data = pad(data, DES.block_size, style=padding)

        encrypted_data = cipher.encrypt(data)

        if output_mode == "Hex":
            output = encrypted_data.hex()
        elif output_mode == "Base64":
            output = b64encode(encrypted_data).decode()
        else:
            output = "数据加密（二进制输出不可显示）"

        return output
    except Exception as e:
        return f"出现错误：{e}"

def des_decrypt(mode, padding, key, iv, data, input_mode, output_mode):
    try:
        padding = PADDING_STYLES[padding]
        key = key[:8]
        if input_mode == "Hex":
            data = bytes.fromhex(data)
        elif input_mode == "Base64":
            data = b64decode(data)
        else:
            data = data.encode()

        if mode != "ECB":
            cipher = DES.new(key, DES_MODES[mode], iv)
        else:
            cipher = DES.new(key, DES_MODES[mode])

        decrypted_data = cipher.decrypt(data)
        if padding != "none":
            decrypted_data = unpad(decrypted_data, DES.block_size, style=padding)
        if output_mode == "Hex":
            output = decrypted_data.hex()
        elif output_mode == "Base64":
            output = b64encode(decrypted_data).decode()
        else:
            output = decrypted_data.decode()

        return output
    except Exception as e:
        return f"出现错误：{e}"

def rsa_encrypt(rsa_password, input_mode, data, output_mode):
    try:
        public_key = RSA.import_key(rsa_password)
        cipher = PKCS1_OAEP.new(public_key)

        if input_mode == "Hex":
            data = bytes.fromhex(data)
        elif input_mode == "Base64":
            data = b64decode(data)
        else:
            data = data.encode()

        encrypted_data = cipher.encrypt(data)

        if output_mode == "Hex":
            output = encrypted_data.hex()
        elif output_mode == "Base64":
            output = b64encode(encrypted_data).decode()
        else:
            output = "加密数据（二进制输出不可显示）"

        return output
    except Exception as e:
        return f"出现错误：{e}"

def rsa_decrypt(rsa_password, input_mode, data, output_mode):
    try:
        private_key = RSA.import_key(rsa_password)
        cipher = PKCS1_OAEP.new(private_key)
        if input_mode == "Hex":
            data = bytes.fromhex(data)
        elif input_mode == "Base64":
            data = b64decode(data)
        else:
            data = data.encode()

        decrypted_data = cipher.decrypt(data)

        if output_mode == "Hex":
            output = decrypted_data.hex()
        elif output_mode == "Base64":
            output = b64encode(decrypted_data).decode()
        else:
            output = decrypted_data.decode()

        return output
    except Exception as e:
        return f"出现错误：{e}"

def calculate_hmac(data, key, input_mode):
    try:
        if not data:
            return ["HMAC-MD5值...", "HMAC-SHA1值...", "HMAC-SHA256值...", "HMAC-SHA512值..."]

        if input_mode == "Base64":
            data = b64decode(data)
        elif input_mode == "HEX":
            data = bytes.fromhex(data)
        else:
            data = data.encode()
        hmac_md5 = hmac.new(key, data, hashlib.md5).digest()
        hmac_sha1 = hmac.new(key, data, hashlib.sha1).digest()
        hmac_sha256 = hmac.new(key, data, hashlib.sha256).digest()
        hmac_sha512 = hmac.new(key, data, hashlib.sha512).digest()
        return [hmac_md5.hex(), hmac_sha1.hex(), hmac_sha256.hex(), hmac_sha512.hex()]
    except Exception as e:
        return [str(e), str(e), str(e), str(e)]


def des3_encrypt(mode, padding, key, iv, data, input_mode, output_mode):
    try:
        print(mode, padding, key, iv, data, input_mode, output_mode)
        padding = PADDING_STYLES[padding]
        key = key.ljust(24, b'\0')

        if input_mode == "Hex":
            data = bytes.fromhex(data)
        elif input_mode == "Base64":
            data = b64decode(data)
        else:
            data = data.encode()

        if mode != "ECB":
            cipher = DES3.new(key, DES3_MODES[mode], iv=iv)
        else:
            cipher = DES3.new(key, DES3_MODES[mode])

        if padding != "none":
            data = pad(data, DES3.block_size, style=padding)

        encrypted_data = cipher.encrypt(data)

        if output_mode == "Hex":
            output = encrypted_data.hex()
        elif output_mode == "Base64":
            output = b64encode(encrypted_data).decode()
        else:
            output = "数据加密（二进制输出不可显示）"

        return output
    except Exception as e:
        traceback.print_exc()
        return f"出现错误：{e}"

def des3_decrypt(mode, padding, key, iv, data, input_mode, output_mode):
    try:
        padding = PADDING_STYLES[padding]

        key = key.ljust(24, b'\0')

        if input_mode == "Hex":
            data = bytes.fromhex(data)
        elif input_mode == "Base64":
            data = b64decode(data)
        else:
            data = data.encode()

        if mode != "ECB":
            cipher = DES3.new(key, DES_MODES[mode], iv=iv)
        else:
            cipher = DES3.new(key, DES_MODES[mode])

        decrypted_data = cipher.decrypt(data)

        if padding != "none":
            decrypted_data = unpad(decrypted_data, DES3.block_size, style=padding)

        if output_mode == "Hex":
            output = decrypted_data.hex()
        elif output_mode == "Base64":
            output = b64encode(decrypted_data).decode()
        else:
            output = decrypted_data.decode()

        return output
    except Exception as e:
        return f"出现错误：{e}"

def unicode_encode(text):
    try:
        encoded_text = ''.join(f"\\u{ord(char):04X}" for char in text)
        return encoded_text
    except Exception as e:
        return f"出现错误：{e}"


def unicode_decode(text):
    try:
        decoded_text = text.encode('latin1').decode('unicode-escape')
        return decoded_text
    except Exception as e:
        return f"出现错误：{e}"

def jwt_encode(payload_data, key):
    try:
        payload = json.loads(payload_data)
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        encoded_jwt = jwt.encode(payload, key, algorithm='HS256')
        return encoded_jwt
    except Exception as e:
        return f"出现错误：{e}"

def jwt_decode(encoded_jwt, key):
    try:
        decoded = jwt.decode(encoded_jwt, key, algorithms=['HS256'])
        decoded_str = json.dumps(decoded, indent=4, ensure_ascii=False)
        return decoded_str
    except jwt.ExpiredSignatureError:
        return "JWT已过期"
    except jwt.InvalidTokenError:
        return "无效的JWT"
    except Exception as e:
        return f"出现错误：{e}"

def string_to_hex(text):
    try:
        hex_output = text.encode('utf-8').hex()
        return hex_output
    except Exception as e:
        return f"出现错误：{e}"

def hex_to_string(hex_input):
    try:
        string_output = bytes.fromhex(hex_input).decode('utf-8')
        return string_output
    except Exception as e:
        return f"出现错误：{e}"