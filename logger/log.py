import logging

# Get a logger for the current module
log = logging.getLogger("AWS_ROLE_GRANTS")

# Set the log level to DEBUG
log.setLevel(logging.INFO)

# Create a handler (e.g., StreamHandler to print logs to console)
console_handler = logging.StreamHandler()

# Optionally, set a formatter to include additional info in the logs (timestamp, log level, etc.)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
log.addHandler(console_handler)
