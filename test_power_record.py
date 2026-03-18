import minium
import time
from ddt import data, ddt


@ddt
class ChargingRecordTest(minium.MiniTest):
    def setUp(self):
        """测试前准备：导航到充电记录页面"""
        self.app.redirect_to("/page/power_record/power_record")
        self.page.wait_for(2)
        self.logger.info("已导航到充电记录页面")

    def tearDown(self):
        """测试后清理"""
        self.logger.info("当前测试用例执行完毕")

    def _get_tab_elements(self):
        """获取分类标签元素列表"""
        return self.page.get_elements(".part1 > view")

    def _switch_tab(self, tab_index):
        """切换到指定分类标签"""
        tabs = self._get_tab_elements()
        if tab_index < len(tabs):
            tabs[tab_index].click()
            self.page.wait_for(1)
            self.logger.info(f"已切换到 {tabs[tab_index].inner_text} 标签")
            return True
        self.logger.error(f"分类标签索引越界: {tab_index}")
        return False

    def _get_records(self):
        """获取当前页面所有充电记录"""
        return self.page.get_elements(".part2")

    # def _scroll_to_bottom(self):
    #     """滚动到底部加载更多记录"""
    #     scroll_view = self.page.get_element(".scroll-view")
    #     if scroll_view:
    #         # 获取滚动视图总高度
    #         scroll_height = scroll_view.evaluate("scrollHeight")
    #         client_height = scroll_view.evaluate("clientHeight")
    #         scroll_y = max(0, scroll_height - client_height)
    #
    #         # 执行滚动
    #         scroll_view.scroll_to(0, scroll_y, duration=1000)
    #         time.sleep(1)  # 等待加载
    #         self.logger.info("已滚动到底部")
    #     else:
    #         self.logger.warning("未找到滚动视图，无法滚动")

    def _verify_record(self, record, index):
        """验证充电记录信息"""
        try:
            order_id = record.get_element(".title").inner_text
            status = record.get_element(".t2.ing").inner_text
            start_time = record.get_elements(".text")[2].get_element(".t2").inner_text
            end_time = record.get_elements(".text")[3].get_element(".t2").inner_text

            self.logger.info(f"验证第 {index + 1} 条记录 - 订单ID: {order_id}")
            self.assertIn("订单ID：", order_id, "订单ID格式错误")
            self.assertIn(status, ["已连接", "充电中", "已结束"], "状态显示错误")
            self.logger.info("记录验证通过")
        except Exception as e:
            self.logger.error(f"记录验证失败: {str(e)}")
            raise

    @data(0, 1, 2, 3)
    def test_switch_tab(self, tab_index):
        """测试分类标签切换功能"""
        # 切换到指定标签
        if not self._switch_tab(tab_index):
            self.fail("分类标签切换失败")

        # 滚动到底部加载所有记录
        # self._scroll_to_bottom()

        # 获取当前标签下的所有记录
        records = self._get_records()
        total = len(records)
        self.logger.info(f"{self._get_tab_elements()[tab_index].inner_text} 标签下有 {total} 条记录")

        # 验证至少有一条记录
        self.assertGreater(total, 0, "标签下无记录")

        # 验证前3条记录
        verify_count = min(3, total)
        for i in range(verify_count):
            self._verify_record(records[i], i)

    def test_scroll_and_verify_all_records(self):
        """测试滚动查看所有记录并验证"""
        # 先切换到全部标签
        self._switch_tab(0)

        # 滚动到底部加载所有记录
        # self._scroll_to_bottom()

        # 获取所有记录
        records = self._get_records()
        total = len(records)
        self.logger.info(f"共有 {total} 条充电记录")

        # 验证所有记录
        for i in range(total):
            self._verify_record(records[i], i)

    def test_click_record_to_detail(self):
        """测试点击记录进入详情页"""
        # 切换到全部标签
        self._switch_tab(0)

        # 滚动到底部加载所有记录
        # self._scroll_to_bottom()

        # 获取所有记录
        records = self._get_records()
        if not records:
            self.fail("没有可点击的充电记录")

        # 点击第一条记录
        records[0].click()
        self.page.wait_for(2)  # 等待详情页加载

        # 验证是否进入详情页（根据实际情况修改验证逻辑）
        current_path = self.page.path
        self.assertIn("power_detail", current_path, "未进入充电记录详情页")
        self.logger.info("成功进入充电记录详情页")

        # 返回充电记录页
        self._click_back_button()
        self.page.wait_for(2)

    def _click_back_button(self):
        """点击返回按钮"""
        back_btns = self.page.get_elements("image, .back-btn, view[text='返回']")
        if back_btns:
            back_btns[0].click()
            self.logger.info("已点击返回按钮")
        else:
            self.app.navigate_back()
            self.logger.info("navigate_back")