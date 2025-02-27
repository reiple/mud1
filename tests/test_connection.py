import pytest
from unittest.mock import Mock, patch
from src.connection import MUDConnection

class TestMUDConnection:
    @pytest.fixture
    def mud_connection(self):
        return MUDConnection()

    @pytest.mark.asyncio
    async def test_connect_success(self, mud_connection):
        """Test successful connection to MUD server"""
        with patch('telnetlib3.open_connection') as mock_connect:
            mock_reader = Mock()
            mock_writer = Mock()
            mock_connect.return_value = (mock_reader, mock_writer)
            
            await mud_connection.connect("localhost", 4000)
            
            assert mud_connection.is_connected()
            mock_connect.assert_called_once_with("localhost", 4000)

    @pytest.mark.asyncio
    async def test_disconnect(self, mud_connection):
        """Test disconnection from MUD server"""
        with patch('telnetlib3.open_connection') as mock_connect:
            mock_reader = Mock()
            mock_writer = Mock()
            mock_connect.return_value = (mock_reader, mock_writer)
            
            await mud_connection.connect("localhost", 4000)
            await mud_connection.disconnect()
            
            assert not mud_connection.is_connected()
            mock_writer.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_command(self, mud_connection):
        """Test sending a command to the server"""
        with patch('telnetlib3.open_connection') as mock_connect:
            mock_reader = Mock()
            mock_writer = Mock()
            mock_connect.return_value = (mock_reader, mock_writer)
            
            await mud_connection.connect("localhost", 4000)
            await mud_connection.send_command("look")
            
            mock_writer.write.assert_called_with("look\n")
            mock_writer.drain.assert_called_once()

    @pytest.mark.asyncio
    async def test_receive_response(self, mud_connection):
        """Test receiving response from the server"""
        with patch('telnetlib3.open_connection') as mock_connect:
            mock_reader = Mock()
            mock_writer = Mock()
            mock_connect.return_value = (mock_reader, mock_writer)
            
            mock_reader.read = Mock(return_value="You see a dark room\n")
            
            await mud_connection.connect("localhost", 4000)
            response = await mud_connection.receive_response()
            
            assert response == "You see a dark room\n"
            mock_reader.read.assert_called_once_with(4096)
