#!/usr/bin/env python3
"""
Servidor de Monitoramento
Recebe pacotes UDP e armazena no banco de dados
"""

import socket
import json
from config import SERVER_PORT
from database import inserir_dados


def iniciar_servidor():
    """Inicia o servidor UDP"""
    # Cria socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind na porta
    sock.bind(('0.0.0.0', SERVER_PORT))
    
    print("=" * 60)
    print("SERVIDOR DE MONITORAMENTO")
    print("=" * 60)
    print(f"Escutando na porta UDP {SERVER_PORT}")
    print("Aguardando pacotes... (Ctrl+C para parar)")
    print("=" * 60)
    print()
    
    try:
        while True:
            # Recebe dados
            dados, endereco = sock.recvfrom(4096)
            
            try:
                # Decodifica JSON
                pacote = json.loads(dados.decode('utf-8'))
                
                print(f"📦 Pacote recebido de {endereco[0]}:{endereco[1]}")
                print(f"   CPU: {pacote['uso_cpu']}% | MEM: {pacote['uso_memoria']}% | DISCO: {pacote['uso_disco']}%")
                
                # Insere no banco de dados
                inserir_dados(pacote)
                print()
                
            except json.JSONDecodeError as e:
                print(f"✗ Erro ao decodificar JSON: {e}")
            except Exception as e:
                print(f"✗ Erro ao processar pacote: {e}")
    
    except KeyboardInterrupt:
        print("\n\nServidor interrompido pelo usuário.")
    finally:
        sock.close()
        print("Servidor encerrado.")


if __name__ == "__main__":
    iniciar_servidor()
