# Author: Mutalip

## Project Setup

Follow the steps below to set up and run the project locally.

### Prerequisites

Before starting, make sure the following tools are installed on your machine:

- Docker
- Docker Compose

Also ensure that the following ports are available and not used by other applications:

- `80`
- `5432`
- `8000`

### Environment Configuration

Copy the example environment file and create your local configuration:

```bash
cp config/env.example config/.env
