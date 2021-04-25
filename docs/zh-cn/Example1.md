### Usage scenarios

> 现有一位设计师，需要对自己制作好的茶壶茶杯用具进行渲染。 <br>该设计师预计要出三张图片用于平面排版，分别是顶视图（正交），全画幅（50mm）， 特写（110mm)<br>按照设计流程，设计师在设置好了模型，光照以及相机后，他需要先给提交一个小样 （低采样/低分辨率）的图给对接的人员<br>确认修改细节后再输出大图（高采样，高分 辨率）

<img src="media/img/example1/0.png" alt="0" width="960px" />

<!-- panels:start -->

<!-- div:title-panel -->

### Set Preview

<!-- div:left-panel -->

<img src="media/img/example1/1.png" alt="1" width="960px" />



<!-- div:right-panel -->

1. 切分新的 RSN 节点面板，接下来所有操作都在此面板中
2. 新增三个任务节点和三个相机节点，分别连接
3. 选中任务节点按 v 键，就可以预览该任务的相机视角 



<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### Set File Path

<!-- div:left-panel -->

<img src="media/img/example1/2.png" alt="2" width="960px" />

<!-- div:right-panel -->

添加路径节点，命名路径表达式为 `$blend_render/$V/$camera` 

>[!TIP]
> 这样输出图片 时候就会放到场景文件所在的文件夹<br>并以版本滑块作为子文件夹，相机名字作为图片名字<br>这样可以方便进行多个版本的更改



<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### 配置渲染采样

<!-- div:left-panel -->

<img src="media/img/example1/3.png" alt="3" width="960px" />

<!-- div:right-panel -->

1. 新增 cycles Settings 节点
2. 按 f 弹出 RSN 帮助菜单，选中合并选中项
3. 选中三个任务节点和新增的合并节点，继续呼出帮助菜单， 选中连接单节点到多任务命令

<!-- panels:end -->

<!-- panels:start -->

<!-- div:title-panel -->

### 渲染

<!-- div:left-panel -->



<img src="media/img/example1/4.png" alt="4" width="960px" />

<!-- div:right-panel -->

最后，添加渲染列表和进度条节点（非必要），使用帮助菜单进行快速连接<br>点一点 确认渲染就可以开始渲染了

> [!TIP]
>
> 设计师若需要制作小样，只需要点一点 half 按钮，就能自动减半采样<br>再把路径节点的版本滑块更改下，就能改变输出路径了 



<!-- panels:end -->

### 输出结果

### <img src="media/img/example1/5.png" alt="5" width="720px" />