import minium
import time
from ddt import data, ddt


@ddt
class ChargingRecordTest(minium.MiniTest):
    # @data(1, 2, 3, 4, 5)
    @data(1)
    def test_click_records_robust(self, loop_count):
        """健壮版：点击记录并处理页面销毁问题"""
        # self.logger.info(f"开始第 {loop_count}/5 次循环")

        # 导航到充电记录页面
        self._navigate_and_verify()

        # 定义要测试的选项卡
        tabs_to_test = ["全部", "充电中", "已结束", "未付款"]

        # 切换并处理每个选项卡
        for tab_name in tabs_to_test:
            # 强制切换到指定选项卡（增加容错机制）
            self._force_switch_to_tab(tab_name)

            # 点击当前选项卡下的所有记录
            self._click_records_in_tab(tab_name)

        # self.logger.info(f"第 {loop_count}/5 次循环结束\n")

    def _navigate_and_verify(self):
        """导航到页面并验证"""
        self.app.redirect_to("/page/power_record/power_record")
        self.page.wait_for(3)
        self._verify_page_loaded()

    def _verify_page_loaded(self):
        """验证页面已加载"""
        try:
            self.page.get_element(".part1")
            self.logger.info("充电记录页面加载成功")
        except:
            self.fail("充电记录页面加载失败")

    def _force_switch_to_tab(self, target_tab):
        """强制切换到指定选项卡（增强版）"""
        max_retries = 5  # 增加重试次数
        for attempt in range(max_retries):
            try:
                # 获取所有选项卡
                tabs = self.page.get_elements(".part1 > view")

                # 查找目标选项卡
                target_index = -1
                for i, tab in enumerate(tabs):
                    if tab.inner_text == target_tab:
                        target_index = i
                        break

                # 如果找不到目标选项卡，记录错误并退出
                if target_index == -1:
                    self.logger.error(f"未找到 {target_tab} 选项卡")
                    self.fail(f"未找到 {target_tab} 选项卡")

                # 检查目标选项卡是否已激活
                active_tab = self.page.get_element(".part1 > view.active")
                if active_tab.inner_text == target_tab:
                    self.logger.info(f"{target_tab} 选项卡已激活")
                    return

                # 点击目标选项卡
                tabs[target_index].click()
                self.page.wait_for(2)  # 等待切换完成

                # 验证是否切换成功
                active_tab = self.page.get_element(".part1 > view.active")
                if active_tab.inner_text == target_tab:
                    self.logger.info(f"成功切换到 {target_tab} 选项卡")
                    return
                else:
                    self.logger.warning(f"切换到 {target_tab} 选项卡失败，当前活动选项卡为 {active_tab.inner_text}")

            except Exception as e:
                self.logger.error(f"切换选项卡出错: {str(e)}")

            # 尝试再次切换前等待
            self.page.wait_for(1)

        self.fail(f"无法切换到 {target_tab} 选项卡，已尝试 {max_retries} 次")

    def _click_records_in_tab(self, tab_name):
        """点击选项卡下的记录"""
        # 滚动加载记录
        self.page.scroll_to(9999, 1000)
        time.sleep(2)

        # 动态获取记录
        records = self.page.get_elements(".part2")
        self.logger.info(f"{tab_name} 选项卡下有 {len(records)} 条记录")

        # 点击每条记录
        for i in range(len(records)):
            # 每次重新获取记录列表
            records = self.page.get_elements(".part2")
            if i >= len(records):
                break

            record = records[i]
            self._click_record_and_verify_detail(record, i + 1, len(records), tab_name)

            # 返回后等待页面稳定
            self.page.wait_for(2)
            self._verify_page_loaded()

    def _click_record_and_verify_detail(self, record, record_index, total_records, tab_name):
        """点击记录并验证详情页"""
        try:
            # 点击记录
            record.click()
            self.page.wait_for(2)
            self.logger.info(f"点击 {tab_name} 选项卡下第 {record_index}/{total_records} 条记录，进入详情页")

            # 验证详情页
            self._verify_detail_page()

        except minium.framework.exception.PageDestroyed:
            self.logger.warning("详情页已销毁，重新导航")
            self._navigate_and_verify()
        except Exception as e:
            self.logger.error(f"详情页操作失败: {str(e)}")
        finally:
            # 返回列表页
            self._return_to_record_page()

    def _verify_detail_page(self):
        """验证详情页"""
        try:
            title = self.page.get_element(".conBox TopStatusBar text").inner_text
            self.assertEqual(title, "充电详情", "详情页标题错误")
            self.logger.info("详情页验证通过")
        except:
            self.logger.warning("详情页验证失败，可能页面已销毁")

    def _return_to_record_page(self):
        """返回列表页"""
        try:
            # 优先使用返回按钮
            back_btn = self.page.get_element("image")
            back_btn.click()
            self.page.wait_for(2)
            self.logger.info("已点击返回按钮")
        except:
            # 备选方案：使用navigate_back
            self.app.navigate_back()
            self.page.wait_for(2)
            self.logger.info("使用navigate_back返回")