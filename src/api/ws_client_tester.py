import asyncio
from websockets.client import connect

async def main():
    async with connect("ws://localhost:1234") as ws:
        await ws.send("Hello world!")
        message = await ws.recv()
        print(str(message))

if __name__ == "__main__":
    asyncio.run(main())