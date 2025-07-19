@echo off
cd /d "%~dp0"

if "%1"=="dev" goto dev
if "%1"=="test" goto test
if "%1"=="logs" goto logs
if "%1"=="down" goto down
if "%1"=="clean" goto clean
if "%1"=="help" goto help

:help
echo.
echo 🏋️‍♀️  Crie Seu Treino - Comandos Disponíveis:
echo.
echo 🚀 Desenvolvimento:
echo   run.bat dev         - Rodar toda a aplicação (backend + frontend + db)
echo   run.bat logs        - Ver logs de todos os serviços
echo   run.bat down        - Parar todos os serviços
echo   run.bat clean       - Limpar containers e volumes
echo.
echo 🧪 Testes:
echo   run.bat test        - Rodar todos os testes (45 testes)
echo.
echo 📱 Acesso:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Digite: run.bat help para ver esta mensagem novamente
echo.
goto end

:dev
echo 🚀 Iniciando desenvolvimento completo...
docker-compose up --build -d
echo.
echo ✅ Aplicação rodando!
echo 🎨 Frontend: http://localhost:3000
echo 🚀 Backend:  http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
goto end

:test
echo 🧪 Executando todos os testes...
docker-compose --profile testing run --rm test-all
goto end

:logs
echo 📊 Logs dos serviços:
docker-compose logs -f
goto end

:down
echo ⬇️  Parando serviços...
docker-compose down
goto end

:clean
echo 🧹 Limpando containers e volumes...
docker-compose down -v --remove-orphans
docker system prune -f
goto end

:end 