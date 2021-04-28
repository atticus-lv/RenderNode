<!-- panels:start -->

<!-- div:title-panel -->

### Task

<!-- div:left-panel -->

<img src="media/img/nodeTask/1.png" width="720px">

<!-- div:right-panel -->

> Task 节点是RSN中最重要的节点。它包含可用于渲染的更改
>
> **Settings Input** 设置输入可以插入任何类型的设置节点<br>**Task output** 可以连接到RenderList节点，viewer节点和merge节点

**标签** 可以被用在路径表达式上

**信息按钮** 可以看到设置节点的信息

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Render List

<!-- div:left-panel -->

<img src="media/img/nodeTask/2.png" width="720px">

<!-- div:right-panel -->

> Render list将获取链接到它的所有task。<br>
>
>**Task input** 可以连接到task或者merge节点

**Render confirm 按钮**:将获得渲染确认表。只需按“确认”即可开始渲染。<br>此外，您还可以按标记图标取消某些任务。它将禁用节点，以便渲染列表稍后不会检查它。<br>带有信息图标的小按钮允许您查看此任务的更改。你可以复制它，也可以在文本编辑器中粘贴它。然后与task info节点一起使用

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Processor

<!-- div:left-panel -->

<img src="media/img/nodeTask/3.png" width="720px">

<!-- div:right-panel -->

> Processor节点为每个任务提供一个进程条<br>

如果使用“ ESC”中断渲染，它将存储停止的帧的数值<br>您可以为完成帧和剩余帧设置自己的颜色

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Viewer

<!-- div:left-panel -->

<img src="media/img/nodeTask/4.png" width="720px">

<!-- div:right-panel -->

> 选择task节点时，可以按v键链接viewer节点以查看此任务。<br>
>
> **Task input** 可以连接到Task节点

**Update Scripts** 在视口更新模式下更新scripts节点

**Update FilePath** 在视口更新模式下更新filepath 节点

**Update ViewLayer Passes** 会生成合成节点树

以上三个都会在渲染时候自动执行

如果task节点是禁用状态的的（按M键），它将不会检查这个task<br>确保节点树中只有一个viewer节点。

<!-- panels:end -->