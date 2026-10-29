DIRECTORY="streaming-replication"

alias dcu="docker compose up -d"
alias dcd="docker compose down"
alias dps="docker ps"
alias der="docker exec -it ${DIRECTORY}-postgres_replica-1 bash"
alias dep="docker exec -it ${DIRECTORY}-postgres_primary-1 bash"
alias dlr="docker logs ${DIRECTORY}-postgres_replica-1"
alias dlp="docker logs ${DIRECTORY}-postgres_primary-1"
