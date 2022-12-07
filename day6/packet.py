import sys
from collections import Counter


def inspect_packets(signal: str, buffer_size: int = 4) -> int:
    signal_length = len(signal)
    marker = 0
    for i in range(signal_length - buffer_size):
        buffer = signal[i:i+buffer_size]
        cnt = Counter(buffer)
        all_different = all([v == 1 for v in cnt.values()])
        if all_different:
            marker = i + buffer_size
            break
    return marker



if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        content = f.read()

    packets = content.rstrip("\n").split("\n")
    packet_markers = [inspect_packets(p) for p in packets]
    print(f"Packet markers: {packet_markers}")

    msg_markers = [inspect_packets(p, buffer_size=14) for p in packets]
    print(f"Message markers: {msg_markers}")
