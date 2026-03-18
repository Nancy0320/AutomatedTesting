import minium
import time
from ddt import data, ddt


@ddt
class ChargingRecordTest(minium.MiniTest):
    TABS_TO_TEST = ["全部", "充电中", "已结束", "未付款"]

    def setUp(self):
        """导航到充电记录页面"""
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
        # 根据选项卡名称映射到对应的 data-status 值
        tab_mapping = {
            "全部": {"status": 0, "pay_status": 0},
            "充电中": {"status": 2, "pay_status": 0},
            "已结束": {"status": 3, "pay_status": 0},
            "未付款": {"status": 0, "pay_status": 1}
        }

        # 获取目标选项卡的 data 属性值
        target_data = tab_mapping.get(tab_name)
        if not target_data:
            self.logger.warning(f"未找到 {tab_name} 选项卡的映射配置")
            return

        # 使用 data-status 和 data-pay_status 定位选项卡
        selector = f".part1 > view[data-status='{target_data['status']}'][data-pay_status='{target_data['pay_status']}']"

        try:
            tab = self.page.get_element(selector)
            tab.click()
            self.page.wait_for(1.5)

            # 验证是否激活
            active_class = tab.attribute("class")[0]
            if "active" in active_class:
                self.logger.info(f"成功切换到 {tab_name} 选项卡")
                return True
            else:
                self.logger.warning(f"切换到 {tab_name} 但未激活")
                return False
        except:
            self.logger.warning(f"使用选择器 {selector} 未找到 {tab_name} 选项卡")
            return False

    def _click_records_in_tab(self, tab_name):
        """点击选项卡下的记录"""
        # 滚动加载记录
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
            self.page.wait_for(2)
            self.logger.info(f"点击 {tab_name} 选项卡下第 {record_index}/{total_records} 条记录")

            # 验证详情页
            self._verify_detail_page()

        except minium.framework.exception.PageDestroyed:
            self.logger.warning("详情页已销毁，重新导航")
            self.app.redirect_to("/page/power_record/power_record")
            self.page.wait_for(2)
        except Exception as e:
            self.logger.error(f"详情页操作失败: {str(e)}")
        finally:
            # 返回列表页
            self._return_to_record_page()

    def _verify_detail_page(self):
        """验证详情页"""
        try:
            # 尝试获取标题元素
            title_element = self.page.get_element(".TopStatusBar text")
            title_text = title_element.inner_text

            # 验证标题是否包含关键词
            if "充电" in title_text:
                self.logger.info(f"详情页标题验证通过: {title_text}")
                return True
            else:
                self.logger.warning(f"详情页标题异常: {title_text}")
                return False
        except:
            self.logger.warning("详情页验证失败")
            return False

    def _return_to_record_page(self):
        """返回列表页"""
        # 尝试多种返回方式
        self._try_back_methods()

        # 验证是否回到记录页
        self.page.wait_for(1.5)
        if not self.page.path.endswith("/power_record/power_record"):
            self.logger.warning("未返回充电记录页，尝试重定向")
            self.app.redirect_to("/page/power_record/power_record")
            self.page.wait_for(2)

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