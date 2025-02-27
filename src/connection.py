import asyncio
import socket

# Telnet protocol constants
IAC = bytes([255])  # Interpret As Command
DONT = bytes([254])
DO = bytes([253])
WONT = bytes([252])
WILL = bytes([251])
ECHO = bytes([1])    # Echo option

class MUDConnection:
    """Handles the connection to a MUD server"""
    
    def __init__(self):
        self._reader = None
        self._writer = None
        self._connected = False

    def is_connected(self) -> bool:
        """Returns whether the client is currently connected to a server"""
        return self._connected

    async def _negotiate_telnet_options(self):
        """텔넷 옵션 협상 - 자국반향(echo) 설정"""
        # WILL ECHO - 클라이언트가 에코를 수행하겠다고 서버에 알림
        self._writer.write(IAC + WILL + ECHO)
        await self._writer.drain()

    async def connect(self, host: str, port: int) -> None:
        """
        Establishes a connection to the MUD server
        
        Args:
            host: The hostname or IP address of the MUD server
            port: The port number to connect to
        """
        try:
            self._reader, self._writer = await asyncio.open_connection(host, port)
            self._connected = True
            await self._negotiate_telnet_options()
        except Exception as e:
            print(f"Connection error: {e}")
            self._connected = False
            raise

    async def disconnect(self) -> None:
        """Closes the connection to the MUD server"""
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
            self._connected = False
            self._reader = None
            self._writer = None

    async def send_command(self, command: str) -> None:
        """
        Sends a command to the MUD server
        
        Args:
            command: The command to send
        """
        if not self.is_connected():
            raise ConnectionError("Not connected to server")
            
        try:
            # 명령어를 보내기 전에 로컬에서 에코
            print(f"> {command}")
            
            self._writer.write(f"{command}\r\n".encode('euc-kr'))
            await self._writer.drain()
        except Exception as e:
            print(f"Send error: {e}")
            raise

    async def receive_response(self, buffer_size: int = 4096) -> str:
        """
        Receives a response from the MUD server
        
        Args:
            buffer_size: Size of the read buffer in bytes
            
        Returns:
            str: The response from the server
        """
        if not self.is_connected():
            raise ConnectionError("Not connected to server")
            
        try:
            raw_data = await self._reader.read(buffer_size)
            if not raw_data:
                return ""
                
            # 텔넷 명령어 처리
            response = b""
            i = 0
            while i < len(raw_data):
                if raw_data[i:i+1] == IAC and i + 2 < len(raw_data):
                    # 텔넷 명령어 스킵 (3바이트)
                    i += 3
                else:
                    response += raw_data[i:i+1]
                    i += 1
                    
            return response.decode('euc-kr', errors='replace')
        except Exception as e:
            print(f"Receive error: {e}")
            return ""
