#!/usr/bin/env python3
"""
Módulo de gerenciamento do banco de dados
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def conectar_bd():
    """Cria e retorna uma conexão com o banco de dados"""
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        return conexao
    except Error as e:
        print(f"✗ Erro ao conectar ao MySQL: {e}")
        return None


def inserir_dados(pacote):
    """Insere os dados do pacote no banco de dados"""
    conexao = conectar_bd()
    
    if conexao is None:
        return False
    
    try:
        cursor = conexao.cursor()
        
        query = """
        INSERT INTO monitoring_data 
        (ip_origem, ip_destino, uso_memoria, uso_cpu, uso_disco, processos)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        valores = (
            pacote['ip_origem'],
            pacote['ip_destino'],
            pacote['uso_memoria'],
            pacote['uso_cpu'],
            pacote['uso_disco'],
            pacote['processos']
        )
        
        cursor.execute(query, valores)
        conexao.commit()
        
        print(f"✓ Dados inseridos no BD - ID: {cursor.lastrowid}")
        
        cursor.close()
        conexao.close()
        return True
        
    except Error as e:
        print(f"✗ Erro ao inserir dados: {e}")
        if conexao:
            conexao.close()
        return False


def obter_ultimos_registros(limite=50):
    """Obtém os últimos N registros do banco"""
    conexao = conectar_bd()
    
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        query = """
        SELECT id, ip_origem, ip_destino, uso_memoria, uso_cpu, uso_disco, 
               processos, tempo
        FROM monitoring_data
        ORDER BY tempo DESC
        LIMIT %s
        """
        
        cursor.execute(query, (limite,))
        registros = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        
        return registros
        
    except Error as e:
        print(f"✗ Erro ao obter registros: {e}")
        if conexao:
            conexao.close()
        return []


def obter_estatisticas():
    """Obtém estatísticas gerais do monitoramento"""
    conexao = conectar_bd()
    
    if conexao is None:
        return None
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        query = """
        SELECT 
            COUNT(*) as total_registros,
            AVG(uso_memoria) as media_memoria,
            AVG(uso_cpu) as media_cpu,
            AVG(uso_disco) as media_disco,
            MAX(uso_memoria) as max_memoria,
            MAX(uso_cpu) as max_cpu,
            MAX(uso_disco) as max_disco,
            MIN(tempo) as primeiro_registro,
            MAX(tempo) as ultimo_registro
        FROM monitoring_data
        """
        
        cursor.execute(query)
        stats = cursor.fetchone()
        
        cursor.close()
        conexao.close()
        
        return stats
        
    except Error as e:
        print(f"✗ Erro ao obter estatísticas: {e}")
        if conexao:
            conexao.close()
        return None
