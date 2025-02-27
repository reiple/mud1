import asyncio
from connection import MUDConnection

class MUDClient:
    """Main MUD client class that handles user interaction"""
    
    def __init__(self):
        self.connection = MUDConnection()
        self.running = False

    async def start(self, host: str, port: int):
        """
        Starts the MUD client and connects to the server
        
        Args:
            host: The hostname or IP address of the MUD server
            port: The port number to connect to
        """
        try:
            await self.connection.connect(host, port)
            self.running = True
            await self._main_loop()
        except Exception as e:
            print(f"Error connecting to server: {e}")
        finally:
            if self.connection.is_connected():
                await self.connection.disconnect()

    async def _main_loop(self):
        """Main game loop that handles input and output"""
        while self.running:
            try:
                # Handle user input
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, input, "> "
                )
                
                if user_input.lower() == "quit":
                    self.running = False
                    continue

                # Send command to server
                if self.connection.is_connected():
                    await self.connection.send_command(user_input)

                # Read server response
                if self.connection.is_connected():
                    response = await self.connection.receive_response()
                    if response:
                        print(response, end="")

            except Exception as e:
                print(f"Error: {e}")
                self.running = False

if __name__ == "__main__":
    client = MUDClient()
    asyncio.run(client.start("146.56.104.221", 8000))
