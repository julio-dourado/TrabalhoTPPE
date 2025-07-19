@echo off
echo 🧪 Executando Testes de Frontend com Selenium...
echo.

REM Executar testes frontend E2E
docker-compose --profile testing up --build frontend-test

REM Executar testes completos E2E
docker-compose --profile testing up --build test-e2e

echo.
echo ✅ Testes finalizados!
echo 📋 Relatórios em: frontend-tests/reports/
pause 