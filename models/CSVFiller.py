import csv
import os


def fill_csv(csv_filename, data, host_id):

    if "apacheLog_statusCode404" in csv_filename or "apacheLog_clientConnect" in csv_filename:
        # Create and open csv file in write mode
        with open(csv_filename, 'w', newline='') as f:
            # Create a CSV writer object
            csv_writer = csv.writer(f)

            csv_writer.writerow(['Date', 'OCCURRENCE'])
            # Write the data in the CSV file
            for result in data[host_id]:
                row = [result[0], result[1]]
                csv_writer.writerow(row)

    elif "_apacheLog_requestUrl" in csv_filename:
        # Create and open csv file in write mode
        with open(csv_filename, 'w', newline='') as f:
            # Create a CSV writer object
            csv_writer = csv.writer(f)

            csv_writer.writerow(['URL', 'OCCURRENCE'])
            # Write the data in the CSV file
            for result in data[host_id]:
                row = [result[0], result[1]]
                csv_writer.writerow(row)

    elif "hardwareUsage" in csv_filename:
        # Create a csv file in write mode if not already exist
        if not os.path.exists(csv_filename):
            with open(csv_filename, 'w', newline='') as f:
                # Create a CSV writer object
                csv_writer = csv.writer(f)

                # Write header in the first line of the CSV file
                csv_writer.writerow(['Date', 'CPU_USAGE', 'MEM_USAGE', 'STO_USAGE'])

        # Open the csv file created before in add mode
        with open(csv_filename, 'a', newline='') as f:
            # Create a CSV writer object
            csv_writer = csv.writer(f)

            # Write the data in the CSV file
            csv_writer.writerow(data[host_id])
