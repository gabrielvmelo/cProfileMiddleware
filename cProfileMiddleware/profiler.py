import time
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send
import cProfile, pstats, io
from traceback import print_exc

class ProfilerMiddleware:
    def __init__(
        self, app: ASGIApp, 
        sort_by : str = 'cumulative',
        print_each_request : bool = False,
        filename : str = "/tmp/profile_output.stats",
        strip_dirs : bool = False,
        activate_EP : str = "/profilling/activate",
        deactivate_EP : str = "/profilling/deactivate",
        data_EP : str = "/profilling/data") -> None:
        
        self.app = app
        self._sort_by = sort_by
        self._print_each_request = print_each_request
        self._filename = filename
        self._strip_dirs = strip_dirs
        self._activate_EP = activate_EP
        self._deactivate_EP = deactivate_EP
        self._data_EP = data_EP
        self._profiler = cProfile.Profile()

    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive=receive)
        method = request.method
        path = request.url.path
        begin = time.perf_counter()
        status_code = 500

        if path == self._activate_EP:
            self._profiler.enable()
            print("Profilling STARTED")
        elif path == self._deactivate_EP:
            self._profiler.disable()
            print("Profilling STOPPED")
        elif path == self._data_EP:
            self._profiler.disable()
            s = io.StringIO()
            ps = pstats.Stats(self._profiler, stream=s).sort_stats(self._sort_by)
            if self._strip_dirs:
                ps.strip_dirs()
            ps.print_stats()
            with open(self._filename, "w") as arq:
                r = s.getvalue()
                arq.write(r)
            print("Profile Data SAVED")
            self._profiler.enable()
        
        async def wrapped_send(message: Message) -> None:
            if message['type'] == 'http.response.start':
                nonlocal status_code
                status_code = message['status']
            await send(message)

        try:
            await self.app(scope, receive, wrapped_send)
        except:
            print_exc()
        finally:
            end = time.perf_counter()
            print(f"Method: {method} ", f"Path: {path} ", f"Duration: {end - begin} ", f"Status: {status_code}")