

# RenderStackNode [Blender Addon]

>  **Design Target**
> Provide users with node-based, flexible rendering output workflow

![原型](img/prototype.jpg)

### Features v 1.0.6

+ Camera overwrite
+ Render engine overwrite 
    + Workbench,Eevee,Cycles
    + Luxcore
+ Output setting overwrite 
    + Frame Range
    + Resulotion,
    + path (format file name support)
    + image settings
+ Object  overwrite 
    + Material
    + Location/Rotation/Scale
+ Script overwrite
+ Viewer Node (output task overwrite)
+ Renderlist  (render all task)
+ Smtp email 
+ Render Process
    + render info confirm
    + 
+ View layer passes output

> Known Error:
> Render with cuda may cause blender internal errors (python state error)




### How it works

1. Use **Settings Node** to overwirte your render settings,such as:

	+ **Camera Node** have the ability to change the camera
	+ **File path Node** give an format name of the render files
	+ **Eevee Setting Node** means that in this task you will render with the eevee engine
	+ **Frame Range Node** control the frame you want to render

2. Use **Task Node** to merge your changes into one render task (animation or still image)

3. Use **Viewer Node / Task List Node** to check your overwriten scene

4. Use **Render List Node** to render all the task that you need

> *Once you plug a node settings to overide something into the a task,the next task will inherit it if there is not a same type Node plug input(except viewlayer passes node,frame range node). So you may start a new render list to keep your node tree cleaner*

![1.0](img/1.0.png)



### Install

##### Familiar with **git**

If you are familiar with **git**, just go to your addon folder(For example,you are using windows)

`C:\Users\{YourUserName}\AppData\Roaming\Blender Foundation\Blender\2.92\scripts\addons`

Then right click and **git bash here**, type in:

`$ git clone https://github.com/atticus-lv/RenderStackNode.git`

**For Other User**

Click [here](https://github.com/atticus-lv/RenderStackNode/releases/latest) to down the latest stable release



### Important Nodes

> Will be a document website later

#### Render 

+ ##### Render List

	> Render all the input task,also allow to view all the input task info
	
	> *node name*
	
	```json
	{
	    "Task.002": [
	        "Camera.002",
	        "File Path.001",
	        "WorkBench Settings"
	    ]
	}
	```
	> *nodes details for each task*
	
	```json
	{
	    "task_name": "Task",
	    "camera": "Camera",
	    "use_blend_file_path": true,
	    "path_format": "$task/$camera",
	    "path": "C:\\Users\\atticus\\Desktop\\blender\\",
	    "engine": "BLENDER_WORKBENCH"
	}
	```
	
	
	
+ ##### Task List

    > Provide Viewer operator for input tasks (Able to execute script node and email node)

+ ##### Viewer

    > Provide automatic update for task node, desire to iterate designs and view changes as soon as possible

+ ##### Task

    > output task( can be linked to the render list node directly)
    >
    > all the overide settings changes is linked to this node 
    
+ ##### Proccessor

    > View your render process when you are rendering images, if you stop render, give you the latest info of each task

    

#### Settings 

+ ##### Camera 

	> Camera overide input
	
+ ##### Scripts

    > Excute the python code when rendering/view this task

+ ##### File path

    > format ouput of the file name ,tips on the node side bar
    
+ ##### Frame Range

    > set your frame range, if not such node in a task , you will get only one image at frame 1

+ ##### Eevee Settings / Cycles Settings / Work Bench Settings

    >  change the render engine 
    
+ **Merge Settings**
  
  > a merge setting node, have nothing useful but merge settings, which make your node tree more clear
  
+ ##### View Layer Passes

    > Separate passes into folder when rendering, if not such node in a task, nothing happend 

*More ....*



### Plans

v 0.5

+ [x]  Basic renderstack with nodes 
+ [x]  eevee, cycles basic support 
+ [x]  camera, resulotion, frame range, file format, format file name support

v 0.6

+ [x]  script node for custom render settings overwriting
+ [x]  layout merge nodes(more organize)

v 0.7
+ [x]  render list merge node (or someting else for render all list)
+ [x]  viewlayers 
+ [x]  stmp email node 

v 0.8
+ [x] SSM (one of my addons for blender), light studio node( 0.23 version / highter)
+ [x] Viewer Node
+ [x] Worlds

v 0.9

+ [x] luxcore support (basic)
+ [x] render process node (ui)

v.1.0

+ [x]  passes for different enginge (view layer output)
+ [x]  object material overwrite node

Planing... 

+ muti blend file ( socket modules or command line)
+ octane support
+ mesh export



