# Face Recognition Example from Videos

This program allows you to detect the persons in the video you provide (*input.mp4*). But you need to have trained models for it. 

For training models I've used **[@ageitgey/face_recognition](https://github.com/ageitgey/face_recognition)** library. So, you need to install it first.


## Training

```bash
$ python .\train.py
```

You can start training process with the command above.
If there is a file called **"data.sav"** in the "**trained"** folder, **"Data Update"** process will start.


### In which cases "Data Update" process will start?
- Deleting the folder of a model.
- Deleting a few or the whole images in a specific model folder.
- Adding at least one new model folder.
- Adding at least one new image in a specific model folder.


## Detection

```bash
$ python .\detect.py
```

With the command above, the program will be executed with **"input.mp4"** file. At the end of the detection process, it will give you a video file called **"output.avi"** which has rectangles and corresponding labels on the faces. 

## Examples

![1](https://raw.githubusercontent.com/ilyasbilgihan/face-recognition-from-videos/main/examples/1.png)
![2](https://raw.githubusercontent.com/ilyasbilgihan/face-recognition-from-videos/main/examples/2.png)
![3](https://raw.githubusercontent.com/ilyasbilgihan/face-recognition-from-videos/main/examples/3.png)
![4](https://raw.githubusercontent.com/ilyasbilgihan/face-recognition-from-videos/main/examples/4.png)
![5](https://raw.githubusercontent.com/ilyasbilgihan/face-recognition-from-videos/main/examples/5.png)
![6](https://raw.githubusercontent.com/ilyasbilgihan/face-recognition-from-videos/main/examples/6.png)
