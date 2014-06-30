package com.mygdx.game;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.mygdx.game.actors.MyActor;
import com.mygdx.game.screens.Splash;

public class MyGdxGame extends Game {
    public static final String TITLE="Versus";
    public static final int WIDTH=480,HEIGHT=800; // used later to set window size

    @Override
    public void create () {
        setScreen(new Splash());
//  PRE TUTORIAL
//        stage = new Stage();
//        MyActor aktor = new MyActor();
//        stage.addActor(aktor);
//        renderer = new ShapeRenderer();

    }

//  PRE TUTORIAL
//    private Stage stage;
//    ShapeRenderer renderer;

// PRE TUTORIAL
//    public class AndroidCamera extends OrthographicCamera{
//
//        public AndroidCamera(int width, int height){
//            super(width, height);
//            this.position.x=width/2;
//            this.position.y=height/2;
//        }
//    }

//  PRE TUTORIAL
//    @Override
//    public void resize (int width, int height) {
//        // See below for what true means.
//        stage.getViewport().update(MyGdxGame.WIDTH, MyGdxGame.HEIGHT, true);
//        stage.getViewport().setCamera(new AndroidCamera(480, 800));
//
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
}