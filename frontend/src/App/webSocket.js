import { io } from 'socket.io-client';


const webSocket = {
	socket: io({
	  reconnection: false,
	  autoConnect: false
	}),
	connect() {
	  this.socket.connect(process.env.DOMAIN, {secure:true});
	},
	tryReconnect() {
		// const c = this.socket;
		setTimeout(() => {
			console.log('webSocket.tryReconnect');
			webSocket.socket.io.open((err) => {
				if (err) {
					console.log(`webSocket.tryReconnect err: ${err}`);
					webSocket.tryReconnect();
				}
			});
		}, 2000);
	}
};

webSocket.socket.io.on("close", webSocket.tryReconnect);

export default webSocket;
