from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from pkg.platform.types import *
from plugins.JM_PDF_plugin.image2pdf import *
from plugins.JM_PDF_plugin.sendfile import *
import re
import os
import random
import zipfile
import json


current_dir = os.path.dirname(__file__)

# 注册插件
@register(name="JMcomicZip", description="迅速突破卡脖子核心技术(带加密)", version="1.0", author="Amethyst/TwperBody")
class JMcomicPDFPlugin(BasePlugin):
    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.send_file = send_file(host="127.0.0.1", port=3000)
        self.pdf_dir = os.path.join(current_dir, "downloads")
        self.instructions = {
            "/jm": r"^/jm$",
            "/jm [ID]": r"^/jm (\d+)$"
        }
    
    def matchPattern(self, msg):
        '''
        匹配指令
        
        args:
            msg: 指令内容
        return:
            匹配结果
        '''
        res = None
        for pattern in self.instructions:
            if re.match(self.instructions[pattern], msg):
                res = pattern
        return res
    
    # 异步初始化
    async def initialize(self):
        pass

    # 当收到群消息时触发
    @handler(GroupMessageReceived)
    async def group_message_received(self, ctx: EventContext):
        msg = str(ctx.event.message_chain)
        # 匹配指令
        match self.matchPattern(msg):
            case "/jm":
                await ctx.reply(MessageChain([
                    Plain("jm卡脖子核心技术\n"),
                    Plain("将jm号对应本子转化为pdf，请输入jm号进行转化，如：/jm 123456")
                ]))
            case "/jm [ID]":
                manga_id = re.search(r"^/jm (\d+)$", msg).group(1)
                password = str(random.randint(100000, 999999))
    
                # 记录manga_id和password到history.json文件
                history_file = os.path.join(self.pdf_dir, "history.json")
                if os.path.exists(history_file):
                    with open(history_file, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                else:
                    history = {}
                history[manga_id] = password
                with open(history_file, 'w', encoding='utf-8') as f:
                    json.dump(history, f, ensure_ascii=False, indent=4)

                 # 检查manga_id是否已存在于history.json中
                if manga_id in history:
                    existing_password = history[manga_id]
                    await ctx.reply(f"读取到jm{manga_id}缓存...\n请使用以下密码解压：{existing_password}")
                    zip_file = os.path.normpath(os.path.join(self.pdf_dir, f"{searchManga(manga_id)}.zip"))
                else:
                    await ctx.reply(f"正在下载jm{manga_id}...\n请使用以下密码解压：{password}")
                    await ctx.reply(f"正在将jm{manga_id}转换为PDF...\n可能需要10s至1min不等，请耐心等待")
                    pdf_file = os.path.normpath(os.path.join(self.pdf_dir, f"{searchManga(manga_id)}.pdf"))
                    zip_file = os.path.normpath(os.path.join(self.pdf_dir, f"{searchManga(manga_id)}.zip"))
                    sendPDF([manga_id])
                    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.setpassword(password.encode())
                        zipf.write(pdf_file)
                    if os.path.exists(pdf_file):
                        os.remove(pdf_file)
                message_data = {
                    "group_id": str(ctx.event.launcher_id),
                    "file": zip_file,
                    "name": f"{manga_id}.zip",
                }
                await self.send_file.send(message_data)
            case _:
                pass
        
    # 插件卸载时触发
    def __del__(self):
        pass
