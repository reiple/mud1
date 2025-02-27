import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.mud_gui import MUDClientGUI

@pytest.fixture
def app(qapp):
    return qapp

@pytest.fixture
def gui(app):
    window = MUDClientGUI()
    window.show()
    return window

def test_gui_has_input_field(gui):
    """Test that GUI has a command input field"""
    assert gui.command_input is not None
    assert gui.command_input.isEnabled()

def test_gui_has_output_area(gui):
    """Test that GUI has an output text area"""
    assert gui.output_area is not None
    assert not gui.output_area.isReadOnly() is False  # Should be read-only

def test_input_field_sends_command(gui, qtbot):
    """Test that entering a command in the input field sends it to the server"""
    command = "look"
    qtbot.keyClicks(gui.command_input, command)
    qtbot.keyClick(gui.command_input, Qt.Key.Key_Return)
    
    # Verify input field was cleared
    assert gui.command_input.text() == ""

def test_output_area_receives_response(gui):
    """Test that server responses appear in the output area"""
    test_response = "You see a dark room\n"
    gui.display_response(test_response)
    
    assert test_response in gui.output_area.toPlainText()

def test_output_area_is_read_only(gui):
    """Test that the output area is read-only"""
    assert gui.output_area.isReadOnly()

def test_input_field_has_focus(gui, qtbot):
    """Test that the input field has focus for immediate typing"""
    assert gui.command_input.hasFocus()

def test_command_history(gui, qtbot):
    """Test command history functionality"""
    commands = ["look", "north", "inventory"]
    
    for cmd in commands:
        qtbot.keyClicks(gui.command_input, cmd)
        qtbot.keyClick(gui.command_input, Qt.Key.Key_Return)
    
    # Test Up key navigation
    for cmd in reversed(commands):
        qtbot.keyClick(gui.command_input, Qt.Key.Key_Up)
        assert gui.command_input.text() == cmd

def test_reconnect_button_exists(gui):
    """Test that GUI has a reconnect button"""
    assert gui.reconnect_button is not None
    assert gui.reconnect_button.isEnabled()

def test_window_title(gui):
    """Test that the window has the correct title"""
    assert gui.windowTitle() == "MUD Client"
