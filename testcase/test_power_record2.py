import minium
import time

from ddt import data, ddt


@ddt
class ChargingRecordTest(minium.MiniTest):
    @data(1, 2, 3, 4, 5)
    def test_switch_tabs(self, loop_count):
        """使用DDT循环执行五次（修正参数位置）"""
        self.logger.info(f"开始第 {loop_count}/5 次循环")

        # 导航到充电记录页面
        self.app.redirect_to("/page/power_record/power_record")
        self.page.wait_for(3)
        self.logger.info("已导航到充电记录页面")

        # 获取所有选项卡元素
        tab_elements = self.page.get_elements(".part1 > view")
        actual_count = len(tab_elements)
        self.logger.info(f"实际找到 {actual_count} 个选项卡")

        # 定义预期选项卡
        expected_tabs = ["全部", "充电中", "已结束", "未付款"]
        expected_count = len(expected_tabs)
        self.logger.info(f"预期 {expected_count} 个选项卡，实际 {actual_count} 个")

        # 切换并验证每个选项卡
        for i in range(actual_count):
            tab_name = tab_elements[i].inner_text
            self._switch_and_verify_tab(i, tab_name, tab_elements)

        self.logger.info(f"第 {loop_count}/5 次循环结束\n")

    def _switch_and_verify_tab(self, tab_index, tab_name, tab_elements):
        """切换并验证单个选项卡"""
        # 点击选项卡
        tab_elements[tab_index].click()
        self.page.wait_for(1.5)
        self.logger.info(f"已切换到 {tab_name} 选项卡")

        # 验证选项卡激活状态
        active_tab = self.page.get_element(".part1 > view.active")
        self.assertIsNotNone(active_tab, "未找到激活的选项卡")
        self.assertEqual(active_tab.inner_text, tab_name, "选项卡激活错误")

        # 滚动查看记录
        self.page.scroll_to(9999, 1000)  # 垂直滚动9999px，持续1000ms
        time.sleep(1.5)

        # 计数记录
        records = self.page.get_elements(".part2")
        self.logger.info(f"{tab_name} 选项卡下有 {len(records)} 条记录")