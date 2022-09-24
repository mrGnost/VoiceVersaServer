import time
from paramiko import Transport, SFTPClient, SSHClient, AutoAddPolicy


host = "cluster.hpc.hse.ru"
port = 2222
user = "damenschikov"
password = "Ahd6fohm"


def process_audio(audio, voice):
    modify_script(audio, voice)
    send_audio(audio)
    start_processing_script()
    get_processed_audio(audio)


def send_audio(audio):
    transport = Transport((host, port))
    transport.connect(username=user, password=password)
    sftp = SFTPClient.from_transport(transport)
    sftp.put("uploads/processing/src/" + audio, "/home/damenschikov/stargan/StarGAN/audio/source/" + audio)
    sftp.put("sbatch/inference.sbatch", "/home/damenschikov/stargan/StarGAN/inference.sbatch")
    sftp.close()
    transport.close()


def modify_script(audio, voice):
    with open('sbatch/inference.sbatch', 'r', newline='\n') as f:
        lines = f.readlines()
    lines[-1] = 'python3 inference.py ' + audio + ' ' + str(voice) + '\n'
    with open('sbatch/inference.sbatch', 'w', newline='\n') as f:
        f.writelines(lines)


def start_processing_script():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cd stargan/StarGAN/; sbatch inference.sbatch')
    print(stdout.read() + stderr.read())
    client.close()


def get_processed_audio(audio):
    transport = Transport((host, port))
    transport.connect(username=user, password=password)
    sftp = SFTPClient.from_transport(transport)

    while True:
        try:
            sftp.get("/home/damenschikov/stargan/StarGAN/audio/result/" + '.'.join(audio.split('.')[:-1] + ['wav']),
                     "uploads/processing/result/" + audio)
            break
        except IOError:
            time.sleep(60)

    print("done")
    sftp.close()
    transport.close()
