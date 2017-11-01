Title: Vegas 用 FrameServer 搭桥
Date: 2017-09-23 14:16:48
Modified: 2017-09-23 15:30:52
Author: 71e6fd52
Category: Windows
Tags: Vegas

之前为了让 Sony Vegas pro 13.0 用 DebugMode FrameServer 搭桥，研究了很久最后发现了一个很简单的办法

1. 安装 [Vegas](http://vegasbar.lofter.com/post/1d4450de_74cd602)
2. 安装 [DebugMode FrameServer 的 Vegas 13 版](http://pan.baidu.com/s/1pLRarub) 密码：6qf3
  1. 打开安装程序
  2. 点击 I Agree
  3. 确定 Sony?Vegas…… 勾着
  4. 点击 Next
  5. 选择 DebugMode FrameServer 的安装路径
  6. 点击 Next
  7. 确定 Vegas 13 的安装路径（默认是 C:\Program Files\Sony\Vegas Pro 13.0 ）
  8. 点击 Install
  9. 安装时会弹出来一个对话框问你是否要创建开始菜单项，没什么用，建议点否
3. 打开 Vegas ，在要渲染的工程里点击渲染为
4. 使用 DebugMode FrameServer (\*.avi) 中的 Project Default
  * 打上第一个勾
5. 已经导出了临时文件（桥）了。

所以，为什么不用 FFmpeg 呢
