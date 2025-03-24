from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from pkg.platform.types import *
from plugins.JM_PDF_plugin.image2pdf import *
from plugins.JM_PDF_plugin.sendfile import *
import re
import os

current_dir = os.path.dirname(__file__)

# 注册插件
@register(name="JMcomicPDF", description="迅速突破卡脖子核心技术", version="1.0", author="Amethyst")
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
                await ctx.reply(f"正在将jm{manga_id}转换为PDF...\n可能需要10s至1min不等，请耐心等待")
                if not mangaCache(manga_id):
                    sendPDF([manga_id])
                message_data = {
                    "group_id": str(ctx.event.launcher_id),
                    "file": os.path.normpath(os.path.join(self.pdf_dir, f"{searchManga(manga_id)}.pdf")),
                    "name": f"{manga_id}.pdf",
                }
                await self.send_file.send(message_data)
            case _:
                pass
        
    # 插件卸载时触发
    def __del__(self):
        pass
