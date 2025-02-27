import sys
import asyncio
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QPushButton, QTextEdit, QLineEdit)
from PyQt6.QtCore import Qt, QTimer
from mud_client import MUDClient

class MUDClientGUI(QMainWindow):
    def __init__(self, host="146.56.104.221", port=8000):
        super().__init__()
        
        # Server connection info
        self.host = host
        self.port = port
        
        # Initialize MUD client
        self.client = MUDClient()
        
        # Command history
        self.command_history = []
        self.MAX_HISTORY_SIZE = 50
        self.history_index = -1
        
        self._init_ui()
        self._setup_connections()
        
        # Start connection after GUI is ready
        QTimer.singleShot(100, self._initial_connect)
        
    def _init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("MUD Client")
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Button layout
        button_layout = QHBoxLayout()
        self.reconnect_button = QPushButton("Reconnect")
        button_layout.addWidget(self.reconnect_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)
        
        # Input layout
        input_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command...")
        input_layout.addWidget(self.command_input)
        
        self.send_button = QPushButton("Send")
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        
        # Set focus to input field
        self.command_input.setFocus()
        
    def _setup_connections(self):
        """Set up signal connections"""
        self.reconnect_button.clicked.connect(self.reconnect)
        self.send_button.clicked.connect(self.send_command)
        self.command_input.returnPressed.connect(self.send_command)
        
        # Key press event for command history
        self.command_input.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        """Handle key press events for command history"""
        if obj is self.command_input and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Up:
                self._previous_command()
                return True
            elif event.key() == Qt.Key.Key_Down:
                self._next_command()
                return True
        return super().eventFilter(obj, event)
        
    def _initial_connect(self):
        """Initial connection attempt after GUI is ready"""
        self.display_response(f"Connecting to {self.host}:{self.port}...\n")
        asyncio.create_task(self._async_connect())
        
    async def _async_connect(self):
        """Asynchronously connect to the server"""
        try:
            await self.client.start(self.host, self.port)
            self.display_response("Successfully connected to server.\n")
        except Exception as e:
            self.display_response(f"Connection failed: {e}\n")
            
    def reconnect(self):
        """Reconnect to the MUD server"""
        self.display_response("Reconnecting to server...\n")
        asyncio.create_task(self._async_reconnect())
        
    async def _async_reconnect(self):
        """Asynchronously reconnect to the server"""
        try:
            if self.client.connection.is_connected():
                await self.client.connection.disconnect()
            await self.client.start(self.host, self.port)
            self.display_response("Successfully reconnected to server.\n")
        except Exception as e:
            self.display_response(f"Reconnection failed: {e}\n")
            
    def send_command(self):
        """Send the command to the server"""
        command = self.command_input.text().strip()
        if command:
            # Add to history
            self.command_history.insert(0, command)
            if len(self.command_history) > self.MAX_HISTORY_SIZE:
                self.command_history.pop()
            self.history_index = -1
            
            # Clear input field
            self.command_input.clear()
            
            # Send command
            asyncio.create_task(self._async_send_command(command))
            
    async def _async_send_command(self, command):
        """Asynchronously send command to server"""
        try:
            await self.client.send_command(command)
        except Exception as e:
            self.display_response(f"Error: {e}\n")
            
    def display_response(self, response):
        """Display response in the output area"""
        self.output_area.moveCursor(self.output_area.textCursor().End)
        self.output_area.insertPlainText(response)
        self.output_area.moveCursor(self.output_area.textCursor().End)
        
    def _previous_command(self):
        """Show previous command from history"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_input.setText(self.command_history[self.history_index])
            
    def _next_command(self):
        """Show next command from history"""
        if self.history_index > 0:
            self.history_index -= 1
            self.command_input.setText(self.command_history[self.history_index])
        elif self.history_index == 0:
            self.history_index = -1
            self.command_input.clear()

class AsyncHelper:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
    def run_forever(self):
        self.loop.run_forever()
        
def main():
    # Initialize Qt application
    app = QApplication(sys.argv)
    
    # Set up asyncio loop
    helper = AsyncHelper()
    
    # Create and show the GUI
    window = MUDClientGUI()
    window.show()
    
    # Run event loops
    timer = QTimer()
    timer.timeout.connect(lambda: None)  # Required for Qt to process events
    timer.start(50)  # 50ms interval
    
    try:
        app.exec()
    finally:
        helper.loop.stop()

if __name__ == "__main__":
    main()
