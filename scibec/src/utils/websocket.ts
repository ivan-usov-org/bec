import { ScibecApplication } from "../application";

export interface WebsocketClient {
    // eslint-disable-next-line  @typescript-eslint/no-explicit-any
    ws?: any;
    // eslint-disable-next-line  @typescript-eslint/no-explicit-any
    user?: any;
    // eslint-disable-next-line  @typescript-eslint/no-explicit-any
    config?: any;
}
export interface WebsocketContainer {
    [index: string]: WebsocketClient[];
}

export async function startWebsocket(app: ScibecApplication) {
    const WebSocket = require('ws');
    const websocketMap: WebsocketContainer = {};

    // console.log(app.restServer)
    const wss = new WebSocket.Server({ server: app.restServer.httpServer?.server });

    // console.log(app.restServer)
    // eslint-disable-next-line  @typescript-eslint/no-explicit-any
    wss.on('connection', function connection(ws: any) {
        // eslint-disable-next-line  @typescript-eslint/no-explicit-any
        ws.on('message', async (message: any) => {
            let msgContainer: any;
            try {
                msgContainer = JSON.parse(message);
            } catch (error) {
                console.log("Failed to parse websocket json message: " + message.toString())
                console.log(error.message)
                return;
            }

            // eslint-disable-next-line  no-prototype-builtins
            if (!msgContainer.hasOwnProperty('message')) {
                return;
            }

            // eslint-disable-next-line  no-prototype-builtins
            if (!msgContainer['message'].hasOwnProperty('join')) {
                return;
            }

            // eslint-disable-next-line  no-prototype-builtins
            if (!msgContainer['message'].hasOwnProperty('token')) {
                return;
            }

            const logbookID: string = msgContainer['message']['join'];
            // eslint-disable-next-line  @typescript-eslint/no-explicit-any
            const config: any = msgContainer['message']['config'];
            // eslint-disable-next-line  no-prototype-builtins
            if (websocketMap.hasOwnProperty(logbookID)) {
                websocketMap[logbookID].push({
                    ws: ws,
                    config: config,
                });
            } else {
                websocketMap[logbookID] = [
                    { ws: ws, config: config },
                ]; //push({ws: ws, user: userProfileFromToken});
            }
        });
    });
}
