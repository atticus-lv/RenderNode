# Node-based RenderStack [Blender Addon]

### **Design Target**

Provide users with node-based, flexible rendering output methods

### Features

> version 0.5 alpha
>
> 中文介绍请看视频 https://www.bilibili.com/video/BV1wr4y1c7Tt/

+ Camera overide
+ Render Engine overide （Workbench,Eevee,Cycles）
+ Output Setting overide  (Frame Range,Resulotion,path（format file name support）,image settings)
+ View overide settings



### How it works

 + **Render List Node** is a render task list for what you need to render.It also  provide the 'Render' button and the 'View' button.You can render your task through this node. *Now you are only able to render one renderlist at once*

 + **Task Node** You need a task node to countains all the settings you need to change(compare to the current settings)
 + **Camera Node** have the ability to change the camera
 + **file path Node** give an format name of the render files
 + **Eevee Setting Node** means that in this task you will render with the eevee engine
 + **Frame Range Node** control the frame you want to render

> *Once you plug a node settings to overide something into the a task,the next task will inherit it if there is not a same type Node plug input. So you may start a new render list to keep your node tree cleaner*

![img1](img/img1.png)



### Install

##### Familiar with **git**

If you are familiar with **git**, just go to your addon folder(For example,you are using windows)

`C:\Users\{YourUserName}\AppData\Roaming\Blender Foundation\Blender\2.92\scripts\addons`

Then right click and **git bash here**, type in:

`$ git clone https://github.com/atticus-lv/RenderStackNode.git`

**For Other User**

Click [here](https://github.com/atticus-lv/RenderStackNode/releases/tag/alpha) to down the latest stable release



### Nodes

+ Render List 

	> Provide Viewer operator for input tasks, and render all the input task

![image-20201130131530141](img/image-20201130131530141.png)

+ Task

    > output task( Link to the render list node)
    >
    > all the overide settings is link to this node 

![image-20201130131850636](img/image-20201130131850636.png)

+ Camera 

	> Camera overide input

![image-20201130133131141](img/image-20201130133131141.png)

+ File path

    > format ouput of the file name 
    >
    > <img src="img/image-20201130133526636.png" alt="image-20201130133526636" style="zoom: 50%;" />

<img src="img/image-20201130133157140.png" alt="image-20201130133157140"  />

+ Eevee Settings / Cycles Settings / Work Bench Settings

    >  change the render engine



### Plans

v 0.5

+ [x]   Basic renderstack with nodes 
+ [x] eevee, cycles basic support 
+ [x]  camera, resulotion, frame range, file format, format file name support

v 1.0

+ [x]  command node for custom render settings overwriting
+ [ ]  render list merge node (or someting else for render all list)
+ [ ]  task marker (won't need to unlink task to no render )
+ [ ]  scene overwriting (maybe)

