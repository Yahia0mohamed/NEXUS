from agents.nexus_agent.NexusChatAgent import NexusChatAgent
import pyfiglet
from colorama import Fore, Style, init

import cmd

class NexusShell(cmd.Cmd):
    intro = "Welcome to NEXUS! Type 'help' or 'x' to exit."
    prompt = "Ask NEXUS: "

    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    def default(self, line):
        """Handle any input that's not a command"""
        if line.strip().lower() == "x":
            print("👋 Exiting NEXUS. Goodbye!")
            return True  # stops the loop

        response = self.agent.chat(user_input=line)
        print("\nNEXUS:", response, "\n")

# Initialize colorama
init(autoreset=True)

def print_banner():
    ascii_banner = pyfiglet.figlet_format("NEXUS")
    print(Fore.CYAN + Style.BRIGHT + ascii_banner)
    print(Fore.BLUE + "Welcome to NEXUS ⚡")
    print(Fore.YELLOW + "Your Favourite Code Assistant!")
    print(Fore.GREEN + "Start Chatting with NEXUS " + Fore.RED + "IF YOU WANT TO EXIT PRESS x")

if __name__ == "__main__":
    agent = NexusChatAgent()
    print_banner()
    NexusShell(agent).cmdloop()