# TODO: learn how to python, this is probably not right
from ..SliverRequests import SliverAPI
import json

from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from mythic_container.PayloadBuilder import *
from mythic import mythic

class UseArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            # TODO: add arguments here for mtls
            CommandParameter(
                name="id",
                description="Which uuid to use.",
                type=ParameterType.String
            ),
        ]

    async def parse_arguments(self):
        self.load_args_from_json_string(self.command_line)


class Use(CommandBase):
    cmd = "use"
    needs_admin = False
    help_cmd = "use"
    description = "Use an implant."
    version = 1
    author = "Spencer Adolph"
    argument_class = UseArguments
    attackmapping = []

    async def create_go_tasking(self, taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        client = await SliverAPI.create_sliver_client(taskData)
        
        # query to confirm uuid
        # TODO: determine if session or beacon uuid
        sliver_id = taskData.args.get_arg('id')
        beacon_info = await client.beacon_by_id(sliver_id)
        session_info = await client.session_by_id(sliver_id)

        if (not beacon_info and not session_info):
            response = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
                TaskID=taskData.Task.ID,
                Success=False,
                Completed=True,
                Error="id not found in sliver",
                TaskStatus="id not found in sliver",
                # DisplayParams="id not found in sliver!"
            )
            return response
        
        isBeacon = beacon_info is not None
        implant_info = beacon_info or session_info

        # check if payload already exists, if so, skip to creating the callback
        search = await SendMythicRPCPayloadSearch(MythicRPCPayloadSearchMessage(
            PayloadUUID=sliver_id
        ))

        if (len(search.Payloads) == 0):
            # create the payload
            # TODO: figure out mappings for windows or mac...
            sliver_os_table = {
                'linux': 'Linux'
            }

            new_payload = MythicRPCPayloadCreateFromScratchMessage(
                TaskID=taskData.Task.ID,
                PayloadConfiguration=MythicRPCPayloadConfiguration(
                    payload_type="sliverimplant",
                    uuid=sliver_id,
                    selected_os=sliver_os_table[implant_info.OS],                 
                    description=f"sliver {'beaconing' if isBeacon else 'interactive'} implant for {sliver_id}",
                    build_parameters=[],
                    c2_profiles=[],
                    commands=['ifconfig', 'download', 'upload', 'ls', 'ps', 'netstat', 'cat', 'cd', 'pwd', 'execute', 'mkdir']
                ),
            )
            await SendMythicRPCPayloadCreateFromScratch(new_payload)

        # create the callback
        # TODO: Probably a way to document this 'Type' for intellisense
        extraInfo = json.dumps({
            # TODO: if buildparams changes, then this won't work anymore (could make it more resilient)
            "slivercfg_fileid": taskData.BuildParameters[0].Value,
            "type": 'beacon' if isBeacon else 'session'
        })
        await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
            PayloadUUID=sliver_id,
            C2ProfileName="",
            IntegrityLevel=3,
            Host=implant_info.Hostname,
            User=implant_info.Username,
            Ip=implant_info.RemoteAddress.split(':')[0],
            ExtraInfo=extraInfo,
            PID=implant_info.PID
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
