./deployment/scripts/wait-for-it.sh ${HOST}:5432 -- ./deployment/scripts/uvicorn.sh