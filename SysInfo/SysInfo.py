import os
import platform
import socket
import time
import psutil
from colorama import Fore, init,Style

# Inicializa o colorama para saída colorida no terminal
init(autoreset=True)
Imagem=f"""    Software-Uso somente pra propositos educacionais
    Author:Jamal Achire
    Tiktok:P1UN-TECH
    Youtube:P1UN-TECH

        {Fore.GREEN}    ____ _____  ___   __
                      / __ <  / / / / | / /
                     / /_/ / / / / /  |/ / 
                    / ____/ / /_/ / /|  /  
                   /_/   /_/\____/_/ |_/   
                  / 
                 /
        .--. _  /
       |o_o |
       |:_/ |
      //   \ \\
     (|     | )
    /'\_   _/`\\
    \___)=(___/  🇲🇿
{Style.RESET_ALL}
"""
print(Imagem)
def detectar_usb():
    """Detecta a inserção de um USB e retorna o caminho onde ele está montado."""
    sistema = platform.system()

    if sistema == "Linux":
        caminho_usb = "/media/"  # Pode ser alterado conforme necessário
        print("Aguardando um dispositivo USB...")

        dispositivos_iniciais = set(os.listdir(caminho_usb))

        while True:
            time.sleep(2)
            dispositivos_atuais = set(os.listdir(caminho_usb))
            novos_dispositivos = dispositivos_atuais - dispositivos_iniciais  # Detecta novo USB

            if novos_dispositivos:
                for dispositivo in novos_dispositivos:
                    caminho_montagem = os.path.join(caminho_usb, dispositivo)
                    print(f"USB inserido: {caminho_montagem}")
                    return caminho_montagem  # Retorna o caminho de montagem do USB

            dispositivos_iniciais = dispositivos_atuais

    elif sistema == "Windows":
        print("Aguardando um dispositivo USB...")

        def obter_dispositivos_usb():
            """Retorna um dicionário com os dispositivos USB conectados e seus caminhos."""
            return {disco.device: disco.mountpoint for disco in psutil.disk_partitions() if 'removable' in disco.opts}

        dispositivos_iniciais = obter_dispositivos_usb()

        while True:
            time.sleep(2)
            dispositivos_atuais = obter_dispositivos_usb()
            novos_dispositivos = {dev: caminho for dev, caminho in dispositivos_atuais.items() if dev not in dispositivos_iniciais}

            if novos_dispositivos:
                for dev, caminho in novos_dispositivos.items():
                    print(f"USB inserido: {caminho}")
                    return caminho  # Retorna o caminho de montagem do USB

            dispositivos_iniciais = dispositivos_atuais


def principal():
    """Coleta informações do sistema e salva em um arquivo dentro do USB conectado."""
    informacoes_sistema = (
        f"{Fore.GREEN}Usuário: {os.getlogin()}\n"
        f"Sistema: {platform.system()}\n"
        f"Versão: {platform.version()}"
    )
    print(informacoes_sistema)

    # Obtém o endereço IP do dispositivo
    nome_host = socket.gethostname()
    endereco_ip = socket.gethostbyname(nome_host)
    print(f"IP: {endereco_ip}")

    # Detecta o USB e obtém seu caminho de montagem
    caminho_usb = detectar_usb()

    # Cria o conteúdo a ser salvo no arquivo
    dados_para_salvar = f"{informacoes_sistema}\nIP: {endereco_ip}"

    # Salva as informações dentro do dispositivo USB
    if caminho_usb:
        caminho_arquivo = os.path.join(caminho_usb, "dados.txt")
        try:
            with open(caminho_arquivo, "w") as arquivo:
                arquivo.write(dados_para_salvar)
            print(f"Informações salvas em: {caminho_arquivo}")
        except Exception as erro:
            print(f"Erro ao salvar o arquivo: {erro}")

if __name__ == "__main__":
    principal()
