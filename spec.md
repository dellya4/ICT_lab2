# Service Specification — Lab 2

Author: Abdrakhmanova Adel
Version: 1

## 1. Purpose

The purpose of this service is to demonstrate a simple REST API implemented in Python using Flask.

The service can return an echo message, show the current server time, accept asynchronous jobs, and return the status and result of a job.

## 2. Endpoints

| ID | Method | Path | Input | Output | Response Codes |
|---|---|---|---|---|---|
| R1 | POST | /echo | `{"message": "string"}` | `{"reply": "string"}` | 200, 400 |
| R2 | GET | /time | none | `{"time": "string"}` | 200 |
| R3 | POST | /jobs | `{"message": "string"}` | `{"job_id": "UUID", "status": "queued"}` | 202, 400 |
| R4 | GET | /jobs/<job_id> | job ID in URL | status and optional result | 200, 404 |

### R1 — Echo

The client sends a JSON object containing a `message` field.

Example input:

`{"message": "hello"}`

Example output:

`{"reply": "hello"}`

If the `message` field is missing or is not a string, the server returns HTTP 400.

### R2 — Current time

Returns the current server date and time.

Example output:

`{"time": "2026-10-12T17:30:00"}`

### R3 — Submit job

The client sends:

`{"message": "hello world"}`

The API generates a unique UUID and stores the job in the file-based queue.

Example response:

`{"job_id": "UUID", "status": "queued"}`

The response code is HTTP 202 Accepted.

### R4 — Job status

The client provides the job identifier in the URL.

If the job is still in the queue:

`{"job_id": "UUID", "status": "queued"}`

If processing is completed:

`{"job_id": "UUID", "status": "done", "result": "HELLO WORLD"}`

If the identifier is invalid or does not exist, HTTP 404 is returned.

## 3. Queue Message Format

The API writes each job into the `queue/` directory.

The message is stored as JSON:

`{"job_id": "UUID", "message": "string"}`

Field types:

- `job_id` — string containing a valid UUID.
- `message` — string containing the text to process.

The worker converts the message to uppercase.

The result is stored in:

`results/<job_id>.json`

## 4. Constraints

- The service uses HTTP.
- The data format is JSON.
- The server is implemented in Python 3 using Flask.
- The server runs on `127.0.0.1`.
- The server uses port `5000`.
- Variant C-2 is used: file-based queue.
- Jobs are stored in the `queue/` directory.
- Results are stored in the `results/` directory.
- Job identifiers must be valid UUID values.
- No AWS credentials or secrets are stored in the project.

## 5. Non-functional Requirements

- N1: `/echo` should respond within 200 ms under normal local execution.
- N2: `/time` should respond within 200 ms under normal local execution.
- N3: `/jobs` should accept a job and return HTTP 202 within 500 ms because job processing is performed asynchronously.
- N4: the worker should start processing an available job within approximately 1 second after detecting it.

## 6. Assumptions

- A1: the application has permission to create and modify files in the project directory.
- A2: the `queue/` and `results/` directories are accessible by both the API and worker.
- A3: the worker may be temporarily stopped; jobs must remain in the queue until it starts again.
- A4: the API and worker run on the same local computer.

If the worker is unavailable, jobs remain in the queue and continue to have the `queued` status until the worker becomes available again.