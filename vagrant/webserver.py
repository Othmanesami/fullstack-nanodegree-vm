from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer



class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>Hello!</body></html>'

                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith('/holla'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>&#161Holla <a href = "/hello">back to hello page</a></body></html>'

                self.wfile.write(output)
                print(output)
                return
            

        except IOError:

            self.send_error(404, 'file not found %s' % self.path)



def main():
    
    try:

        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print('web server is running in port %s' %port)

        server.serve_forever()


    except KeyboardInterrupt:

        print('^C entered stoping the server...')
        server.socket.close()




if __name__ == '__main__':
    main()
