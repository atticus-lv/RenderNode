<!-- panels:start -->

<!-- div:title-panel -->

### Resolution

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> 此节点可以更改输出分辨率

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Frame Range

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> 此节点可以更改输出帧范围。<br>可以将其用于渲染动画。如果未链接到任务节点，则任务将继承场景的当前帧（在渲染列表中仅渲染一帧）
>

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Image Format

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> 为输出提供3个基本格式。<br>还可以处理图像的透明性（仅适用于blender内置引擎），选择RGBA来保存alpha通道

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Image Format

### File Path

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> 此节点使用$获取场景/task节点的属性，然后将其应用于输出文件名（格式化输出）<br>用法（另见侧面板）
>
> ```
>$blend: 文件名（先保存！）
> $F4: 帧数格式:0001 ("4"代表四位补全，可以是其他数字)'
> $label: Task节点的标签
> $camera: 场景摄影机的名字
> $res: 分辨率（X X Y）
> $engine: 渲染引擎
> $vl: 场景视图层的名称
> $T{}: %Y%m%d %H-%M-%S → 20210223 17-47-35"
> ↑{}内参考 python time库的用法 
> /: 创建文件夹，/前为文件夹名字
> ```

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Render Slot

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> 此节点允许您将渲染结果放入图像编辑器的不同渲染槽中

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### View Layer Passes

<!-- div:left-panel -->

image

<!-- div:right-panel -->

> 此节点允许您输出选定viewlayer的不同通道（拆分）<br>如果需要取消此选项，则需要链接一个新节点以禁用它。

<!-- panels:end -->