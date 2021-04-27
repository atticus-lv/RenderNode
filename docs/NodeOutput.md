<!-- panels:start -->

<!-- div:title-panel -->

### Resolution

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> This node can change the output resolution

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Frame Range

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> 
> This node can change the output frame range.<br>You can use it for render animation. If not link to the task node, the task will inherit the context frame of the scene(only render one frame in render list)

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Image Format

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> Provide the 3 base format for output.<br>Also can handle the transparent of the image(Only for blender built-in engine), make sure select RGBA to save the alpha channel
> 

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### File Path

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> This node use $ to get the properties of the render task,then apply it to the output file name <br>Usage(Also show in the side pannel):
> 
>```
> $blend: name of your file (save first!)
> $label: Task label
> $camera: name of scene camera
> $res: resolution (X x Y)
> $engine: render engine
> $vl: name of scene view layer
> $date: month-day
> $time: hour-min
> /: create folder,should be dict_input folder name in front of "/"
> ```

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Render Slot

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> This node allow you to put the render result into different render slot of the image eidtor

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### View Layer Passes

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> This node allow you to output different passes of a select viewlayer <br>if you need to disble this option, you need to link a new node to disable it .
> 

<!-- panels:end -->