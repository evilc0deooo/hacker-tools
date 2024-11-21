该脚本 crawlergo_linux_amd64 联动 Xray 进行批量漏扫操作。

使用方法：
    - 将所有目标放入 targets.txt 文件。
    - 执行命令：docker build -t xray .
    - 执行命令：docker run -itd xray
    - 执行完毕会自动进行批量漏扫操作，可查看 /root/debug.log 文件来查看脚本运行情况。
    - 报告输出位置在 /root/output_{time}.html