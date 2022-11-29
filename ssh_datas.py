import sys
import os

def main():
    print os.name

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'deploy':
            import paramiko

            # Connect to remote host
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname="leodagan.telecomste.net", username="grudu", password="113-TgBT-3784", port=22113)

            # Setup sftp connection and transmit this script
            sftp = client.open_sftp()
            sftp.put(__file__, '/tmp/myscript.py')
            sftp.close()

            # Run the transmitted script remotely without args and show its output.
            # SSHClient.exec_command() returns the tuple (stdin,stdout,stderr)
            stdout = client.exec_command('python /tmp/myscript.py')[1]
            for line in stdout:
                # Process each line in the remote output
                print line

            client.close()
            sys.exit(0)
    except IndexError:
        pass

    # No cmd-line args provided, run script normally
    main()