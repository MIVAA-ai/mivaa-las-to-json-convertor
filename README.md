# Logs Scanner Application

This application scans LAS files in a specified directory and processes them into a standardized JSON format using Docker for easy deployment.

## Prerequisites

1. **Download the Repository**:
   - Clone or download the repository as a ZIP file.

2. **Unzip the Repository**:
   - Extract the downloaded ZIP file to a folder on your system.

3. **Install Docker**:
   - Ensure Docker is installed and running on your machine. You can download Docker [here](https://www.docker.com/).

## Steps to Run the Application

### 1. Update the `.env` File

Edit the `.env` file in the root of the repository and update it with the directories on your system. Ensure these directories exist on your machine before running the application:

```env
PROCESSED_VOLUME=F:/logs-scanner-directory/processed
UPLOADS_VOLUME=F:/logs-scanner-directory/uploads
LOGS_VOLUME=F:/logs-scanner-directory/logs
DATA_IN_VOLUME=F:/logs-scanner-directory/worker/data/in
DATA_RESULTS_VOLUME=F:/logs-scanner-directory/worker/data/results
```

- Replace `F:/logs-scanner-directory` with the desired base path on your system.

### 2. Start the Application

Run the following command to start the application:

```bash
docker-compose --env-file .env up
```

This command will:
- Build the necessary Docker images.
- Start the containers for the application.

### 3. Access the Logs and Processed Data

- **Uploads Directory**:
  Place your LAS files in the directory specified in the `UPLOADS_VOLUME` path in your `.env` file.
- **Processed Directory**:
  The processed JSON files will be saved in the directory specified in the `PROCESSED_VOLUME` path.

## Troubleshooting

- Ensure the directories specified in the `.env` file exist and are accessible by Docker.
- Check the Docker logs for errors:
  ```bash
  docker-compose logs
  ```
- If you need to rebuild the containers after making changes, use:
  ```bash
  docker-compose --env-file .env up --build
  ```

## Notes

- This application requires Docker Compose.
- Ensure your LAS files are properly formatted for successful processing.
