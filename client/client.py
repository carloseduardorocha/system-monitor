#!/usr/bin/env python3
"""
Cliente de Monitoramento
Coleta informações do sistema e envia via UDP para o servidor
"""

import socket
import json
import time
import psutil
from config import SERVER_IP, SERVER_PORT, INTERVALO_COLETA, IP_DESTINO


def obter_ip_local():
    """Obtém o IP local da máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def coletar_uso_memoria():
    """Retorna a taxa de utilização de memória em %"""
    memoria = psutil.virtual_memory()
    return round(memoria.percent, 2)


def coletar_uso_cpu():
    """Retorna a taxa de uso do processador em %"""
    return round(psutil.cpu_percent(interval=1), 2)


def coletar_uso_disco():
    """Retorna a taxa de utilização do disco baseada em KB/s (igual monitor do sistema)"""
    try:
        # Primeira leitura
        io1 = psutil.disk_io_counters()
        time.sleep(1)  # 1 segundo para calcular por segundo
        io2 = psutil.disk_io_counters()
        
        # Calcula bytes lidos e escritos no último segundo
        read_bytes = io2.read_bytes - io1.read_bytes
        write_bytes = io2.write_bytes - io1.write_bytes
        
        # Converte para KB/s
        read_kbs = read_bytes / 1024
        write_kbs = write_bytes / 1024
        total_kbs = read_kbs + write_kbs
        
        # Converte para porcentagem
        # Usar 10000 KB/s (10 MB/s) como 100% - uso intenso típico
        # Ajuste esse valor conforme necessário:
        # - 5000 KB/s = mais sensível
        # - 20000 KB/s = menos sensível
        percent = min((total_kbs / 10000) * 100, 100)
        
        return round(percent, 2)
    except:
        return 0.0


def coletar_processos():
    """Retorna uma string com os principais processos em execução"""
    processos = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Ordena por uso de CPU e pega os top 10
    processos_ordenados = sorted(processos, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:10]
    
    # Formata como string
    processos_str = ", ".join([f"{p['name']}:{p['pid']}" for p in processos_ordenados])
    return processos_str


def montar_pacote():
    """Monta o pacote com todas as informações coletadas"""
    pacote = {
        'ip_origem': obter_ip_local(),
        'ip_destino': IP_DESTINO,
        'uso_memoria': coletar_uso_memoria(),
        'uso_cpu': coletar_uso_cpu(),
        'uso_disco': coletar_uso_disco(),
        'processos': coletar_processos()
    }
    return pacote


def enviar_pacote(sock, pacote):
    """Envia o pacote via UDP para o servidor"""
    try:
        # Serializa o pacote em JSON
        dados = json.dumps(pacote).encode('utf-8')
        
        # Envia via UDP
        sock.sendto(dados, (SERVER_IP, SERVER_PORT))
        print(f"✓ Pacote enviado - CPU: {pacote['uso_cpu']}% | MEM: {pacote['uso_memoria']}% | DISCO: {pacote['uso_disco']}%")
        return True
    except Exception as e:
        print(f"✗ Erro ao enviar pacote: {e}")
        return False


def main():
    """Função principal do cliente"""
    print("=" * 60)
    print("CLIENTE DE MONITORAMENTO")
    print("=" * 60)
    print(f"Servidor: {SERVER_IP}:{SERVER_PORT}")
    print(f"Intervalo de coleta: {INTERVALO_COLETA} segundos")
    print(f"IP Local: {obter_ip_local()}")
    print("=" * 60)
    print("Iniciando monitoramento... (Ctrl+C para parar)")
    print()
    
    # Cria socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            # Coleta e monta o pacote
            pacote = montar_pacote()
            
            # Envia para o servidor
            enviar_pacote(sock, pacote)
            
            # Aguarda o próximo intervalo
            time.sleep(INTERVALO_COLETA)
            
    except KeyboardInterrupt:
        print("\n\nMonitoramento interrompido pelo usuário.")
    finally:
        sock.close()
        print("Cliente encerrado.")


if __name__ == "__main__":
    main()