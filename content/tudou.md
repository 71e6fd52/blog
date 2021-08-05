Title: 修复土豆文解码器
Date: 2021-08-05 14:19:52
Author: 71e6fd52
Category: reverseengineering
Tags: reverseengineering

整理硬盘时，在硬盘中翻到了多年前在 [KeyFC](https://www.keyfc.net) 下载的[土豆文](https://www.keyfc.net/bbs/showtopic-25834.aspx)套件，
随着 Windows 系统的不断更新，土豆文解码器的登录检测已经无法正常工作了。

<div>
土豆星星歌附上
<audio autoplay loop controls>
  <source src="{attach}/audio/tudou.opus" type="audio/ogg; codecs=opus"/>
  <source src="{attach}/audio/tudou.mp3" type="audio/mpeg"/>
  <p>看起来你的浏览器听不到呢，<a href="{attach}/audio/tudou.mp3">链接在这里</a></p>
</audio>
</div>

## KeyFC

[KeyFC](https://www.keyfc.net) 是个超级有爱的论坛~

多年前路过 KFC，被神秘的土豆文所吸引。下载完土豆文套件，玩了一会儿，然后尘封在了硬盘的角落里。
也再没访问过 KFC。

硬盘角落中的土豆文套件终于被我看到，使我重新找到了 KFC。已经看完 CLANNAD 的我再次浏览 KFC ，KFC 的温暖深深的感动了我。

## 土豆文

> 土豆文是蕴含了世界发展底层规律的远古先进语言，其真正来源已不可考。
> 土豆文不是文字，而是一种规律。
> 土豆文不通过文字本身表达意思，而通过字符的排列规律展现其含义。
> 现代科学研究认为，土豆文主要展现了以下规律：
> 1. 叠加。事物之间没有明显的边界，对与错，好与坏，阴与阳等总是相互纠缠在一起，不停的复制叠加成为不同的繁复形态。
> 2. 相似。事物之间有普遍的相似性，不仅表现在事物之间的相似，也表现在局部与整体的相似，过去与未来的相似
> 3. 同源。 复杂的甚至是对立的事物，同样是由初始的最简单的某种元素，根据叠加与相似的规律发展而成。

https://www.keyfc.net/bbs/showtopic-22242.aspx

总之，土豆文就是一种对文字的编码，长这样：

> 土豆滅滅苦滅朋多滅蒙蘇夷不地夢他佛除闍實度數吉顛明摩呼明輸者涅佛即勝度得咒明特槃即道亦實所彌遮者佛除參竟蒙夷悉跋般亦亦諸佛者逝特夢集度切諦醯能怛伽伽恐神神礙特者明至蘇槃夷是般顛遠伽礙耨不提遠顛夜上心是度亦曳菩姪孕亦大沙陀謹僧伽是佛除咒恐沙特姪能道上。遠無參佛心竟大度是參知迦能道上。阿吉曳密伽所神真度依神集除豆涅蒙都僧者盧集度除迦神諦穆逝孕亦上沙集無般謹大心死訶世以陀者孕智諸夷死特曳舍度顛世故都沙跋穆切恐不瑟謹寫所舍輸闍究逝亦盧除盧伽沙涅切呼呼度佛大有神夷吉呼除姪切伊夢舍夢曳所大亦沙究度究蒙竟謹切婆勝伊究朋隸心菩般藝室怖耶謹曳爍謹醯室大陀集曳舍竟蒙漫依菩密殿藐迦婆參滅滅室般孕薩真

## 登录

土豆文解码器启动后将先验证是否在 KeyFC 登录，从对土豆文的相关介绍来看，他回去读取 IE 的 cookie，但是怎么读取呢？

上火绒剑！

![火绒剑界面]({attach}images/tudou-1.webp)

从火绒剑分析得到，它调用了 wininet 的 [InternetGetCookieA](https://docs.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetgetcookiea) 函数。
但是用 IE11 登录 KFC 并不能让解码器登录，大概是 IE11 已经不用这套函数了。

继续研究 wininet 的文档，找到了另一个函数 [InternetSetCookieA](https://docs.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetsetcookiea)。
那么推测只要用 InternetSetCookieA 设置了 Cookie，就可以使解码器登录了。

写了个 Powershell 脚本设置了 Cookie，但是并没有成功（实际上是复制时漏了字符），上 OD！

## 脱壳

为了找出解码器的具体工作原理，我决定反编译。

PEiD 查壳 `PECompact 2.x`，esp 定律后单步跟踪到 `0053C715 jmp eax`，顺利找到 oep 004c7618。

![jmp eax]({attach}images/tudou-2.webp)
![oep]({attach}images/tudou-3.webp)

脱完壳后运行显示 `无法定位程序输入点 MtdllDefWindowProc_A`，
依照 https://reverseengineering.stackexchange.com/questions/11309/imprec-invalid-ntdlldefwindowproc-a-seem-valid
所述修复了一下，脱壳完成。

## 探索

由前面所述，解码器使用的是 `InternetGetCookieA` 函数，直接 OD 打断点在 `InternetGetCookieA` 上。
跟踪一下，发现它实际上只读取了 `dnt` 这一个 cookie，然后发现了我复制 Cookie 时的错误……

![OD界面]({attach}images/tudou-4.webp)

## 完成

土豆文解码器会使用 `InternetGetCookieA` 轮询 `http://www.KeyFC.net` 的 Cookie，从中提取出 `dnt` 的值。
`dnt` 的值形如 `userid=<userid>&password=<encoded password>&...`，根据我的观察，解码器实际上只提前了其中 userid 的值。

最后我用 powershell 做了一个登录器：
```powershell
$source=@"
using System.Runtime.InteropServices;
using System;
namespace Cookies
{
    public static class setter
    {
        [DllImport("wininet.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern bool InternetSetCookie(string url, string name, string data);
 
        public static bool SetWinINETCookieString(string url, string name, string data)
        {
            bool res = setter.InternetSetCookie(url, name, data);
            if (!res)
            {
                throw new Exception("Exception setting cookie: Win32 Error code="+Marshal.GetLastWin32Error());
            }else{
                return res;
            }
        }
    }
}
"@

Add-Type -TypeDefinition $source -Language CSharp

[DateTime]$dateTime = Get-Date
$str = $dateTime.AddDays(30).ToString("R")

$dnt = Read-Host -Prompt '请输入 Cookie dnt 的值'
$dnt = $dnt -replace '^(dnt)?\s*:?\s*"?', ''
$dnt = $dnt -replace '"$', ''

[Cookies.setter]::SetWinINETCookieString("http://www.keyfc.net", "dnt", "$dnt;Expires=$str")
```

之后大概会做个 Qt 版的发 KFC 上。
