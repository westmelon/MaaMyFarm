from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction
from utils import logger

import json
import time


@AgentServer.custom_action("Collect")
class Collect(CustomAction):
    # corn/grape/wheat
    def CollectByType(type: str, context: Context):
        return
    
    # 收集农作物
    def CollectCrops(self, context: Context):

        Count = 5
        while Count > 0:
            img = context.tasker.controller.post_screencap().wait().get()
            findDetail = context.run_recognition(
                "collect_find_corn",
                img,
                pipeline_override={
                    "collect_find_corn": {
                        "recognition": "TemplateMatch",
                        "template": "crop_corn.png",
                        "threshold": 0.65,
                    }
                },
            )

            if findDetail:
                logger.info(f"找到grape{len(findDetail.all_results)}个, 开始采集")
                matureDetail = context.run_recognition(
                    "collect_find_mature_corn",
                    img,
                    pipeline_override={
                        "collect_find_mature_corn": {
                            "recognition": "TemplateMatch",
                            "template": "crop_corn_growup.png",
                            "threshold": 0.65,
                            "action": "Click",
                            "target_offset": [
                                20,
                                10,
                                0,
                                0
                            ],
                            "post_delay": 3000,
                        }
                    },
                )
            Count -= 1
            
        return True

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        # taskList: dict = json.loads(argv.custom_action_param)
        # print(taskList)
        # if not taskList:
        #     return CustomAction.RunResult(success=True)
        print("my_action_111 is running!")
        # execute task
        logger.info("开始采集农作物")
        # self.EnterShop(context, "旅行商人")
        self.CollectCrops(context)


        logger.info("采集完成 任务结束")
        return CustomAction.RunResult(success=True)
