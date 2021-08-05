Title: 破解课后网
Date: 2020-04-17 09:32:01
Author: yahvk
Category: 
Tags: kehou
Summary:

疫情期间在家上网课，我们学校用的是[课后网](https://www.kehou.com/)。
为了能在网课上摸鱼，我就破解了课后网。

## 防止摸鱼

在课后网中每节课都有这么一个表格

![家长督学界面]({attach}images/kehou-1.webp)

我的目的就是让认真度为 100%

### 签到

在上课过程中，软件会随机跳出签到按钮，有 20 秒的签到时间，超时就算作未签到。
一般一节课会有 2 次签到。

### 认真度

![认真度规则]({attach}images/kehou-2.webp)

认真度主要受在线时间、「认真时间」和上文所说签到次数的影响。

「认真时间」app 内没有给出解释，经过实测，切出 app 后是不认真时间，只要让 app 在前台就算是认真。

### 锁屏

Windows 端的课后网程序会不断的获取焦点来让自己显示在最上方，影响其它程序的使用。

## 破解一：反编译 apk

最初，我认为 apk 的反编译会比 Windows 的简单很多，所以我就对 apk 下手了。

没有反编译经验，这里的反编译流程是我自己 google 研究出来的，不一定是最好的。

我当时用的课后网的 apk 传到 mega 上了：[https://mega.nz/file/8HAg1YpS#odqb6VBz6j3jQdeYEK1CstimutTu2tdEGeq_6Vf9LjE](https://mega.nz/file/8HAg1YpS#odqb6VBz6j3jQdeYEK1CstimutTu2tdEGeq_6Vf9LjE)

### 反编译

```sh
apktool d kehou.apk -o kehou-apktool # 解包 kehou.apk 到 kehou-apktool
d2j-dex2jar kehou.apk # 提取 kehou.apk 代码为 jar
jadx kehou-dex2jar.jar # 把上一步提取出的 jar 反编译为 java 代码放在 kehou-dex2jar/sources/
```

### 修改代码

#### 签到

反编译完了就可以找代码了，在 kehou-apktool/res `rg 签到` 找到了一个叫做 **rollcall_confirm** 的 layout。

再在 kehou-dex2jar/sources/ `rg rollcall` 找到了签到主要在
`vizpower/imeeting/RollCallMgr.java` 和 `vizpower/imeeting/viewcontroller/RollcallConfirmViewController.java` 两个文件。

对代码一番研究后找出当签到开始时会调用 `RollcallConfirmViewController#onStartRollcallConfirm`，
点击签到按钮后会调用 `RollcallConfirmViewController#onBtnClickRollcallConfirm`。

所以只要在 `onStartRollcallConfirm` 中调用 `onBtnClickRollcallConfirm`，就可以在开始签到的时候自动签到了。

然后我还在 `onBtnClickRollcallConfirm` 加了个提示：

```java
Toast.makeText(this.m_pIMainActivity.getActivity(), "已自动签到", Toast.LENGTH_LONG).show();
```

#### 认真度

由上一步可以看出来所有课后网自己的代码都在 vizpower 中，直播课相关的内容在 vizpower/imeeting。

由「认真时间」的计算方法可以推断逻辑是写在 `onPause` 回调内，直接在 vizpower/imeeting `rg onPause -A5`，找出这部分代码在 `MainActivity.java` 中。

「认真时间」的计算来自于 Timer 发的心跳包，这个 Timer 在 `onPause` 停止，在 `onResume` 中恢复。
在 `onPause` 中把停止 Timer 的 `DesktopShareMgr.getInstance().stopDSTimer();` 这一行注释掉就可以一直「认真」了。

### 编译回 apk

需要 Android SDK，编译出 class 文件：

```sh
javac -cp /opt/android-sdk/platforms/android-29/android.jar:.../kehou-dex2jar.jar <edited files> # 把 android.jar 和 kehou-dex2jar.jar 的路径换成你自己的
```

把编译出来的 class 文件按原来的目录组织起来，我放在 inject/source 下，然后编译出 dex 文件，再反编译为 smali 文件：

```sh
dx --dex --output=classes.dex source
d2j-baksmali classes.dex
```

然后用这些 smali 替换掉 apktool 解出来的 smali 文件，然后用 apktool 打包，再签名。

```sh
apktool b kehou-apktool
cd kehou-apktool/dist/
d2j-apk-sign kehou.apk
```

### 附注

有一些文件内有部分无法反编译的代码，这时用上一节的方法就不行了，
这时要找出对应的函数，只把编译出的对应函数的 smali 代码覆盖过去，而不是所有文件。

也可以直接编辑 apktool 解出来的 smali 文件，我后来就是这么做的。
但是有时候直接改 smali 代码，大概是改出了些问题，app 执行到那部分代码时会崩溃，这时还是用上一节的方法吧。

## 破解二：辅助功能

在一次强制更新后，课后的 app 使用了 360 加固，破解一失效。

我想到了抢红包的原理，于是我找到了[《Android 通过辅助功能实现抢微信红包原理简单介绍》](https://www.jianshu.com/p/e1099a94b979)。

这段暂略……

## 破解三：修改网络流量

以为破解二不能破解「认真时间」，所以上课时间这台手机就用不了了，我对此并不满意。
这次我把目标转移到了 PC 端上。

首先，因为锁屏和我使用 Linux 的需求，我就把课后网装到了虚拟机上。

反编译 native code 的程序难度太大了，所以很容易想到从网络入手。

代码：[https://gitlab.com/71e6fd52/kehou_proxy](https://gitlab.com/71e6fd52/kehou_proxy)

### 通讯协议

我用的 VirtualBox 自带抓包功能：

```sh
mkfifo /tmp/file.pcap
VBoxManage modifyvm vm1 --nictrace1 on --nictracefile1 /tmp/file.pcap
wireshark -k -i /tmp/file.pcap &
```

但是看抓出的包并不容易看出来，只能看出通讯在 9980 端口上，这时破解一中反编译的源代码就派上了用场。

经过对源代码的分析可以看出包的格式为 `0x02 0x02 <后面的长度:i16> 0x01 <命令号:i16> <内容>`，
所有数字为小端。

所有命令在 vizpower/mtmgr/PDU 下，如 `ReplyNaming` 的命令号为 -32206(0x32 0x82)，内容由

```java
public byte bTime = ((byte) 0);
public int dwUserID = 0;
...
byteBuffer.putInt(this.dwUserID);
byteBuffer.put(this.bTime);
```

可见先是 i32 的 dwUserID，然后是 i8 的 bTime。

再看一下调用的代码可以看出来 dwUserID 是加入课堂时会由 `NotifyJoinMeeting`(-32254) 分配的 ID，
bTime 是签到所花的秒数。

### 修改网络

先要让网络经过 nftable，我最初用的是 arp 攻击，后来直接让主机作为虚拟机的网关。

建一个 tap，此处虚拟机网段为 192.168.2.0/24 ：

```sh
ip tuntap add dev tap0 mode tap user $USER
ip addr add 192.168.2.1/24 scope link dev tap0
ip link set tap0 up
```

虚拟机设置为桥接网络，桥接在 tap0 上。

在把所有发往 9980 的端口劫持了（以主机地址为 192.168.1.200 为例）：

```text
table ip nat {
  chain prerouting {
    type nat hook prerouting priority 0;
    ip saddr 192.168.2.0/24 tcp dport 9980 dnat to 192.168.1.200;
  }
}
```

接下来再在主机上启动一个监听 9980 端口的程序，并把收到的数据（做些修改的）转发到课后网的服务器上。
这个程序在收到 `NotifyJoinMeeting`(-32254) 时记录下 UserID，
在收到 `RequestNaming`(-32207) 时回复 `ReplyNaming`(-32206)。

### 获取 ip

上一节所说的中间程序需要连接到课后网的服务器上，但是据我观察，课后网的服务器地址每节课是不一样的。

所以我就加了一个程序，抓取课后网试图连接的服务器的 ip 地址发送给这个中间程序，这就是我的代码中 `pcap_server.rb` 的用处。
