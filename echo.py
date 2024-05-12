import socket
import http


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8000)
server_socket.bind(server_address)
server_socket.listen(1)

print(f'Сервер запущен на {server_address[0]}:{server_address[1]}')

while True:
    print('Ожидание соединения...')
    connection, client_address = server_socket.accept()

    try:
        print(f'Соединение установлено с {client_address}')

        while True:
            data = connection.recv(1024)
            if not data:
                break

            request = data.decode()

            request_lines = request.split('\r\n')
            request_line = request_lines[0].split()
            method, path, protocol = request_line

            if '?' in path:
                path, query_string = path.split('?', 1)
                params = dict(param.split('=') for param in query_string.split('&'))
                try:
                    status_code = int(params.get('status', '200'))
                except ValueError:
                    status_code = 200
            else:
                status_code = 200

            headers = '\r\n'.join(request_lines[1:])
            response_headers = '\r\n'.join([
                f'Request Method: {method}',
                f'Request Source: {client_address}',
                f'Response Status: {status_code} {http.HTTPStatus(status_code).phrase}',
                headers
            ])
            response = (f'HTTP/1.1 {status_code} {http.HTTPStatus(status_code).phrase}\r\nContent-Length: '
                        f'{len(response_headers)}\r\n\r\n{response_headers}')

            connection.sendall(response.encode())

    finally:
        connection.close()
