import os
import struct
import time
import uuid


def uuid7() -> uuid.UUID:
    """
    Generates UUIDv7 according to RFC 9562.
    Structure: [unixts-48bits][rand-74bits] (with version/variant bits)
    """
    # Get current Unix time in milliseconds (48 bits)
    timestamp_ms = int(time.time() * 1000)
    
    # Generate 10 random bytes (80 bits total)
    rand_bytes = os.urandom(10)
    
    # Pack into UUID structure:
    # - First 6 bytes: timestamp (big-endian)
    # - Next 2 bytes: version/variant + random bits
    # - Last 8 bytes: random data
    uuid_bytes = (
        struct.pack(">Q", timestamp_ms)[2:]  # 48 bits timestamp (6 bytes)
        + bytes([rand_bytes[0] & 0x0F | 0x70])  # Version 7 (4 bits)
        + rand_bytes[1:2]  # More random bits
        + bytes([rand_bytes[2] & 0x3F | 0x80])  # Variant RFC 4122 (2 bits)
        + rand_bytes[3:]  # Remaining random bits (62 bits)
    )
    
    return uuid.UUID(bytes=uuid_bytes)
