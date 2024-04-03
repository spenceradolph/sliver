import pathlib
from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *


class BasicPythonAgent(PayloadType):
    name = "sliver"
    file_extension = ""
    author = "Spencer Adolph"
    supported_os = [SupportedOS("sliver")]
    wrapper = False
    wrapped_payloads = []
    note = """This payload connects to sliver."""
    supports_dynamic_loading = False
    c2_profiles = []
    mythic_encrypts = False
    translation_container = None # "myPythonTranslation"
    build_parameters = [
        BuildParameter(
            name="CONFIGTEXT",
            description="Sliver Operator Config (paste string)",
            parameter_type=BuildParameterType.String,
            default_value="Paste Here"
        ),
        # BuildParameter(
        #     name="CONFIGFILE",
        #     description="Sliver Operator Config (select file)",
        #     parameter_type=BuildParameterType.File,
        # )
    ]
    agent_type = "service"
    agent_path = pathlib.Path(".") / "sliver"
    agent_icon_path = agent_path / "agent_functions" / "sliver.svg"
    agent_code_path = agent_path / "agent_code"

    build_steps = [
        BuildStep(step_name="Gathering Files", step_description="Making sure all commands have backing files on disk"),
        BuildStep(step_name="Configuring", step_description="Stamping in configuration values")
    ]

    async def build(self) -> BuildResponse:
        # this function gets called to create an instance of your payload
        resp = BuildResponse(status=BuildStatus.Success)
        ip = "127.0.0.1"
        create_callback = await SendMythicRPCCallbackCreate(MythicRPCCallbackCreateMessage(
            PayloadUUID=self.uuid,
            C2ProfileName="",
            User="Sliver",
            Host="Sliver",
            Ip=ip,
            IntegrityLevel=3,
        ))
        if not create_callback.Success:
            logger.info(create_callback.Error)
        else:
            logger.info(create_callback.CallbackUUID)
        return resp
