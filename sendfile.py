import json
import aiohttp

class send_file():
    def __init__(self, host: str, port: int):
        self.url = f"http://{host}:{port}"

    async def send(self, message_data: dict):
        '''
        发送文件
        
        args:
            message_data: dict, 包含文件信息的字典
            
        return:
            None
        '''
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps(message_data)
        async with aiohttp.ClientSession(self.url, headers=headers) as session:
            async with session.post("/upload_group_file", data=payload) as response:
                await response.json()
                print(response)