<!-- panels:start -->

<!-- div:title-panel -->

### Resolution

<!-- div:left-panel -->

<img src="media/img/nodeOutput/1.png" width="720px">

<!-- div:right-panel -->

> 此节点可以更改输出分辨率
>
> 当你选择这个节点为激活节点时，你可以留意到你能够使用RSN的预设了<br>你也可以启用旁边的小按钮来进入添加/移除预设模式

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Frame Range

<!-- div:left-panel -->

<img src="media/img/nodeOutput/2.png" width="720px">

<!-- div:right-panel -->

> 此节点可以更改输出帧范围。<br>可以将其用于渲染动画。如果未链接到任务节点，则任务将继承场景的当前帧（在渲染列表中仅渲染一帧）
>

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Image Format

<!-- div:left-panel -->

<img src="media/img/nodeOutput/3.png" width="720px">

<!-- div:right-panel -->

> 为输出提供3个基本格式。<br>还可以处理图像的透明性（仅适用于blender内置引擎），选择RGBA来保存alpha通道

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Image Format

### File Path

<!-- div:left-panel -->

<img src="media/img/nodeOutput/4.png" width="720px">

<!-- div:right-panel -->

> 此节点使用$获取场景/task节点的属性，然后将其应用于输出文件名（格式化输出）

用法（另见侧面板）

```
$blend: 文件名（先保存！）
$F4: 帧数格式:0001 ("4"代表四位补全，可以是其他数字)'
$label: Task节点的标签
$camera: 场景摄影机的名字
$res: 分辨率（X X Y）
$engine: 渲染引擎
$vl: 场景视图层的名称
$T{}: %Y%m%d %H-%M-%S → 20210223 17-47-35"
↑{}内参考 python time库的用法 
/: 创建文件夹，/前为文件夹名字
```

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Render Slot

<!-- div:left-panel -->

<img src="media/img/nodeOutput/5.png" width="720px">

<!-- div:right-panel -->

> 此节点允许您将渲染结果放入图像编辑器的不同渲染槽中

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### View Layer Passes

<!-- div:left-panel -->

<img src="media/img/nodeOutput/6.png" width="720px">

<img src="media/img/nodeOutput/6.5.png" width="720px">

<!-- div:right-panel -->

> 此节点允许您输出选定viewlayer的不同通道（拆分）<br>如果需要取消此选项，则需要链接一个新节点以禁用它。
>
> 请保证你的激活的合成节点名字为"Composite"(默认)<br>否则将出现 Runtime Error 的报错<br>
>
> <img src="media/img/nodeOutput/6.6.png" width="360px">
>
> 你可以在 1.2.3版本及以上来更改默认的名字（针对想保持翻译新建数据的用户）<br><img src="media/img/nodeOutput/6.7.png" width="360px">

<!-- panels:end -->