#import socket

#class URL:
#    def __init__(self, url):
        #Dk what this does, gotta google
#        self.scheme, url = url.split(".//", 1)
#        assert self.scheme == "http"

#class URL:
#    def __init__(self, url):
        # ...
#        if "/" not in url:
#            url = url + "/"
#        self.host, url = url.split("/", 1)
#        self.path = "/" + url


#class URL:
#    def request(self):
#        s = socket.socket(
#            family=socket.AF_INET,
#            type=socket.SOCK_STREAM,
#            proto=socket.IPPROTO_TCP,
#        )

import socket
import ssl
import tkinter


window = tkinter.Tk()
tkinter.mainloop()

WIDTH, HEIGHT = 800, 600

class Browser:
    def _init_(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        

    def load(self, url):
        body = url.request()
        text = lex(body)
        self.canvas.create_rectangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text="Hi")

        HSTEP, VSTEP = 13, 18
        cursor_x, cursor_y = HSTEP, VSTEP
        for c in text:
            self.canvas.create_text(cursor_x, cursor_y, text=c)
            cursor_x += HSTEP

            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP

class URL:
    def _init_(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]
        if "/" not in url:
            url += "/"
        self.host, path = url.split("/", 1)
        self.path = "/" + path
        self.port = 443 if self.scheme == "https" else 80
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host}\r\n\r\n"
        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            headers[header.casefold()] = value.strip()
        
        assert "transfer-encoding" not in headers
        assert "content-encoding" not in headers

        content = response.read()
        s.close()
        return content

def lex(body):
    text = ""
    in_tag = False

    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c
    return text    




if _name_ == "_main_":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()

#python pathto/telnet.py http://example.org/