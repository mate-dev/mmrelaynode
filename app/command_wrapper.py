import os
import subprocess
import time

output_file = '/home/mesh/app/command_output.txt'
flag_file = '/home/mesh/app/.commands_executed'

# Remove the output file if it exists
if os.path.exists(output_file):
    os.remove(output_file)

def log_to_file(message):
    with open(output_file, 'a') as f:
        f.write(message + "\n")

def execute_meshtastic_command(options):
    """Execute a meshtastic command with the given options."""
    command = ["meshtastic", "--host", "mmrelaydevice", "--port", "4403"] + options.split()
    log_to_file(f"Executing command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    log_to_file("Standard Output:\n" + result.stdout)
    log_to_file("Standard Error:\n" + result.stderr)
    time.sleep(1)  # Pause for 1 second between commands

if os.path.exists(flag_file):
    log_to_file("Commands have already been executed previously. Skipping.")
else:
    # Print all environment variables at the start
    log_to_file("All environment variables:\n" + str(os.environ))

    # Loop through environment variables in sequence
    index = 1
    while True:
        command = os.environ.get(f'MESHTASTIC_COMMAND_{index}')
        if command:
            log_to_file(f"Found command variable: MESHTASTIC_COMMAND_{index} with value: {command}")
            execute_meshtastic_command(command)
            index += 1
        else:
            log_to_file(f"No more MESHTASTIC_COMMAND variables found, ending at index {index-1}.")
            # Create the flag file to indicate that all commands have been executed.
            with open(flag_file, 'w') as f:
                f.write("Commands executed on: " + time.ctime())
            break