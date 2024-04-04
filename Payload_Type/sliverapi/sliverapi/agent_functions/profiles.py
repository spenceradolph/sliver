# TODO: learn how to python, this is probably not right
from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ProfilesArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Profiles(CommandBase):
    cmd = "profiles"
    needs_admin = False
    help_cmd = "profiles"
    description = "Get the list of external builders that Sliver is aware of."
    version = 1
    author = "Spencer Adolph"
    argument_class = ProfilesArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        client = await SliverAPI.create_sliver_client(taskData)
        
        # TODO: figure out custom command that accomplishes this
        profiles = await client.implant_profiles()

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"Profiles: {str(profiles)}".encode("UTF8"),
        ))

        # TODO: error handling
        response = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )

        return response

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
