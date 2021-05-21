"""
Module with backend processing logic
"""

import hashlib
import hmac
import math
import time


def generate_time_based_one_time_password(secret: str) -> str:
    """
    Implementation of time based one time password, based on
    https://hackernoon.com/
    implementing-2fa-how-time-based-one-time-password-actually-works-with-python-examples-cm1m3ywt

    Args:
        secret (str): secret to be used to generate password

    Returns:
        str: time based one time password
    """

    time_since_epoch_in_seconds = math.floor(time.time())
    grace_period_in_seconds = 30

    message_to_hash = math.floor(time_since_epoch_in_seconds / grace_period_in_seconds)

    hashed_message = hmac.new(
        key=bytes(secret, encoding="utf-8"),
        msg=message_to_hash.to_bytes(length=8, byteorder="big"),
        digestmod=hashlib.sha256
    )

    return get_truncated_hashed_message(message=hashed_message, target_length=6)


def get_truncated_hashed_message(message: hmac.HMAC, target_length: int) -> str:
    """
    Gived hased message, generate its truncated version

    Args:
        message (hmac.HMAC): message to truncate
        target_length (int): target message length

    Returns:
        str: truncated message
    """

    bitstring = bin(int(message.hexdigest(), base=16))

    last_four_bits = bitstring[-4:]

    offset = int(last_four_bits, base=2)

    chosen_32_bits = bitstring[offset * 8: offset * 8 + 32]

    text_message = str(int(chosen_32_bits, base=2))

    return text_message[-target_length:]
