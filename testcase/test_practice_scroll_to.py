import minium, time
from ddt import data


class PageTest(minium.MiniTest):

    def test_scroll_to(self):
        page = self.app.redirect_to("/page/message_list/message_list")
        # 2000ms内页面滚动到高度为700px的位置
        time.sleep(2)
        page.scroll_to(700, 2000)
        time.sleep(5)
