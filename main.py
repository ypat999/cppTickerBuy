import argparse

import gradio as gr
from loguru import logger

from tab.go import go_tab
from tab.login import login_tab
from tab.order import order_tab
from tab.problems import problems_tab
from tab.settings import setting_tab

#CP30_URL="https://www.allcpp.cn/allcpp/event/event.do?event=1729"

header = """
# CPP 抢票🌈

⚠️此项目完全开源免费 （[项目地址](https://github.com/mikumifa/cppTickerBuy)），切勿进行盈利，所造成的后果与本人无关。
"""

short_js = """
<script src="https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js" rel="external nofollow"></script>
<script src="https://static.geetest.com/static/js/gt.0.4.9.js"></script>
"""

custom_css = """
.pay_qrcode img {
  width: 300px !important;
  height: 300px !important;
  margin-top: 20px; /* 避免二维码头部的说明文字挡住二维码 */
}
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860, help="server port")
    parser.add_argument("--share", type=bool, default=False, help="create a public link")
    args = parser.parse_args()

    logger.add("app.log")
    with gr.Blocks(head=short_js, css=custom_css) as demo:
        gr.Markdown(header)
        with gr.Tab("配置"):
            setting_tab()
        with gr.Tab("抢票"):
            go_tab()
        with gr.Tab("查看订单"):
            order_tab()
        with gr.Tab("登录管理"):
            login_tab()
        with gr.Tab("常见问题"):
            problems_tab()

    print("CPP账号的登录是在此控制台，请留意提示！！")
    print("点击下面的网址运行程序     ↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    demo.launch(share=args.share, inbrowser=True)
