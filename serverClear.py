import socket
import asyncio

async def handle_client(reader, writer):
	#print(reader, writer)
	while 1:
		data = (await reader.read(1024)).decode('utf8')

		print(data)
		response = data
		writer.write(response.encode('utf8'))
		await writer.drain()

	writer.close()


async def run_server():
	server = await asyncio.start_server(handle_client, '127.0.0.1', 15557)
	async with server:
		await server.serve_forever()

asyncio.run(run_server())
