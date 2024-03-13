# Tokka WETH/ETH pricing

## Running Instructions

In order to execute the project, you will need docker installed:

```bash
docker compose build
docker compose up
```

### Tests

In order to run the tests, you can use poetry:

```bash
# First, make sure you're using python 3.11
python3 --version
# Install poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
# Run the tests
poetry run pytest .
```

## Services

### Web Server

Based on FastApi, contains three simple endpoints, which are described in the [openapi.json](openapi.json) file.

#### Get Transaction Fee

Given a hash, returns the transaction, together with the fee spent in USDT equivalent.

#### Post Importing Job

Given a range of blocks, returns the job ID.

#### Get Importing Job Status

Given the job ID obtained from the endpoint above, returns the status of the job and, if the latter is COMPLETED, all of the transactions and respective transaction fees in USDT.

- PENDING: Waiting to be picked up by a worker
- IN_PROGRESS: Importing the transactions
- COMPLETED: Finished successfully
- FAILED: Importing process ran into an issue. Waiting to be picked up by a worker

### Background Worker

Based on `Celery` running on top of `Redis`. The workers serve two separate purposes:

- Running batch importing jobs
- Creating new importing jobs in the background (based on crontab)

Batches requested by the user run directly, while batches created by the crontab run on the following order of priority:

1.  Failed
2.  In Progress for more than 1 hour (Considered stale)
3.  Pending

The number of workers is defined by the flag `-c 2` in the [docker compose file](docker-compose.yml)

### Database

Running a PostgreSQL database, in order to store all of the transactions and prices imported from the APIs.

The database includes two tables:

- **transaction**: Contains all imported transactions
- **importingjob**: Keeps track of all importing jobs

## APIs used

### Etherscan

Used for accessing the transactions on the given contract

### Binance

Used for accessing the ETH/USDT prices

### Infura

Used for fetching a transaction given its hash

## Bonuses

### Scalability

Since the amount of web and background workers can increase when needed, the solution is fully scalable. Once the transaction importing is up to date, the queries will be very fast, without any need for external API connections.

One possible issue is that the start time for importing all existing transactions might be slow, depending on the rate-limiting from the APIs used.

### Reliability

There is no floating point precision happening anywhere in the project. Therefore, the amounts calculated are as reliable as the data coming from the APIs.

### Availability

It is important to note that large batch queries might take a substantial amount of time, if the concerned transactions where not yet imported.

## Disclaimer

> The setup for docker to run FastAPI and Celery was largely based on a [template](https://github.com/tiangolo/full-stack-fastapi-postgresql)
> from FastAPI documentation
