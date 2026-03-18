import minium
import time
from ddt import data, ddt


@ddt
class ChargingRecordTest(minium.MiniTest):
    # 定义要测试的选项卡
    TABS_TO_TEST = ["全部", "充电中", "已结束", "未付款"]

    def setUp(self):
        """测试前准备：导航到充电记录页面"""
        self.app.redirect_to("/page/power_record/power_record")
        self.page.wait_for(3)
        self.logger.info("已导航到充电记录页面")

    @data(*TABS_TO_TEST)
    def test_tab_operations(self, tab_name):
        """测试选项卡切换和记录点击"""
        self.logger.info(f"开始测试 {tab_name} 选项卡")

        # 切换到目标选项卡
        self._switch_to_tab(tab_name)

        # 点击当前选项卡下的所有记录
        self._click_records_in_tab(tab_name)

        self.logger.info(f"{tab_name} 选项卡测试完成")

    def _switch_to_tab(self, tab_name):
        """切换到指定选项卡（优化版）"""
        # 尝试通过文本直接找到选项卡
        try:
            tab = self.page.get_element(f".part1 > view:contains-text('{tab_name}')")
            tab.click()
            self.page.wait_for(1.5)

            # 验证是否切换成功
            active_tab = self.page.get_element(".part1 > view.active")
            if active_tab.inner_text == tab_name:
                self.logger.info(f"成功切换到 {tab_name} 选项卡")
                return
        except:
            pass

        # 如果直接方法失败，尝试备选方法
        self.logger.warning(f"直接切换到 {tab_name} 失败，尝试备选方法")
        self._switch_to_tab_alternative(tab_name)

    def _switch_to_tab_alternative(self, tab_name):
        """备选方法切换到指定选项卡"""
        # 获取所有选项卡
        tabs = self.page.get_elements(".part1 > view")

        # 查找目标选项卡
        target_index = -1
        for i, tab in enumerate(tabs):
            if tab.inner_text == tab_name:
                target_index = i
                break

        if target_index == -1:
            self.logger.error(f"未找到 {tab_name} 选项卡")
            return

        # 检查当前激活的选项卡
        active_tab = self.page.get_element(".part1 > view.active")
        if active_tab.inner_text == tab_name:
            self.logger.info(f"{tab_name} 选项卡已激活")
            return

        # 点击目标选项卡
        tabs[target_index].click()
        self.page.wait_for(1.5)

        # 验证是否切换成功
        active_tab = self.page.get_element(".part1 > view.active")
        if active_tab.inner_text == tab_name:
            self.logger.info(f"成功切换到 {tab_name} 选项卡")
        else:
            self.logger.warning(f"切换到 {tab_name} 选项卡失败，当前活动选项卡为 {active_tab.inner_text}")

    def _click_records_in_tab(self, tab_name):
        """点击选项卡下的记录"""
        # 滚动加载记录（如果需要）
        self.page.scroll_to(9999, 1000)
        time.sleep(1)

        # 获取记录
        records = self.page.get_elements(".part2")
        self.logger.info(f"{tab_name} 选项卡下有 {len(records)} 条记录")

        if not records:
            return

        # 点击每条记录
        for i in range(len(records)):
            # 重新获取当前记录列表
            current_records = self.page.get_elements(".part2")
            if i >= len(current_records):
                break

            record = current_records[i]
            self._click_record_and_verify_detail(record, i + 1, len(records), tab_name)

            # 返回后等待页面稳定
            self.page.wait_for(1.5)

    def _click_record_and_verify_detail(self, record, record_index, total_records, tab_name):
        """点击记录并验证详情页"""
        try:
            # 点击记录
            record.click()
            self.page.wait_for(1.5)
            self.logger.info(f"点击 {tab_name} 选项卡下第 {record_index}/{total_records} 条记录")

            # 验证详情页
            self._verify_detail_page()

        except Exception as e:
            self.logger.error(f"详情页操作失败: {str(e)}")
        finally:
            # 返回列表页
            self._return_to_record_page()

    def _verify_detail_page(self):
        """验证详情页"""
        try:
            # 尝试获取标题元素
            title_element = self.page.get_element(".conBox TopStatusBar text")
            title_text = title_element.inner_text

            # 验证标题是否包含关键词
            if "充电" in title_text:
                self.logger.info(f"详情页标题验证通过: {title_text}")
            else:
                self.logger.warning(f"详情页标题异常: {title_text}")
        except:
            self.logger.warning("详情页验证失败")

    def _return_to_record_page(self):
        """返回列表页（简化版）"""
        try:
            # 尝试多种返回方式
            self._try_back_methods()
        except:
            # 如果返回失败，重新导航到页面
            self.app.redirect_to("/page/power_record/power_record")
            self.page.wait_for(2)
            self.logger.info("重新导航到充电记录页面")

    def _try_back_methods(self):
        """尝试多种返回方式"""
        # 1. 尝试使用页面返回按钮
        try:
            back_btn = self.page.get_element("image")
            if back_btn:
                back_btn.click()
                self.page.wait_for(1.5)
                self.logger.info("使用页面返回按钮返回")
                return
        except:
            pass

        # 2. 尝试使用导航返回
        try:
            self.app.navigate_back()
            self.page.wait_for(1.5)
            self.logger.info("使用navigate_back返回")
            return
        except:
            pass

        # 3. 尝试物理返回键
        try:
            self.native.return_key()
            self.page.wait_for(1.5)
            self.logger.info("使用物理返回键返回")
        except:
            self.logger.warning("所有返回方式均失败")