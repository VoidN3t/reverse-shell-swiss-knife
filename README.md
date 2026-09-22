# Reverse Shell Swiss Knife

A small interactive terminal utility for generating reverse-shell commands and PHP web-shell files for authorized security testing, lab environments, and capture-the-flag exercises.

> **Warning:** Reverse shells provide remote command execution. Use this project only on systems and networks that you own or have explicit permission to test. Do not use generated payloads against third-party systems.

## Features

- Interactive terminal menu powered by [`simple-term-menu`](https://pypi.org/project/simple-term-menu/).
- Bash reverse-shell command generation:
  - Base64-encoded command output.
  - Plaintext command output.
- PHP reverse-shell generation:
  - Save a configured PHP web-shell file to a chosen path.
  - Print a PHP one-liner command.
- Python reverse-shell command generation:
  - Base64-encoded command output.
  - Plaintext command output.
- Configurable callback IP address and listener port.

## Requirements

- Python 3.
- A Unix-like environment for using the generated Bash, PHP, or Python commands.
- `pip` for installing the Python dependency.

## Installation

Clone the repository and create an isolated virtual environment:

```bash
git clone https://github.com/VoidN3t/reverse-shell-swiss-knife.git
cd reverse-shell-swiss-knife
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

A prebuilt binary is also published in the repository's GitHub Releases. This binary is intended to let you run the tool without installing Python and the project dependencies locally, while still using the same interactive menu and payload generation features described in this project. Download the release for your platform, verify it is the official artifact from this repository, and use it only in authorized lab or test environments.

## Usage

Start the interactive menu:

```bash
python3 app.py
```

Choose a shell type, enter the IP address of the authorized listener, and provide the listener port. The tool then prints the selected command or writes the generated PHP file to disk.

### Start a listener

For an authorized lab or test environment, start a TCP listener on the same IP and port configured in the application. For example:

```bash
nc -lvnp 4444
```

The listener must be running and reachable before a generated command is executed.

## Menu options

### Bash

- **Encrypted Bash**: Base64-encodes the generated Bash command and prints a decode-and-execute form.
- **Plaintext Bash**: Prints the Bash command directly.

### PHP

- **PHP web file**: Creates a PHP file configured with the supplied callback IP and port.
- **PHP command**: Prints a PHP one-liner configured with the supplied callback IP and port.

### Python

- **Encrypted Python**: Base64-encodes the generated Python command and prints a decode-and-execute form.
- **Plaintext Python**: Prints the Python command directly.

## Project structure

```text
.
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Security considerations

- Treat generated commands and PHP files as security-sensitive artifacts.
- Do not commit generated payloads, callback addresses, credentials, or test data.
- Restrict listeners to isolated networks whenever possible.
- Remove generated PHP files after testing and verify that no unauthorized copy remains deployed.
- Base64 encoding is **not encryption**; it only changes the representation of a command.
- Review every generated command before executing it.

## Limitations

- The tool does not start a listener automatically.
- It does not validate IP addresses, ports, or generated payloads.
- Generated commands depend on the target system having the required shell, interpreter, and network access.
- Behavior may vary across operating systems and shell implementations.

## Contributing

Contributions are welcome. When submitting changes, please include a clear description, keep generated artifacts out of commits, and test updates in an isolated environment.

## License

No license is currently specified for this repository. Until a license is added, all rights are reserved by the copyright holder.
