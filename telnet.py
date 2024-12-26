#import socket

#class URL:
#    def init(self, url):
        #Dk what this does, gotta google
#        self.scheme, url = url.split(".//", 1)
#        assert self.scheme == "http"

#class URL:
#    def init(self, url):
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

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def draw(self):
        self.canvas.delete("all") 
        for x, y, c in self.display_list:
            if self.scroll <= y < self.scroll + HEIGHT:
                self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
        body = url.request()
        text = lex(body)
        self.display_list = layout(text)
        self.draw()

def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
#NEWNEWNEWNEWNEW
        if c == "\n":  # Handle newlines
            cursor_y += VSTEP
            cursor_x = HSTEP
        elif cursor_x + HSTEP >= WIDTH:  # Handle word wrapping
            cursor_y += VSTEP
            cursor_x = HSTEP
#NEWNEWNEWNEWNEW
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
    return display_list

class URL:
    def __init__(self, url):
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

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <URL>")
    else:
        Browser().load(URL(sys.argv[1]))
        tkinter.mainloop()


#python pathto/telnet.py http://example.org/
