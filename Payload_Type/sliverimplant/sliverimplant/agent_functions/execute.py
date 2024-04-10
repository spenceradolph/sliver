from ..SliverRequests import SliverAPI


from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class ExecuteArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="exe",
                description="exe to execute",
                type=ParameterType.String
            ),
            CommandParameter(
                name="args",
                description="args to pass to executable",
                type=ParameterType.Array
            ),
            CommandParameter(
                name="output",
                description="capture output or not",
                type=ParameterType.Boolean
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Execute(CommandBase):
    cmd = "execute"
    needs_admin = False
    help_cmd = "execute"
    description = "Execute a program on the remote system"
    version = 1
    author = "Spencer Adolph"
    argument_class = ExecuteArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        execute_results = await SliverAPI.execute(taskData)

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"{str(execute_results)}".encode("UTF8"),
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
