import sounddevice as sd
print("\nHost APIs:")
for i, api in enumerate(sd.query_hostapis()):
    print(f"[{i}] {api['name']}")
print("\nDevices:")
for i, d in enumerate(sd.query_devices()):
    print(f"[{i}] API: {d['hostapi']}, IN: {d['max_input_channels']}, OUT: {d['max_output_channels']}, {d['name']}")
