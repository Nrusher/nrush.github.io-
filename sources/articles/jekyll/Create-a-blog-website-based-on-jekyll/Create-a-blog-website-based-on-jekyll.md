---
layout: default
title:  "Create a blog website based on jekyll"
create_time: 2023-02-28 00:34:13
categories: jekyll
author: Nrush
---

<center><strong><font size=6>Create a blog website based on jekyll</font></strong></center>

- this unordered seed list will be replaced by toc as unordered list
{:toc}

Good tools are essential to do the job well. This blog is used to record how to use jekyll.

## 1 What is jekyll?

Jekyll is a tool which can help you create a static blog website fastly and easilly.

Here are some links about jekyll:

- Home page of jekyll: <https://jekyll.com>
- Jekyll中文主页: <https://jekyllcn.com>
- A website where you can find many jekyll themes: <http://jekyllthemes.org>

Here are some blog websites based on jekyll, they provide good examples
- <http://gohom.win/>

## 2 A quick start about how to use jekyll. [on ubuntu server]

### 2.1 Install

```sh
# Install ruby
sudo apt-get install ruby-full build-essential zlib1g-dev

echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Change gem's source, you can use `gem sources -l` to see wether the source has been
# changed sucessfully. This step is not essential. However, if you don't do that, the
# download speed of gem will be super slow :)
gem sources --remove https://rubygems.org/
# 国内加速源
gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/

# install jekyll and  bundler
gem install jekyll bundler

# Change bundle's source. For same reason of changing gem's source.
# 国内加速源
bundle config mirror.https://rubygems.org https://mirrors.tuna.tsinghua.edu.cn/rubygems
```

### 2.2 View the first jekyll page in local

```sh
# Init jekyll website dir
jekyll new ~/myblog
cd myblog
# start the serve
jekyll serve
# Now browse to http://localhost:4000

# When you want to browse the website on another PC which is in the same
# LAN as your serve, use following cmd. Then, you can browse to the 
# x.x.x.x:4000 where x.x.x.x is the ip of your serve.
jekyll serve -w --host=0.0.0.0

# if want to see drafts, use
jekyll serve -w --host=0.0.0.0 --drafts
```

OK, now a website is ready. The rest is how to decorate the website, enjoy it!

## 3 how to publish the blog website on the internet?

There are many ways to publish the website, some are free and some should pay some money.

Free ways:
- Github pages: <https://pages.github.com/>
- Gitee pages: <https://gitee.com/help/articles/4136>
- The static web hosting service of Coding: <https://coding.net/>

The greatest advantage of `free ways` is free, the biggest disadvantage of `paid ways` is I must give some money to service provider. OK, for a better browsing experience and saving time, I choose a `paid way`

- cloudbase: <https://docs.cloudbase.net/hosting/quick-start> [ This is not a advertisement, believe me ...... :) ]

**step 1**: Buy cloudbase service.

**step 2**: enable static web hosting service.

**step 3**: Install `tcb` on local PC.

```sh
apt install nodejs npm
npm i -g @cloudbase/cli
tcb login --key
cd <website path>
tcb hosting deploy ./ -e <envid>
```


## 4 Some records about how to decorate the website

## 4.1 Add favicon.ico

The error is very annoying, fix it!
```
Not Found: /favicon.ico
```
- prepare a picture you like (png, jpg ...) or use <https://www.logosc.cn/logo/> to get one.
- use <https://www.bitbug.net/> create a favicon.ico.
- add `<link rel="shortcut icon", href="/the/path/of/your/ico">` to the head of html.

OK, the ico has been shown on the tab now.

## 4.2 Default values of website

Set the values in _config.yml
```
defaults:
  -
    scope:
      path: "/_posts/"
    values:
      author: Nrush
```
