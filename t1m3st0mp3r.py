import datetime
import argparse

# Define the argument parser
parser = argparse.ArgumentParser(description='Convert Windows FILETIME or Unix epoch timestamp to a human-readable datetime format.')

# Add a subparser for the two types of timestamps
subparsers = parser.add_subparsers(dest='command', required=True, help='Choose the type of timestamp to convert.')

# Subparser for FILETIME conversion
filetime_parser = subparsers.add_parser('filetime', help='Convert Windows FILETIME timestamp.')
filetime_parser.add_argument('--low', type=int, required=True, help='Low part of the original file last modification timestamp (e.g., -1354503710)')
filetime_parser.add_argument('--high', type=int, required=True, help='High part of the original file last modification timestamp (e.g., 31047188)')

# Subparser for Unix epoch conversion
unixepoch_parser = subparsers.add_parser('unixepoch', help='Convert Unix epoch timestamp.')
unixepoch_parser.add_argument('--timestamp', type=str, required=True, help='Unix epoch timestamp (e.g., "1682424941" or "1682424941.123456")')

# Parse the arguments
args = parser.parse_args()

if args.command == 'filetime':
   
    originalFileLastModifTimestamp = args.low
    originalFileLastModifTimestampHigh = args.high
    full_timestamp = (originalFileLastModifTimestampHigh << 32) | (originalFileLastModifTimestamp & 0xFFFFFFFF)

    # Convert the timestamp to seconds
    timestamp_seconds = full_timestamp / 10**7

    # Convert to a datetime object
    timestamp = datetime.datetime(1601, 1, 1) + datetime.timedelta(seconds=timestamp_seconds)

    print(f"The converted datetime from FILETIME is: {timestamp}")

elif args.command == 'unixepoch':
    # Provide the Unix epoch timestamp
    timestamp_str = args.timestamp

    try:
        # Convert the timestamp string to a float
        timestamp = float(timestamp_str)

        # Convert the timestamp to a datetime object
        utc_time = datetime.datetime.utcfromtimestamp(timestamp)

        # Format the UTC time
        formatted_time = utc_time.strftime("%d/%m/%y %H:%M:%S.%f")[:-3]
        print("Original UTC Time:", formatted_time)

        # Subtract 1 hour from the UTC time
        one_hour_less = utc_time - datetime.timedelta(hours=1)
        formatted_one_hour_less = one_hour_less.strftime("%d/%m/%y %H:%M:%S.%f")[:-3]
        print("One Hour Less UTC Time:", formatted_one_hour_less)
    except ValueError:
        print("Invalid timestamp provided. Please ensure it is a valid number.")
