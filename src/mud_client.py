import asyncio
from connection import MUDConnection

class MUDClient:
    def __init__(self):
        self.connection = MUDConnection()
        self.running = False

    async def start(self, host: str, port: int) -> None:
        """Start the MUD client and connect to server"""
        await self.connection.connect(host, port)
        self.running = True

    async def stop(self) -> None:
        """Stop the MUD client"""
        self.running = False
        await self.connection.disconnect()

    async def send_command(self, command: str) -> None:
        """Send a command to the server"""
        if not self.connection.is_connected():
            raise ConnectionError("Not connected to server")
        await self.connection.send_command(command)

    def is_running(self) -> bool:
        """Check if the client is running"""
        return self.running

if __name__ == "__main__":
    client = MUDClient()
    asyncio.run(client.start("146.56.104.221", 8000))
