// ==UserScript==
// @name                慧博投研咨询定制插件v1.1
// @description         绕过下载区域的链接的权限
// @namespace   yfmx746qpx8vhhmrgzt9s4cijmejj3tn
// @icon                        http://ww1.sinaimg.cn/large/4ec98f50jw1e85azvlnh9j206y06y3ye.jpg
// @author                      zhnlk
// @include        http*://*.microbell.com/*
// @include        http*://*.hibor.com.cn/*
// @include        http*://microbell.com/*
// @include        http*://hibor.com.cn/*
// @version                     2016-06-28
// @grant        none
// ==/UserScript==

//2016.06.28 绕过下载区域的链接的权限
//2016-08-31 v1.1版更新，自动获取uname和did

var viewEle = document.getElementById("view");
if(viewEle){
    //====点击浏览
    //去掉click事件
    viewEle.removeAttribute("onclick");
    //将按钮的链接替换
    viewEle.parentNode.setAttribute("href","webpdf.asp?uname="+document.getElementById('hduname').value+"&did="+document.getElementById('hddocurl').value+"&degree=1&baogaotype=1&fromtype=21");
    //====立即下载
    var downNow = viewEle.parentNode.nextElementSibling;
    downNow.children[0].removeAttribute("onclick");
    downNow.setAttribute("href","webdownload.asp?uname="+document.getElementById('hduname').value+"&did="+document.getElementById('hddocurl').value+"&degree=1&baogaotype=1&fromtype=21");
    //====迅雷下载
    var downWithThunder = viewEle.parentNode.nextElementSibling.nextElementSibling;
    downWithThunder.children[0].removeAttribute("onclick");
    downWithThunder.setAttribute("href","webxunlei.asp?uname="+document.getElementById('hduname').value+"&did="+document.getElementById('hddocurl').value+"&degree=1&baogaotype=1&fromtype=21&Pid=13950");
}