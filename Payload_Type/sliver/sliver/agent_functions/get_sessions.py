from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

from sliver import SliverClientConfig, SliverClient, client_pb2


class GetSessionsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
        ]

    async def parse_arguments(self):
        pass


class GetSessions(CommandBase):
    cmd = "get_sessions"
    needs_admin = False
    help_cmd = "get_sessions"
    description = "Get the list of sessions that Sliver is aware of."
    version = 1
    author = "Spencer Adolph"
    argument_class = GetSessionsArguments
    attackmapping = []

    async def create_go_tasking(self,
                                taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        response = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=False,
            Completed=True
        )

        # TODO: interact with sliver here, append to response? (check bloodhound get_domains)
        # taskData holds the build params, which has the config file text to load

        configtext = None
        for buildParam in taskData.BuildParameters:
            if buildParam.Name == "CONFIGTEXT":
                configtext = buildParam.Value
        # configfile: BuildParameterType.File = None
        # for buildParam in taskData.BuildParameters:
        #     if buildParam.Name == "CONFIGFILE":
        #         configfile = buildParam.Value

        # MythicRPCFileGetContentMessage()
        # filecontent = await SendMythicRPCFileGetContent(MythicRPCFileGetContentMessage(
        #     AgentFileId=configfile
        # ))

        # response.Stdout = configfile

        config = SliverClientConfig.parse_config(configtext)
        client = SliverClient(config)
        await client.connect()

        sessions = await client.sessions()

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"Sessions: {str(sessions)}".encode("UTF8"),
        ))

        response.Success = True

        return response

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
