﻿import asyncio
import math

import numpy as np
import pandas as pd
from moteus import Register

from opensourceleg.actuators.moteus import MoteusActuator
from opensourceleg.logging.logger import LOGGER


async def main():
    mc1 = MoteusActuator(
        servo_id=42,
        bus_id=3,
    )
    current_data = pd.DataFrame(
        {
            "Time": [],
            "Output_Current": [],
            "Command_Current": [],
        }
    )
    try:
        await mc1.start()
        iter = 0
        time_period = 0.001
        while True:
            iter += 1
            await mc1.update()
            print(f"######")
            print(f"{mc1.case_temperature}")
            print(f"------")

            current_data = pd.concat(
                [
                    current_data,
                    pd.DataFrame(
                        {
                            "Time": [iter * time_period],
                            "Output_Current": [mc1._data[0].values[Register.Q_CURRENT]],
                            "Command_Current": [
                                mc1._data[0].values[Register.COMMAND_Q_CURRENT]
                            ],
                        }
                    ),
                ],
                ignore_index=True,
            )
            current_data.to_csv("current_sensor_only.csv", index=False)
            await asyncio.sleep(time_period)

    finally:
        await mc1.stop()


if __name__ == "__main__":
    asyncio.run(main())
