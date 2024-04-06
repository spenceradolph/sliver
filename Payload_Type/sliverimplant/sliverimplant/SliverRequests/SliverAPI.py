from mythic_container.MythicCommandBase import PTTaskMessageAllData
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient
import json
import gzip

async def create_sliver_client(taskData: PTTaskMessageAllData):
    # TODO: should this configfile somehow be cached so we aren't always using rpc to pull it?
    # Should this be a class who's attributes then are updated with the config?
    # Requires better python skills...

    extraInfoObj = json.loads(taskData.Callback.ExtraInfo)
    configfile = extraInfoObj['slivercfg_fileid']

    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=configfile
    ))

    # TODO: error handling!

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    await client.connect()
    
    return client

async def ifconfig(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        ifconfig_task = await interact.ifconfig()
        ifconfig_results = await ifconfig_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        ifconfig_results = await interact.ifconfig()

    return ifconfig_results

async def download(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        download_task = await interact.download(remote_path=taskData.args.get_arg('path'))
        download_results = await download_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        download_results = await interact.download(remote_path=taskData.args.get_arg('path'))

    plaintext = gzip.decompress(download_results.Data)

    return plaintext

async def upload(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    filestuff = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=taskData.args.get_arg('uuid')
    ))

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        upload_task = await interact.upload(
            remote_path=taskData.args.get_arg('path'),
            data=filestuff.Content
        )
        upload_results = await upload_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        upload_results = await interact.upload(
            remote_path=taskData.args.get_arg('path'),
            data=filestuff.Content
        )

    return upload_results

async def ls(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        ls_task = await interact.ls()
        ls_results = await ls_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        ls_results = await interact.ls()
        
    return ls_results

async def ps(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        ps_task = await interact.ps()
        ps_results = await ps_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        ps_results = await interact.ps()
        
    return ps_results

async def netstat(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    # TODO: get args from task

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        netstat_task = await interact.netstat(tcp=True, udp=True, ipv4=True, ipv6=True, listening=True)
        netstat_results = await netstat_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        netstat_results = await interact.netstat(tcp=True, udp=True, ipv4=True, ipv6=True, listening=True)
        
    return netstat_results
