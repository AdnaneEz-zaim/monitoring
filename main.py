import paramiko

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

client.connect(hostname="leodagan.telecomste.net", username="grudu", password="113-TgBT-3784", port=22113)

command="ls"
_, stdout, stderr = client.exec_command(command)
output = stdout.read().decode("utf-8")
for line in output.splitlines():
    print(line)
