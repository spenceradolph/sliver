from tabulate import tabulate
from mythic_container.MythicCommandBase import PTTaskMessageAllData
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient


async def create_sliver_client(taskData: PTTaskMessageAllData):
    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=taskData.BuildParameters[0].Value
    ))

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    
    await client.connect()

    return client

async def sessions_list(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)
    sessions = await client.sessions()

    # ID         Transport   Remote Address         Hostname   Username   Operating System   Health  
    # ========== =========== ====================== ========== ========== ================== =========
    # 78c06ded   mtls        192.168.17.129:51042   ubuntu     root       linux/amd64        [ALIVE] 

    headers = ["ID", "Transport", "Remote Address", "Hostname", "Username", "Operating System", "Health"]
    data = [(session.ID, session.Transport, session.RemoteAddress, session.Hostname, session.Username, session.OS, "[DEAD]" if session.IsDead else "[ALIVE]") for session in sessions]
    table = tabulate(data, headers=headers)

    return table

async def profiles_list(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)
    profiles = await client.implant_profiles()

    # TODO: better formatting

    return profiles

async def beacons_list(taskData: PTTaskMessageAllData):
    client = await create_sliver_client(taskData)
    beacons = await client.beacons()

    # TODO: better formatting

    return beacons




