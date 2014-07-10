package com.mygdx.game.actors;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.*;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.math.EarClippingTriangulator;
import com.badlogic.gdx.scenes.scene2d.Actor;
import com.mygdx.game.MyGdxGame;

import java.util.ArrayList;
import java.util.List;

public class MyActor extends Actor {
    Texture texture = new Texture(Gdx.files.internal("data/text.png"));
    private ShapeRenderer renderer;
    public float[] vertexes;
    PolygonSprite poly;
    PolygonSpriteBatch polyBatch;
    SpriteBatch sprite_batch;
    BitmapFont font;

    public MyActor () {
        int GAME_WIDTH = MyGdxGame.WIDTH; // width of screen
        int GAME_HEIGHT = MyGdxGame.HEIGHT; // height of screen
        int radius = 50;
        int number_of_vertices = 9;
        sprite_batch = new SpriteBatch();
        font = new BitmapFont();
        font.setColor(Color.WHITE);
        List<Float> vertice_list = new ArrayList<Float>();

        for (int vertice = 1; vertice < number_of_vertices + 1; vertice++) {

            int vertice_x_coordinate = radius + (int) Math.round((radius * Math.cos((2*Math.PI) * vertice / number_of_vertices)));
            int vertice_y_coordinate = radius + (int) Math.round((radius * Math.sin((2*Math.PI) * vertice / number_of_vertices)));
            vertice_list.add((float)vertice_x_coordinate);
            vertice_list.add((float)vertice_y_coordinate);
        }

        this.vertexes = new float[vertice_list.size()];

        for(int i=0; i < vertice_list.size(); i++) vertexes[i] = vertice_list.get(i);

        for (int j= 0; j<vertexes.length; j++) {
            System.out.print(vertexes[j]);

            if (j% 2 != 0) {
                System.out.print("\n");
            } else {
                System.out.print(" , ");
            }
        }
        short triangles[] = new EarClippingTriangulator().computeTriangles(vertexes).toArray();
//            for(int i=0; i < vertice_list.size(); i++) System.out.print(triangles[i] + "\n");
        PolygonRegion polyReg = new PolygonRegion(
                new TextureRegion(texture),
                vertexes,
                triangles
        );
        poly = new PolygonSprite(polyReg);
//            poly.setOrigin(w/2, h/2);
        polyBatch = new PolygonSpriteBatch();

        System.out.print(GAME_WIDTH);
        System.out.print("\n");
        System.out.print(GAME_HEIGHT);
        System.out.print("\n======\n");

    }


    @Override
    public void draw(Batch batch, float parentAlpha) {
        polyBatch.begin();
        poly.draw(polyBatch);
        polyBatch.end();
        sprite_batch.begin();
        font.draw(sprite_batch, ". COORDINATE HERE", vertexes[0], vertexes[1]);
        sprite_batch.end();
    }
}