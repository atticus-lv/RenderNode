### Resolution

This node can change the output resolution

### Frame Range

This node can change the output frame range.

You can use it for render animation. If not link to the task node, the task will inherit the context frame of the scene(only render one frame in render list)

### Image Format

Provide the 3 base format for output.

Also can handle the transparent of the image(Only for blender built-in engine), make sure select RGBA to save the alpha channel

### File Path

This node use $ to get the properties of the render task,then apply it to the output file name 

Usage(Also show in the side pannel):

```
$blend: name of your file (save first!)
$label: Task label
$camera: name of scene camera
$res: resolution (X x Y)
$engine: render engine
$vl: name of scene view layer
$date: month-day
$time: hour-min
/: create folder,should be dict_input folder name in front of "/"
```

### Render Slot

This node allow you to put the render result into different render slot of the image eidtor

### View Layer Passes

This node allow you to output different passes of a select viewlayer 

If it is not linked to the task, it will inherit the current compositor tree