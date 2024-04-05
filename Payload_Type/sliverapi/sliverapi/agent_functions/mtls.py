# TODO: learn how to python, this is probably not right
from ..SliverRequests import SliverAPI

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *

class MtlsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            # TODO: add arguments here for mtls
            CommandParameter(
                name="port",
                description="Which port to listen on",
                type=ParameterType.Number
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Mtls(CommandBase):
    cmd = "mtls"
    needs_admin = False
    # TODO: what is the intended use of help_cmd
    help_cmd = "mtls"
    description = "Start an mTLS listener"
    version = 1
    author = "Spencer Adolph"
    argument_class = MtlsArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        client = await SliverAPI.create_sliver_client(taskData)
        
        results = await client.start_mtls_listener(
            host = "0.0.0.0",
            port = taskData.args.get_arg('port'),
            persistent = False,
        )

        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=taskData.Task.ID,
            Response=f"results: {results}".encode("UTF8"),
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
