RSN插件是一款基于节点的，为用户提供灵活渲染输出流程的插件。它同样适用于视觉开发和设计迭代当中。事实上，它有点像节点版本的场次系统

## RSN能做什么

> [!NOTE]
> RSN的核心是在渲染前修改场景中的数据，这使得它有着比较好的灵活性

举一个简单的例子

+ 渲染场景中**多个镜头**，并以相机的名字作为输出的图片名字 [👉链接](Example1.md)
+ 在这个每个镜头里，物体的**摆放，材质，数据**都可以是不同的 [👉链接](Example2.md)
+ 为其中的某一个镜头添加**动画**，并以另外一个渲染引擎（比如workbench）来渲染
+ 假如不确定一个镜头要渲染多久，可以在渲染后向指定邮箱发送报告邮件
+ 只需要按一下按钮，就能将以上所有需要的镜头**队列渲染**，无需在电脑面前等待操作

<!-- panels:start -->

<!-- div:title-panel -->

## 下载

<!-- div:left-panel -->

**最新版** *新特性与修复*:

[https://github.com/atticus-lv/RenderStackNode/archive/main.zip](https://github.com/atticus-lv/RenderStackNode/archive/main.zip)

**稳定版** *开箱即用*

[RSN 1.2.1 📚 ](https://github.com/atticus-lv/RenderStackNode/releases/latest)



<!-- div:right-panel -->

> [!TIP]
> 如果你熟悉git的话
>
> `cd C:\Users\{YourUserName}\AppData\Roaming\Blender Foundation\Blender\2.93\scripts\addons`(Windows)
>
> `git clone https://github.com/atticus-lv/RenderStackNode.git`

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

## 工作原理

<!-- div:left-panel -->

<img src="media/img/howitwork.png" width=960px />

<!-- div:right-panel -->

> [!NOTE]
> RSN接受设置节点，并使用它来修改场景，例如：

1. 图中的设置节点有

    + **Camera** 相机节点具有更改相机的能力
    + **File path** 文件路径节点提供渲染文件的格式名称
    + **Eevee Setting** 意味着在此任务中，将使用eevee引擎进行渲染

2. **Task** 任务节点，将更改合并到一个渲染任务中（因此可用于渲染）

3. **Viewer**  查看器节点应用并查看更改

4. **Render List**  渲染列表节点渲染您需要的所有任务

*插入节点设置以将某些内容添加到任务中，如果没有相同类型的Node输入，则下一个任务将继承该场景状态。可以启动一个新的渲染列表，以使您的节点树保持整洁*

<!-- panels:end -->

