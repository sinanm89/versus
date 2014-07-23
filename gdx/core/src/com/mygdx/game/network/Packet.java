package com.mygdx.game.network;

/**
 * Created by snn on 7/23/14.
 */
public class Packet {
    public static class ConnectRequest { String message;  }
    public static class ConnectResponse { String message; }
    public static class GreetingRequest { String message; }
    public static class GreetingResponse { String message; }
}
