#!/usr/bin/env python3
"""
Interface Web para visualização dos dados de monitoramento
"""

from flask import Flask, render_template, jsonify, send_from_directory
import mysql.connector
from mysql.connector import Error
from config import WEB_PORT, DEBUG, DB_CONFIG
from datetime import datetime
import os

app = Flask(__name__)


def conectar_bd():
    """Cria conexão com o banco de dados"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    """Serve arquivos estáticos"""
    return send_from_directory('static', path)


@app.route('/api/dados')
def obter_dados():
    """API: Retorna os últimos 50 registros"""
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'erro': 'Erro de conexão com BD'}), 500
    
    try:
        cursor = conexao.cursor(dictionary=True)
        query = """
        SELECT id, ip_origem, ip_destino, uso_memoria, uso_cpu, 
               uso_disco, processos, tempo
        FROM monitoring_data
        ORDER BY tempo DESC
        LIMIT 50
        """
        cursor.execute(query)
        registros = cursor.fetchall()
        
        # Converte datetime para string
        for reg in registros:
            if isinstance(reg['tempo'], datetime):
                reg['tempo'] = reg['tempo'].strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.close()
        conexao.close()
        
        return jsonify(registros)
    except Error as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/estatisticas')
def obter_estatisticas():
    """API: Retorna estatísticas gerais"""
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'erro': 'Erro de conexão com BD'}), 500
    
    try:
        cursor = conexao.cursor(dictionary=True)
        query = """
        SELECT 
            COUNT(*) as total_registros,
            ROUND(AVG(uso_memoria), 2) as media_memoria,
            ROUND(AVG(uso_cpu), 2) as media_cpu,
            ROUND(AVG(uso_disco), 2) as media_disco,
            ROUND(MAX(uso_memoria), 2) as max_memoria,
            ROUND(MAX(uso_cpu), 2) as max_cpu,
            ROUND(MAX(uso_disco), 2) as max_disco,
            MIN(tempo) as primeiro_registro,
            MAX(tempo) as ultimo_registro
        FROM monitoring_data
        """
        cursor.execute(query)
        stats = cursor.fetchone()
        
        # Converte datetime para string
        if stats['primeiro_registro']:
            stats['primeiro_registro'] = stats['primeiro_registro'].strftime('%Y-%m-%d %H:%M:%S')
        if stats['ultimo_registro']:
            stats['ultimo_registro'] = stats['ultimo_registro'].strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.close()
        conexao.close()
        
        return jsonify(stats)
    except Error as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/grafico')
def dados_grafico():
    """API: Retorna dados para o gráfico (últimos 5 minutos)"""
    conexao = conectar_bd()
    if not conexao:
        return jsonify({'erro': 'Erro de conexão com BD'}), 500
    
    try:
        cursor = conexao.cursor(dictionary=True)
        query = """
        SELECT uso_memoria, uso_cpu, uso_disco, tempo
        FROM monitoring_data
        WHERE tempo >= DATE_SUB(NOW(), INTERVAL 5 MINUTE)
        ORDER BY tempo ASC
        """
        cursor.execute(query)
        registros = cursor.fetchall()
        
        # Formata tempo
        for reg in registros:
            if isinstance(reg['tempo'], datetime):
                reg['tempo'] = reg['tempo'].strftime('%H:%M:%S')
        
        cursor.close()
        conexao.close()
        
        return jsonify(registros)
    except Error as e:
        return jsonify({'erro': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("INTERFACE WEB DE MONITORAMENTO")
    print("=" * 60)
    print(f"Acesse: http://localhost:{WEB_PORT}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=WEB_PORT, debug=DEBUG)