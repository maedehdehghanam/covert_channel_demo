#!/usr/bin/env python3

import base64
import re
import time

log_file = "/var/log/named/query.log"
site_url = "example.com"

# 09-Apr-2024 21:54:44.893 client @0x748f2f265168 127.0.0.1#55082 (!.example.com): query: !.example.com IN TXT + (127.0.0.1)
extract_pattern = r"query:\s+(.+)\." + re.escape(site_url)


def receive_data():
    last_position = 0
    received_data = ""

    while True:
        with open(log_file, "r", encoding="UTF-8") as file:
            content = file.read()

            # ignore already read lines
            content = content[last_position:]
            last_position += len(content)

        for log in content.splitlines():
            try:
                matches = re.findall(extract_pattern, log)
                if matches:
                    extracted_chars = str(matches[0])
                    decoded_chars = base64.b64decode(
                        extracted_chars.encode()).decode()
                    received_data += decoded_chars
            except ValueError as e:
                pass

        if received_data:
            print(f"Received data: {received_data}")
            received_data = ""
        time.sleep(1)


if __name__ == "__main__":
    receive_data()
