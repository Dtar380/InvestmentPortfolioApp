# Deployment

This document describes how to deploy the InvestmentPortfolioAPP using the provided Dockerfiles, Docker Compose configurations, and the `deployment` helper files. It covers local development, production compose usage, environment variables, database migrations, TLS, CI/CD notes, and troubleshooting tips.

**Prerequisites**
- Docker and Docker Compose installed on the host
- Access to environment variables / secrets for production (see `.env.prod`)
- A domain name and DNS configured for production (for TLS)

**Files in this folder**
- **.env.dev**: environment variables for local development
- **.env.prod**: environment variables for production
- **docker-compose.dev.yml**: compose config for local development
- **docker-compose.prod.yml**: compose config for production
- **nginx.conf**: example Nginx reverse-proxy config used by the frontend/production setup
- **docker/**: Dockerfiles for backend and frontend (dev & prod)

Quick links:
- Compose dev: `docker-compose -f deployment/docker-compose.dev.yml`
- Compose prod: `docker-compose -f deployment/docker-compose.prod.yml`

## Local development (fast)
1. Copy or review `.env.dev` and set any local overrides.

2. Build and deploy using the repository helper scripts (recommended):

```bash
bash ./scripts/build.sh dev
bash ./scripts/deploy.sh dev
```

3. To stop services (advanced):

```bash
docker-compose -f deployment/docker-compose.dev.yml down
```

Notes:
- The development compose files are configured for iterative development and may mount local source volumes. Containers will reflect local code changes.

## Production (simple docker-compose)
1. Copy `.env.prod` to the server and ensure file permissions restrict access.
2. Build and deploy using the repository helper scripts (recommended):

```bash
bash ./scripts/build.sh prod
bash ./scripts/deploy.sh prod
```

3. To view logs or perform advanced maintenance, you can use Docker Compose directly:

```bash
docker-compose -f deployment/docker-compose.prod.yml logs -f
docker-compose -f deployment/docker-compose.prod.yml pull
docker-compose -f deployment/docker-compose.prod.yml up -d --remove-orphans
```

4. To stop and remove containers (advanced):

```bash
docker-compose -f deployment/docker-compose.prod.yml down
```

## Database migrations
This project includes Alembic configuration in the backend. To run migrations against the running backend container (example):

```bash
docker-compose -f deployment/docker-compose.prod.yml exec backend alembic upgrade head
```

Adjust the service name if your compose file uses a different name (e.g., `api` or `web`). If you run migrations from the host, ensure the same Python/DB dependencies and env variables are present.

## Nginx / TLS
- `nginx.conf` contains an example reverse-proxy for the frontend and API. Use it as a starting point for your production Nginx config.
- For TLS on a Linux host, a common approach is to use Certbot + the Nginx plugin to obtain certificates and automatically update `nginx.conf` to use them.
- Example Certbot flow (on the host, not in compose):

```bash
sudo certbot --nginx -d your.domain.example
```

Alternatively, terminate TLS at a cloud load balancer or a reverse-proxy container (see the `nginx.conf` example).

## Environment variables & secrets
- Store production secrets outside of version control. Use `.env.prod` only on the production host with restricted permissions.
- Examples of values to include: database URL, secret keys, OAuth credentials, API keys, and any service-specific settings. Do not commit these files.

## CI/CD recommendations
- Build and push images to a container registry (Docker Hub, GitHub Container Registry, ECR, etc.) from CI.
- Tag releases semantically (e.g., `v1.2.3`) and reference those tags in `docker-compose.prod.yml` to enable safe rollbacks.
- Example deploy flow in CI:
	1. Run tests and linters.
	2. Build images and push to registry.
	3. On successful push, SSH to production host and run `docker-compose -f deployment/docker-compose.prod.yml pull && docker-compose -f deployment/docker-compose.prod.yml up -d`.

## Rollbacks
- If using tagged images, rollback by changing the image tag in `docker-compose.prod.yml` to the previous stable tag and running `docker-compose up -d`.

## Backups & maintenance
- Back up any persistent databases or storage according to the database's recommended tooling (e.g., `pg_dump` for Postgres).
- Verify backups regularly and test restores in a staging environment.

## Troubleshooting
- If containers fail to start, inspect logs: `docker-compose -f deployment/docker-compose.prod.yml logs <service>`.
- Check environment variables are present and correctly formatted.
- Ensure the host firewall permits required ports (HTTP/HTTPS, or any custom ports).

## Security notes
- Keep Docker, the OS, and base images updated. Rebuild images periodically to pickup base-image security fixes.
- Do not expose admin or database ports publicly. Use private networking or firewall rules.

## Next steps / Tailoring for your infrastructure
- Consider replacing the simple docker-compose production deploy with a container orchestrator (Docker Swarm, Kubernetes, Nomad) for scaling, health checks, and zero-downtime deployments.
- Integrate secret management (Vault, cloud secrets manager) for production-grade secret handling.

If you want, I can also:
- Add example GitHub Actions CI/CD workflow for building and pushing images.
- Add a `deploy.sh` helper that performs a safe remote deploy via SSH.
