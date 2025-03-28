from pkg.core.entities import LauncherTypes
from plugins.JM_PDF_plugin.utils.callapi import NapCatApi
from pkg.plugin.context import EventContext

async def send_file(napcat: NapCatApi, ctx: EventContext, file: str, name: str):
    '''
    发送文件
    
    args:
        napcat: NapCatApi实例
        ctx: EventContext实例
        file: 文件路径
        name: 文件名
    '''
    match ctx.event.query.launcher_type:
        case LauncherTypes.PERSON:
            await napcat.callApi('/upload_private_file', {
                'user_id': str(ctx.event.sender_id),
                'file': file,
                'name': name
            })
        case LauncherTypes.GROUP:
            await napcat.callApi('/upload_group_file', {
                'group_id': str(ctx.event.launcher_id),
                'file': file,
                'name': name
            })
        case _:
            raise ValueError(f"Unsupported launcher type: {ctx.event.query.launcher_type}")
    
    