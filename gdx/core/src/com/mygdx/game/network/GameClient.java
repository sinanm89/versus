package com.mygdx.game.network;


import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryonet.Client;
import com.esotericsoftware.kryonet.Connection;
import com.esotericsoftware.kryonet.Listener;
import com.esotericsoftware.minlog.Log;

import java.io.IOException;

public class GameClient {
//        public Client client;

    public GameClient() throws IOException {
        Client client = new Client(16384, 2048);
        register(client);

        NetworkListener listener1 = new NetworkListener();
        listener1.init(client);
        client.addListener(listener1);
        System.out.println("I will now try to connect");
        client.start();

//        new Thread(client).start();
        try {
            client.connect(5000, "192.168.1.100", 8123);
            System.out.println("Connected");
        } catch (IOException e) {
            e.printStackTrace();
            client.stop();
        }
        Packet.ConnectRequest request = new Packet.ConnectRequest();
        request.message = "Here is the request!";
        client.sendTCP(request);
    }


    private void register(Client client) {
        Kryo kryo = client.getKryo();
        kryo.register(Packet.ConnectRequest.class);
        kryo.register(Packet.ConnectResponse.class);
//        kryo.register(Packet.GreetingRequest.class);
//        kryo.register(Packet.GreetingResponse.class);
    }

}