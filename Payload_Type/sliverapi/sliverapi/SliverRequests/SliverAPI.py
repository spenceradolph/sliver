from mythic_container.MythicCommandBase import PTTaskMessageAllData
from mythic_container.MythicRPC import SendMythicRPCFileGetContent, MythicRPCFileGetContentMessage
from sliver import SliverClientConfig, SliverClient


async def create_sliver_client(taskData: PTTaskMessageAllData):
    # TODO: should this configfile somehow be cached so we aren't always using rpc to pull it?
    # Should this be a class who's attributes then are updated with the config?
    # Requires better python skills...

    # TODO: cleaner way of grabbing this since its the only parameter?
    configfile = None
    for buildParam in taskData.BuildParameters:
        if buildParam.Name == "CONFIGFILE":
            configfile = buildParam.Value

    filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        AgentFileId=configfile
    ))

    # TODO: error handling!

    config = SliverClientConfig.parse_config(filecontent.Content)
    client = SliverClient(config)
    await client.connect() # Most functionality requires connecting first
    return client

