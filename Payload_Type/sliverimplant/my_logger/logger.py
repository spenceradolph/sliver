import mythic_container.MythicCommandBase
from mythic_container.LoggingBase import *
import logging
from mythic_container.MythicGoRPC import *


class MyLogger(Log):
    async def new_task(self, msg: LoggingMessage) -> None:
        logger.info(msg)
        await SendMythicRPCTaskUpdate(MythicRPCTaskUpdateMessage(
            TaskID=msg.Data.ID,
            UpdateCompleted=True,
            UpdateStatus="success",
        ))
        await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
            TaskID=msg.Data.ParentTaskID,
            Response=mythic_container.MythicCommandBase.InteractiveMessageType[msg.Data.InteractiveTaskType][0].encode()
        ))




