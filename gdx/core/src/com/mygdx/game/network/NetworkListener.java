package com.mygdx.game.network;

import com.esotericsoftware.kryonet.Client;
import com.esotericsoftware.kryonet.Connection;
import com.esotericsoftware.kryonet.Listener;
import com.esotericsoftware.minlog.Log;

public class NetworkListener extends Listener {
    private Client client;

    public void init(Client client) {
        this.client = client;
    }

    public void connected(Connection arg0) {
        System.out.println("- someone has connected");
    }

    public void disconnected(Connection arg0) {
        System.out.println("- someone has disconnected");
    }

    public void received(Connection conn, Object obj) {
        if (obj instanceof Packet.ConnectRequest) {
            System.out.println("- Packed Received");
        }
    }
//        client.addListener(new Listener() {
//            public void received (Connection connection, Object object) {
//                if (object instanceof SomeResponse) {
//                    System.out.println("inside the received");
//                    SomeResponse response = (SomeResponse)object;
//                    System.out.println(response.text);
//                }
//            }
//        });

}
