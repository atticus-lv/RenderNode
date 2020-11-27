# Node-based RenderStack [Blender Addon]

Design Target: Provide users with node-based, flexible rendering output methods

Preliminary idea (finish getting info from nodes)

![img1](img/img1.png)



**Info Node Data**

> use it to overwrite settings

```json
{
    "0":{
        "name":"Task",
        "Camera Settings":{
            "Res X":1920,
            "Res Y":1080,
            "Res Scale":100
        },
        "Render Settings":{
            "Engine":"CYCLES",
            "Samples":128
        }
    },
    "1":{
        "name":"Task.001",
        "Camera Settings":{
            "Res X":1200,
            "Res Y":1600,
            "Res Scale":50
        },
        "Render Settings":{
            "Engine":"CYCLES",
            "Samples":64
        }
    }
}
```

