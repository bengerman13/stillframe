# stillframe

Use video frames as images for live displays.


## proposed pipeline

1. discover media catalog
1. for each video file in the movie catalog, split the film into frames. 
   This will probably use ffmpeg
1. batch frames into _scenes_. Initially, these will be simple time blocks
   in the future, use image comparison to detect scene transition
1. attempt to detect people in scenes, reject scenes with them

## proposed usage
1. run a webserver that selects `scenes` at random
1. present the frames of the scene to connected viewers
1. allow api access to show the current and recent scenes
1. allow api access to add scenes to denylist

# proposed scene structure

```
${SCENE_ID}
├── metadata.yml
└── images
    ├── ${SCENE_ID}.${TIME}.${FRAME}.jpg
    ├── ${SCENE_ID}.${TIME}.${FRAME}.jpg
    └── ${SCENE_ID}.${TIME}.${FRAME}.jpg
```


