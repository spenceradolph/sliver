from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class UploadArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="path",
                description="full path to create file",
                type=ParameterType.String
            ),
            CommandParameter(
                name="uuid",
                description="uuid of existing file to upload",
                type=ParameterType.String
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Upload(CommandBase):
    cmd = "upload"
    needs_admin = False
    help_cmd = "upload"
    description = "Upload a file"
    version = 1
    author = "Spencer Adolph"
    argument_class = UploadArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        response = await SliverAPI.upload(taskData, taskData.args.get_arg('uuid'), taskData.args.get_arg('path'))

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response="upload success!".encode("UTF8"),
        ))

        taskResponse = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
            Completed=True
        )
        return taskResponse

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
