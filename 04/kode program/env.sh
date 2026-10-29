#!/usr/bin/env bash
# Shortcut untuk praktikum streaming replication.
# Ganti DIRECTORY dengan nama direktori tempat file-file ini disimpan.
# Container akan diberi nama <direktori>-postgres_primary-1 dan <direktori>-postgres_replica-1.
#
# Catatan: modul memakai "sudo docker-compose" (Compose v1 di Linux).
# Di Docker Desktop (Windows/macOS) gunakan "docker compose" tanpa sudo.
DIRECTORY="streaming-replication"

alias dcu="docker compose up -d"
alias dcd="docker compose down"
alias dps="docker ps"
alias der="docker exec -it ${DIRECTORY}-postgres_replica-1 bash"
alias dep="docker exec -it ${DIRECTORY}-postgres_primary-1 bash"
alias dlr="docker logs ${DIRECTORY}-postgres_replica-1"
alias dlp="docker logs ${DIRECTORY}-postgres_primary-1"
