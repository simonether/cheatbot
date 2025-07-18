"""
This file is for manually testing the CheatBot API client.
"""
import asyncio
import os

from cheatbot.client import CheatBotClient
from cheatbot.models.task_creation import CreateTaskParams, Interval


async def main():
    """Main function to test the CheatBot API client."""
    api_key = os.getenv("CHEATBOT_API_KEY")
    if not api_key:
        raise ValueError("CHEATBOT_API_KEY environment variable not set.")

    async with CheatBotClient(api_key) as client:
        task_params = CreateTaskParams(
            service=40,
            link="https://t.me/hornymontana",
            quantity=32,
            post=134,
            gender="random",
            duration_type="hour",
            duration_value=48,
            intervals=[
                Interval(from_time="2023-12-06T15:00:00", to_time="2023-12-06T17:00:00", speed_coefficient=-3),
                Interval(from_time="2023-12-06T17:00:00", to_time="2023-12-06T19:00:00", speed_coefficient=2),
            ],
        )
        created_task = await client.create_task(task_params)
        print(f"Task created with ID: {created_task.task.id}")


if __name__ == "__main__":
    asyncio.run(main())
