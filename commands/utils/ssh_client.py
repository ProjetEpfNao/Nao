import paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.44', username='nao',
            password='nao')

ssh.exec_command("cd /home/nao/commands")
stdin, stdout, stderr = ssh.exec_command("ls")
for line in stdout.readlines():
    print line.strip()
stdin, stdout, stderr = ssh.exec_command("python nao.py")
