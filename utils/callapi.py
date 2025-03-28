import json
import aiohttp
from pkg.core.entities import LauncherTypes

class NapCatApi():
    def __init__(self, host: str, port: int):
        self.url = f"http://{host}:{port}"

    async def callApi(self, api_url: str, payload: dict, ):
        '''
        发送文件
        
        args:
            payload: dict, 负载字典
            api_url: str, 发送者类型
        return:
            None
        '''
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps(payload)
        async with aiohttp.ClientSession(self.url, headers=headers) as session:
            async with session.post(api_url, data=payload) as response:
                data = await response.json()
                return data