package com.mygdx.game;

import com.badlogic.gdx.graphics.OrthographicCamera;

public class AndroidCamera extends OrthographicCamera {

    public AndroidCamera(int width, int height){
        super(width, height);
        this.position.x=width/2;
        this.position.y=height/2;
    }
}