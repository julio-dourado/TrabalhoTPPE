set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "${POSTGRES_DB}_test";
EOSQL

echo "Banco de dados de teste '${POSTGRES_DB}_test' criado com sucesso."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "${POSTGRES_DB}_test" -f /docker-entrypoint-initdb.d/init.sql

echo "Schema inicial aplicado ao banco de dados de teste."