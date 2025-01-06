# mivaa-las-to-json-convertor

This application scans LAS files in a specified directory and processes them into a JSON Well Log Format using Docker for easy deployment.

## Prerequisites

1. **Download the Repository**:
   - [Clone](https://github.com/MIVAA-ai/mivaa-las-to-json-convertor.git) or download the repository as a [ZIP](https://github.com/MIVAA-ai/mivaa-las-to-json-convertor/archive/refs/heads/main.zip) file.

2. **Unzip the Repository**:
   - Extract the downloaded ZIP file to a folder on your system.

3. **Install Docker**:
   - Ensure Docker is installed and running on your machine. You can download Docker [here](https://www.docker.com/).

## Steps to Run the Application Using the Startup Script

### 1. Execute the Script
- Open a terminal or command prompt, navigate to the directory where the script is saved (in this case it will be github repo directory), and run it with the base directory as an argument.

#### For Windows:
1. Open Command Prompt.
2. Run the command:
   ```cmd
   startup-windows.bat "F:/logs-scanner-directory"
   ```
   Replace `F:/logs-scanner-directory` with your desired base directory.

#### For Linux:
1. Open a terminal.
2. Make the script executable (only needed the first time):
   ```bash
   chmod +x startup-linux.sh
   ```
3. Run the command:
   ```bash
   ./startup-linux.sh /path/to/logs-scanner-directory
   ```
   Replace `/path/to/logs-scanner-directory` with your desired base directory.

### 2. What the Script Does
- Automatically creates the necessary folders in the base directory.
- Updates the `.env` file with the correct paths.
- Starts the application using Docker Compose.

### 3. Access the Logs and Processed Data

- **Uploads Directory**:
  Place your LAS files in the directory specified in the `UPLOADS_VOLUME` path in your `.env` file.
- **Processed Directory**:
  The processed JSON files will be saved in the directory specified in the `PROCESSED_VOLUME` path.
- **Scanned Files Summary**:
  A summary of scanned files is saved in `worker/data/summary/scanned_file.csv`.
- **Processing Logs**:
  Detailed processing logs are saved in `worker/data/results`.
- **Converted Output**:
  Converted files in JSON Well Log Format are saved in the `processed` folder specified by `PROCESSED_VOLUME`.

## Testing Results

| Metric                    | Value                     |
|---------------------------|---------------------------|
| Number of LAS Files       | 400                       |
| Total Dataset Size        | 2 GB                      |
| Processing Time           | 50 minutes               |
| Success Rate             | 100%                      |

## Additional Resources

- **Blog**:
  Read the detailed blog post about this application: [https://deepdatawithmivaa.com/2025/01/06/upgrade-your-well-log-data-workflow-vol-1-from-las-2-0-to-json/]

- **JSON Well Log Format**:
  Details about JSON Well Log Format: [https://jsonwelllogformat.org/]

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
- Avoid opening the scanned_files.csv in the Excel application while the system updates the file. The application locks the file, which prevents the system from updating it with the latest information.
- This application is currently tested in the windows environment, incase you face any issues running it in Linux, feel free to reach out.

Feel free to raise any issues or suggestions for improvement! Reach out at [info@deepdatawithmivaa.com](mailto:info@deepdatawithmivaa.com) for more help, comments, or feedback.
