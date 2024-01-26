# FastAPI Invoice Generator

This is a simple web application built with FastAPI to generate invoices based on a CSV timesheet. The application allows users to upload a CSV file with a timesheet in a specific format, and it automatically calculates and displays invoices for each company involved in the projects.

## Features

- **CSV Timesheet Input:** Users can upload a CSV file containing the timesheet data for various projects.

- **Automatic Invoice Generation:** The application automatically processes the uploaded timesheet and generates invoices for each company involved.

- **Web Interface:** A user-friendly web interface allows users to interact with the application.

## Requirements

- Python 3.12+
- FastAPI
- Uvicorn
- CSV file with a specific format (as described below)

## CSV Timesheet Format

The CSV file should have the following columns:

- Employee ID
- Billable Rate (per hour)
- Project
- Date
- Start Time
- End Time

Example:

```csv
Employee ID, Billable Rate (per hour), Project, Date, Start Time, End Time
1, 300, Google, 2019-07-01, 09:00, 17:00
2, 100, Facebook, 2019-07-01, 11:00, 16:00
```

## Usage

### Without Docker

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:

    ```bash
    uvicorn main:app --reload
    ```

3. Open your web browser and visit <http://127.0.0.1:8000>.

4. Upload the CSV file using the provided form.

5. The application will automatically generate invoices for each company involved in the projects.

6. The application will generate invoices for each company based on the uploaded timesheet.

### With Docker

1. Run the application:

    ```bash
    docker compose up -d
    ```

2. Open your web browser and visit <http://127.0.0.1:80>.

3. Upload the CSV file using the provided form.

4. The application will automatically generate invoices for each company involved in the projects.

## Testing

To run the tests, use the following command:

```bash
pytest
```

## License

This project is licensed under the terms of the [MIT license](/LICENSE).

## Contact

If you want to contact me you can reach me at <a href="mailto:djangbahevans@yahoo.com">djangbahevans@yahoo.com</a>.
