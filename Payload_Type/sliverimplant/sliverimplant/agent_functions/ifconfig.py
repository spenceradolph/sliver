# TODO: learn how to python, this is probably not right
from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class IfconfigArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass


class Ifconfig(CommandBase):
    cmd = "ifconfig"
    needs_admin = False
    help_cmd = "ifconfig"
    description = "View network interface configurations"
    version = 1
    author = "Spencer Adolph"
    argument_class = IfconfigArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        client = await SliverAPI.create_sliver_client(taskData)

        # await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
        #     TaskID=taskData.Task.ID,
        #     Response="waiting on beacon probably".encode("UTF8"),
        # ))
        
        # TODO: figure out custom command that accomplishes this
        interact = await client.interact_beacon(taskData.Payload.UUID)
        ifconfig_task = await interact.ifconfig()
        ifconfig = await ifconfig_task

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"{str(ifconfig)}".encode("UTF8"),
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
