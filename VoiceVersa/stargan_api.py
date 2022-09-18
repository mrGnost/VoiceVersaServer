import time
from pydub import AudioSegment
from paramiko import Transport, SFTPClient, SSHClient, AutoAddPolicy


host = "cluster.hpc.hse.ru"
port = 2222
user = "damenschikov"
password = "Ahd6fohm"


def process_audio(audio, voice):
    # audio, is_mp3 = mp3_to_wav(audio)
    modify_script(audio, voice)
    send_audio(audio)
    start_processing_script()
    get_processed_audio(audio)
    # if is_mp3:
    #     wav_to_mp3(audio)


def mp3_to_wav(audio):
    root = 'uploads/custom_audio/'
    if audio.split('.')[-1] == 'wav':
        return audio, False
    sound = AudioSegment.from_mp3(root + audio)
    new_name = audio[:-3] + 'wav'
    sound.export(root + new_name, format='wav')
    return new_name, True


def wav_to_mp3(audio):
    root = 'uploads/processed_audio/'
    sound = AudioSegment.from_wav(root + audio)
    sound.export(root + audio[:-3] + 'mp3', format='mp3')


def send_audio(audio):
    transport = Transport((host, port))
    transport.connect(username=user, password=password)
    sftp = SFTPClient.from_transport(transport)
    sftp.put("uploads/custom_audio/" + audio, "/home/damenschikov/stargan/StarGAN/audio/source/" + audio)
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
            sftp.get("/home/damenschikov/stargan/StarGAN/audio/result/" + audio, "uploads/processed_audio/" + audio)
            break
        except IOError:
            time.sleep(60)

    sftp.close()
    transport.close()
