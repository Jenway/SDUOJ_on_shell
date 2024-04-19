# SDUOJ_on_shell

## 这是什么？

> This repo is still under construction.

这是一个 python 项目，在命令行上使用 [SDUOJ](https://github.com/SDUOJ/OnlineJudge)

## 可以做什么？

- [X] 在终端登录 SDUOJ
- [X] 查看题目列表与题目详情
- [X] 提交代码
- [] 查看提交状态

## How to Use?

### Install 

Download `sduoj-0.0.1.tar.gz` from [release](https://github.com/Jenway/SDUOJ_on_shell/releases) and run:

```bash
pip install sduoj-0.0.1.tar.gz
```

### Run


- 在终端登录 oj 并查看题目,顺便下载题目的 `.md` 文件
    ```bash
    python -m SDUOJ -ojd
    ```
    默认查看 `用户组` 里的 `题单`，如果是 `比赛`，调用的是另外几个 api，如需要可以手动修改一下
- 提交代码，并返回结果(分数)
    ```bash
    python -m SDUOJ -oju
    ```
    上传的目标在 `config.json` 中指定，该文件由运行 `main.py` 得到

## How does it work?

1. 通过山大 SSO 登录 SDUOJ 并获取 cookie
2. 调用 SDUOJ 的 若干 API 

## 一起来完善这个项目

如果你有什么好的想法，欢迎提出 issue 或者 pr
