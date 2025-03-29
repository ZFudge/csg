To build images, install static files, run the server, and start the backend, proxy, and frontend dev servers, run:
```
make all
```
Or separately:
```
make build
make install
make static
make run
```

proxy server: http://localhost
frontend dev server: http://localhost:3075

Verify the websockets are working:
```
curl "http://localhost/socket.io/?EIO=4&transport=polling"
```
Should get a response like this
```
0{"sid":"3ABCefghIJkLMnopAAAA","upgrades":["websocket"],"pingTimeout":20000,"pingInterval":25000}%
```

If the response doesn't include "upgrades":["websocket"] something is wrong.
