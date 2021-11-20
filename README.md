<p align="center">
  <a href="https://atticus-lv.github.io/RenderStackNode/#/">
    <img src="res/logo.png" alt="logo" width="1080px"/>
  </a>
</p>
<h4 align="center">
    Node based design and render workflow in blender<br>
</h4>
<p align="center">
    Documentation ➡️
    <a href="https://atticus-lv.github.io/RenderStackNode/#/">
	[Github] 
    </a>
    <a href="https://atticus-lv.gitee.io/renderstacknode">
    <tr>[Gitee]
    </a>
</p>


### Feature

| v1.2.4           | Description                                            |
| ---------------- | ------------------------------------------------------ |
| Render queue     | render animation and still frame in one queue          |
| UI               | processor bar,viewport gpu draw nodes,tab search       |
| Custom Overwrite | all properties can be overwrite and update in viewport |
| Path Expression  | use $ to generate formatted name                       |
| Version Control  | various sth and set various in one task                |
| Path Expression  | use $ to generate formatted name                       |
| Third Party      | Octane, Luxcore, SSM(an other addon of mine)           |

**Preview**

<img src="res/feature.gif" width="1080px" />

### Download ![![](docs/media/logo/blender%20logo.png)](https://img.shields.io/badge/blender-2.93%2B-red)

**Stable** *Ready for work*

[Stable 1.2.4.1 📚 ](https://github.com/atticus-lv/RenderStackNode/releases/tag/v1.2.4)

### Develop Feature 

<img src="res/feature_develop.png" width="1080px" />

**Develop** *New features, change any time before stable*:

[https://github.com/atticus-lv/RenderStackNode/archive/develop.zip](https://github.com/atticus-lv/RenderStackNode/archive/develop.zip)

+ Workflow
  + Geometry Nodes field style workflow , much easier and cleaner


+ Nodes
  
    + group nodes

    + new swith node(no 'Variants Node'any more, use a direct input socket)

    + input nodes (object/material/float/vector/int/bool/string)

    + utility nodes (math/vector,boolean math/string operate)
+ Performance (Evaluate system)

    + develop based on rigging_nodes' , provide faster speed
+ UI
  
    + remove old draw outline, draw process time and node name instead instead
    + dynamic enums/sockets for user' preference (render engine, color manage,etc)
+ Know Limited
  
    + When edit inside a render node group, it won't update the whole tree, you should always set the active task on the base root
    
    + old node remove
    
### Support me

blendermarket: https://blendermarket.com/products/renderstacknode

alipay: 1029910278@qq.com
