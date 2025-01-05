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
        self.canvas = tkinter.Canvas(self.window)
        self.canvas.pack(fill = tkinter.BOTH, expand=True)      # Dynamic packing to resize with window
        self.scroll = 0
        self.width = WIDTH  # Default
        self.height = HEIGHT   #Default
        self.window.bind("<Down>", self.scrolldown)     # Keybind to scroll down
        self.window.bind("<Up>", self.scrollup)         # Keybind to scroll up
        self.window.bind("<Configure>", self.resize)    # Adds resize binding

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()
    def scrollup(self, e):
        self.scroll -= SCROLL_STEP
        self.draw()

    def draw(self):
        self.canvas.delete("all") 
        for x, y, c in self.display_list:
            if self.scroll <= y < self.scroll + self.height:
                self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
        body = url.request()
        text = lex(body)
        self.text = text    # Stores text for resizing
        self.display_list = layout(text, self.width)
        self.draw()

    def resize(self, event):
        # Handles window resize events
        self.width = event.width    # Capture new width
        self.height = event.height  # Capture new height
        self.display_list = layout(self.text, self.width)   # Recalculate layout
        self.draw()     # Redraw the content
        
def layout(text, width):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    max_line_width = width - HSTEP  # Calculate layout based on current width

    words = text.split()  # Split text into words
    for word in words:
        word_width = len(word) * HSTEP  # Approximate width of the word
        if cursor_x + word_width > max_line_width:  # Wrap to next line if it doesn't fit
            cursor_y += VSTEP
            cursor_x = HSTEP
        for c in word:  # Add each character to the display list
            display_list.append((cursor_x, cursor_y, c))
            cursor_x += HSTEP
        cursor_x += HSTEP  # Add space after each word

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
