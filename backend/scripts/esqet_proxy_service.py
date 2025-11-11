import asyncio
import logging
from proxy_agent import ProxyAgent
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("esqet_proxy")

class ESQETProxy:
    def __init__(self, host='127.0.0.1', port=8000):
        self.agent = ProxyAgent(f'socks5h://{host}:{port}')
        self.key = secrets.token_bytes(32)
        self.cipher = Cipher(algorithms.AES(self.key), modes.GCM())

    async def proxy_request(self, url, data=None):
        try:
            encryptor = self.cipher.encryptor()
            encrypted = encryptor.update(json.dumps(data).encode()) + encryptor.finalize()
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.agent.request('POST', url, data=encrypted)
            )
            decryptor = self.cipher.decryptor()
            decrypted = decryptor.update(response.content) + decryptor.finalize()
            logger.info(f"Proxied {url}: {response.status_code}")
            return json.loads(decrypted)
        except Exception as e:
            logger.error(f"Proxy error: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    proxy = ESQETProxy()
    asyncio.run(proxy.proxy_request("http://localhost:5000/nft"))
