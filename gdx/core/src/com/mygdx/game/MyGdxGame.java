package com.mygdx.game;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Net;
import com.badlogic.gdx.net.ServerSocket;
import com.badlogic.gdx.net.ServerSocketHints;
import com.badlogic.gdx.net.Socket;
import com.badlogic.gdx.net.SocketHints;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.Table;
import com.mygdx.game.network.GameClient;
import com.mygdx.game.screens.Splash;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class MyGdxGame extends Game {
    public static final String TITLE = "Versus";
    public static int WIDTH = 480, HEIGHT = 800; // used later to set window size
    private Stage stage;
    private Table table;


    @Override
    public void create() {
        setScreen(new Splash());
//        stage = new Stage();
//        table = new Table();
        new Thread(new Runnable() {
            @Override
            public void run() {
//                try {
//                    new GameClient();
//                } catch (IOException e) {
//                    e.printStackTrace();
//                }

                SocketHints socketHints = new SocketHints();
                // Socket will time our in 4 seconds
                socketHints.connectTimeout = 4000;
                //create the socket and connect to the server entered in the text box ( x.x.x.x format ) on port 9021
                Socket socket = Gdx.net.newClientSocket(Net.Protocol.TCP, "127.0.0.1", 8123, socketHints);
                try {
                    // write our entered message to the stream
                    socket.getOutputStream().write("sinan".getBytes());
                } catch (IOException e) {
                    e.printStackTrace();
                }

                BufferedReader buffer = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                while(true){
                    try {
                        // Read to the next newline (\n) and display that text on labelMessage
//                    labelMessage.setText(buffer.readLine());
                        if (buffer.readLine() != null){
                            System.out.println(buffer.readLine());
                        }
                    } catch (IOException e) {
                        System.out.println("didnt get one");
                        e.printStackTrace();
                    }
                }


            }
        }).start();

    }
}


// PRE TUTORIAL
//    public class AndroidCamera extends OrthographicCamera{
//
//        public AndroidCamera(int width, int height){
//            super(width, height);
//            this.position.x=width/2;
//            this.position.y=height/2;
//        }
//    }
//
//    @Override
//    public void resize (int width, int height) {
//        // See below for what true means.
//        set_height(Gdx.graphics.getHeight());
//        set_width(Gdx.graphics.getWidth());
//    }
//
//    public void set_width(int current_width) {
//        this.WIDTH = current_width;
//    }
//
//    public void set_height(int current_height) {
//        this.HEIGHT = current_height;
//    }
//  PRE TUTORIAL
//    @Override
//    public void render () {
//        stage.draw();
//        Gdx.graphics.getGL20().glClearColor(12, 12, 0, 12);
//        renderer.setColor(Color.GREEN);
//        renderer.begin(ShapeRenderer.ShapeType.Filled);
//        renderer.circle(200, 300, 50 / 8);
//
//        renderer.end();
//    }
//
//  PRE TUTORIAL
//    @Override
//    public void dispose() {
//        stage.dispose();
//    }


