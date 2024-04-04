# TODO: generate command with options
# consider other mythic components that would be better suited for building this 'payload'
# is there a way to use the builder flow instead of a command inside a callback


# Example code

# implant_config = client_pb2.ImplantConfig(
#     IsBeacon=True,
#     Name="sliver-pytest-1",
#     GOARCH="amd64",
#     GOOS="linux",
#     Format=client_pb2.OutputFormat.EXECUTABLE,
#     ObfuscateSymbols=False,
#     C2=[client_pb2.ImplantC2(Priority=0, URL="http://localhost:80")],
# )

# implant = await client.generate_implant(implant_config)