import minium
import time
from ddt import data, ddt


@ddt
class FuwuTest(minium.MiniTest):
    @data(*range(5))
    def test_fuwu(self, index):
        """测试页面滚动功能（循环执行5次）"""
        # 导航到目标页面
        page = self.app.redirect_to("/page/fuwu_xieyi/fuwu_xieyi")
        self.page.wait_for(2)  # 等待页面加载
        self.logger.info(f"开始第 {index + 1}/5 次滚动测试")
        # 执行滚动操作（持续时间2000ms）
        page.scroll_to(100200, 10000)
        time.sleep(20)
        self.logger.info(f"第 {index + 1}/5 次滚动测试通过")
