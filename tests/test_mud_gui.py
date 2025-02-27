import pytest
import tkinter as tk
from src.mud_gui import MUDClientGUI
import ttk

class TestMUDClientGUI:
    @pytest.fixture
    def gui(self):
        root = tk.Tk()
        gui = MUDClientGUI(root)
        yield gui
        root.destroy()

    def test_gui_has_input_field(self, gui):
        """Test that GUI has a command input field"""
        assert gui.command_input is not None
        assert isinstance(gui.command_input, tk.Entry)

    def test_gui_has_output_area(self, gui):
        """Test that GUI has an output text area"""
        assert gui.output_area is not None
        assert isinstance(gui.output_area, tk.Text)

    def test_input_field_sends_command(self, gui, mocker):
        """Test that entering a command in the input field sends it to the server"""
        # Mock the send_command method
        mock_send = mocker.patch.object(gui.client, 'send_command')
        
        # Simulate entering a command
        gui.command_input.insert(0, "look")
        gui.send_command(None)  # Simulate Enter key press
        
        # Verify the command was sent
        mock_send.assert_called_once_with("look")
        
        # Verify input field was cleared
        assert gui.command_input.get() == ""

    def test_output_area_receives_response(self, gui):
        """Test that server responses appear in the output area"""
        test_response = "You see a dark room\n"
        gui.display_response(test_response)
        
        # Get all text from the output area
        output_text = gui.output_area.get("1.0", tk.END)
        assert test_response in output_text

    def test_output_area_is_read_only(self, gui):
        """Test that the output area is read-only"""
        assert gui.output_area['state'] == 'disabled'

    def test_input_field_has_focus(self, gui):
        """Test that the input field has focus for immediate typing"""
        assert gui.focus_get() == gui.command_input

    def test_command_history(self, gui):
        """Test command history functionality"""
        commands = ["look", "north", "inventory"]
        for cmd in commands:
            gui.command_input.insert(0, cmd)
            gui.send_command(None)
        
        assert gui.command_history == commands[::-1]  # Latest command first
        assert len(gui.command_history) <= gui.MAX_HISTORY_SIZE

    def test_reconnect_button_exists(self, gui):
        """Test that GUI has a reconnect button"""
        assert gui.reconnect_button is not None
        assert isinstance(gui.reconnect_button, ttk.Button)

    def test_reconnect_functionality(self, gui, mocker):
        """Test that reconnect button triggers reconnection"""
        # Mock the client's connect method
        mock_connect = mocker.patch.object(gui.client, 'start')
        
        # Simulate clicking reconnect button
        gui.reconnect()
        
        # Verify reconnection was attempted
        mock_connect.assert_called_once_with("146.56.104.221", 8000)
