import pathlib
from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *


class SliverImplant(PayloadType):
    name = "sliverimplant"
    author = "Spencer Adolph"
    note = """This payload connects to sliver to interact with a specific implant."""
    supported_os = [SupportedOS.Windows, SupportedOS.Linux, SupportedOS.MacOS]
    file_extension = ""
    wrapper = False
    wrapped_payloads = []
    supports_dynamic_loading = False
    c2_profiles = []
    mythic_encrypts = False
    translation_container = None # "myPythonTranslation"
    # agent_type = ""
    agent_path = pathlib.Path(".") / "sliverimplant"
    agent_icon_path = agent_path / "agent_functions" / "sliver.svg"
    agent_code_path = agent_path / "agent_code"
    build_steps = []
    build_parameters = []

    async def build(self) -> BuildResponse:
        # TODO: ability to build payloads from Mythic instead of using 'generate' command in sliver (or with sliver meta api)
        pass
