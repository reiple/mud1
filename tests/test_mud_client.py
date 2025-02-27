import pytest
from unittest.mock import Mock, patch
from src.mud_client import MUDClient

class TestMUDClient:
    @pytest.fixture
    def mud_client(self):
        return MUDClient()

    @pytest.mark.asyncio
    async def test_client_start(self, mud_client):
        """Test client startup and connection"""
        with patch('src.connection.MUDConnection') as mock_connection:
            mock_connection_instance = Mock()
            mock_connection.return_value = mock_connection_instance
            mock_connection_instance.is_connected.return_value = False
            
            # Simulate immediate quit
            with patch('builtins.input', return_value='quit'):
                await mud_client.start("localhost", 4000)
            
            mock_connection_instance.connect.assert_called_once_with("localhost", 4000)
            assert not mud_client.running

    @pytest.mark.asyncio
    async def test_client_command_sending(self, mud_client):
        """Test sending commands to the server"""
        with patch('src.connection.MUDConnection') as mock_connection:
            mock_connection_instance = Mock()
            mock_connection.return_value = mock_connection_instance
            mock_connection_instance.is_connected.return_value = True
            
            # Simulate one command then quit
            with patch('builtins.input', side_effect=['look', 'quit']):
                await mud_client.start("localhost", 4000)
            
            # Verify the command was sent
            mock_writer = mock_connection_instance._writer
            mock_writer.write.assert_called_with("look\n")
