from server import HTTPServer

def main():
    port = 4321
    root_dir = './public' # be careful of the relative path, since it depends on this file's execution path
    http_server = HTTPServer(port, root_dir)
    http_server.start()

if __name__ == "__main__":
        main()