#!/usr/bin/env python3
"""
Script principal para executar testes Selenium do frontend
"""

import subprocess
import sys
import time
import os
from pathlib import Path


def main():
    """Executar testes com configurações otimizadas"""
    
    # Configurar diretório de trabalho
    os.chdir(Path(__file__).parent)
    
    # Argumentos do pytest
    pytest_args = [
        "python", "-m", "pytest",
        "-v",  # Verbose
        "--tb=short",  # Traceback curto
        "--html=reports/report.html",  # Relatório HTML
        "--self-contained-html",  # HTML self-contained
        "--maxfail=5",  # Parar após 5 falhas
        "--durations=10",  # Mostrar 10 testes mais lentos
    ]
    
    # Adicionar argumentos da linha de comando
    if len(sys.argv) > 1:
        pytest_args.extend(sys.argv[1:])
    else:
        # Executar todos os testes por padrão
        pytest_args.append("tests/")
    
    # Criar diretório de relatórios
    os.makedirs("reports", exist_ok=True)
    
    print("🚀 Iniciando testes de frontend com Selenium...")
    print(f"📂 Diretório: {os.getcwd()}")
    print(f"🔧 Comando: {' '.join(pytest_args)}")
    print("-" * 60)
    
    # Executar testes
    start_time = time.time()
    result = subprocess.run(pytest_args)
    end_time = time.time()
    
    # Mostrar resultado
    duration = end_time - start_time
    print("-" * 60)
    print(f"⏱️  Tempo total: {duration:.2f}s")
    
    if result.returncode == 0:
        print("✅ Todos os testes passaram!")
    else:
        print("❌ Alguns testes falharam!")
        print(f"📊 Código de saída: {result.returncode}")
    
    print("📋 Relatório HTML: reports/report.html")
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main()) 