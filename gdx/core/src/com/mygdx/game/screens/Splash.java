package com.mygdx.game.screens;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.scenes.scene2d.Actor;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.actions.Actions;
import com.badlogic.gdx.scenes.scene2d.ui.Image;
import com.mygdx.game.AndroidCamera;
import com.mygdx.game.MyGdxGame;


public class Splash implements Screen {
    private Texture texture = new Texture(Gdx.files.internal("data/logosnn.png"));
    private Image splash_image = new Image(texture);
    private Stage stage = new Stage();

    @Override
    public void render(float delta) {
        Gdx.gl.glClearColor(0,0,0,1); //sets clear color to black
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT); //clear the batch
        stage.act(); //update all actors
        stage.draw(); //draw all actors on the Stage.getBatch()
    }

    @Override
    public void resize(int width, int height) {

    }

    @Override
    public void show() {
        stage.addActor(splash_image); //adds the image as an actor to the stage
//        splash_image.addAction(Actions.sequence(Actions.alpha(0), Actions.fadeIn(0.5f), Actions.delay(2), Actions.run(new Runnable() {
        splash_image.addAction(Actions.sequence(
                Actions.fadeOut(0.5f),
                Actions.delay(1),
                Actions.run(new Runnable() {
                    @Override
                    public void run() {
                        ((MyGdxGame)Gdx.app.getApplicationListener()).setScreen(new MainMenu());
                    }
                })));

    }

    @Override
    public void hide() {
        dispose();
    }

    @Override
    public void pause() {
        System.out.print("I've paused.");
    }

    @Override
    public void resume() {
    }

    @Override
    public void dispose() {
        texture.dispose();
        stage.dispose();
    }

}