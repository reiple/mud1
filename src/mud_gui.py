import tkinter as tk
from tkinter import ttk
import asyncio
from mud_client import MUDClient

class MUDClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MUD Client")
        
        # Server connection info
        self.host = "146.56.104.221"
        self.port = 8000
        
        # Initialize MUD client
        self.client = MUDClient()
        
        # Command history
        self.command_history = []
        self.MAX_HISTORY_SIZE = 50
        self.history_index = 0
        
        self._setup_gui()
        self._setup_bindings()

    def _setup_gui(self):
        """Set up the GUI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="3")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button frame for controls
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Reconnect button
        self.reconnect_button = ttk.Button(button_frame, text="Reconnect", command=self.reconnect)
        self.reconnect_button.pack(side=tk.LEFT, padx=2)
        
        # Output area
        self.output_area = tk.Text(main_frame, wrap=tk.WORD, height=24, width=80)
        self.output_area.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.output_area.config(state='disabled')
        
        # Scrollbar for output area
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.output_area.yview)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.output_area['yscrollcommand'] = scrollbar.set
        
        # Command input field
        self.command_input = ttk.Entry(main_frame, width=80)
        self.command_input.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # Send button
        self.send_button = ttk.Button(main_frame, text="Send", command=self.send_command)
        self.send_button.grid(row=2, column=1, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Set focus to input field
        self.command_input.focus()

    def _setup_bindings(self):
        """Set up key bindings"""
        self.command_input.bind('<Return>', self.send_command)
        self.command_input.bind('<Up>', self.previous_command)
        self.command_input.bind('<Down>', self.next_command)

    def reconnect(self):
        """Reconnect to the MUD server"""
        self.display_response("Reconnecting to server...\n")
        asyncio.create_task(self._async_reconnect())

    async def _async_reconnect(self):
        """Asynchronously reconnect to the server"""
        try:
            # Disconnect if already connected
            if self.client.connection.is_connected():
                await self.client.connection.disconnect()
            
            # Try to reconnect
            await self.client.start(self.host, self.port)
            self.display_response("Successfully reconnected to server.\n")
        except Exception as e:
            self.display_response(f"Reconnection failed: {e}\n")

    def send_command(self, event=None):
        """Send the command to the server"""
        command = self.command_input.get().strip()
        if command:
            # Add to history
            self.command_history.insert(0, command)
            if len(self.command_history) > self.MAX_HISTORY_SIZE:
                self.command_history.pop()
            self.history_index = -1
            
            # Clear input field
            self.command_input.delete(0, tk.END)
            
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
        self.output_area.config(state='normal')
        self.output_area.insert(tk.END, response)
        self.output_area.see(tk.END)
        self.output_area.config(state='disabled')

    def previous_command(self, event=None):
        """Show previous command from history"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_input.delete(0, tk.END)
            self.command_input.insert(0, self.command_history[self.history_index])

    def next_command(self, event=None):
        """Show next command from history"""
        if self.history_index > 0:
            self.history_index -= 1
            self.command_input.delete(0, tk.END)
            self.command_input.insert(0, self.command_history[self.history_index])
        elif self.history_index == 0:
            self.history_index = -1
            self.command_input.delete(0, tk.END)

    async def start(self, host: str, port: int):
        """Start the MUD client and connect to server"""
        self.host = host
        self.port = port
        try:
            await self.client.start(host, port)
        except Exception as e:
            self.display_response(f"Connection error: {e}\n")

def main():
    root = tk.Tk()
    gui = MUDClientGUI(root)
    asyncio.run(gui.start("146.56.104.221", 8000))
    root.mainloop()

if __name__ == "__main__":
    main()
