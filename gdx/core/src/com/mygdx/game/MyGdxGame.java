package com.mygdx.game;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.Table;
import com.mygdx.game.actors.MyActor;
import com.mygdx.game.screens.MainMenu;
import com.mygdx.game.screens.Splash;

public class MyGdxGame extends Game {
    public static final String TITLE="Versus";
    public static int WIDTH=480,HEIGHT=800; // used later to set window size
    private Stage stage;
    private Table table;

    @Override
    public void create () {
        setScreen(new Splash());
//        stage = new Stage();
//        table = new Table();

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
}

