import minium
import time


class AddVehicleNumberTest(minium.MiniTest):
    def test_add(self):
        self.logger.info("开始测试")
        try:
            # 1. 返回首页
            self._safe_click("image", "返回按钮", timeout=10)
            self.app.wait_for_page("/page/index/index")

            # 2. 绑定设备流程
            self._bind_device()

            # 3. 选择车辆信息
            self._select_vehicle_info()

            # 4. 查看并解绑车辆
            self._unbind_vehicle()

            self.logger.info("测试成功完成")
        except Exception as e:
            self.logger.error(f"测试失败: {str(e)}")
            self.capture("error.png")
            raise

    def _safe_click(self, selector, element_name, text=None, timeout=15):
        """高效元素点击方法"""
        try:
            # 构建精确选择器
            exact_selector = f'{selector}:text("{text}")' if text else selector
            element = self.page.wait_for(exact_selector, max_timeout=timeout)
            element.click()

            # 短暂等待操作生效
            self.page.wait_for(0.3)
            return True
        except:
            self.logger.warning(f"点击{element_name}失败")
            return False

    def _bind_device(self):
        self.logger.info("绑定设备")
        btn = self.page.get_element(".bind_device", inner_text="绑定设备充电")
        btn.click()

        # 直接定位绑定按钮
        if not btn:
            raise Exception("绑定设备按钮未找到")

        # 一步完成输入框操作
        input_ele = self.page.get_element("input.input_text")
        input_ele.input("924010604")

        # 确认添加
        btn2 = self.page.get_element(".bind-btn", inner_text="确认添加")
        btn.click()

        if not btn2:
            raise Exception("确认添加按钮未找到")

        # 等待绑定完成 - 检查绑定成功元素
        # self.page.wait_for(".bind-success", max_timeout=15)

    def _select_vehicle_info(self):
        self.logger.info("选择车辆信息")

        # 确保在正确页面
        # 等待选择区域加载
        # self.page.wait_for(".selection-area", max_timeout=10)

        # 快速选择选项
        self._safe_click("view", "电动自行车", "电动自行车")
        self._safe_click("view", "凤凰", "凤凰")
        self._safe_click("view", "型号1", "型号1")

        # 确认添加
        self._safe_click(".confirm_btn", "确定添加", "确定添加")

        # 等待信息保存
        self.page.wait_for(".save-success", max_timeout=10)

    def _unbind_vehicle(self):
        self.logger.info("解绑车辆")

        # 确保在车辆管理页面

        # 使用条件等待替代固定等待
        # self.app.wait_util(
        #     lambda: self.page.element_is_exists(".slide5"),
        #     max_timeout=15
        # )

        # 快速完成解绑流程
        self._safe_click(".slide5", "查看详情", "查看详情")
        self._safe_click(".unbind_btn", "我要解绑", "我要解绑")
        self._safe_click(".unbind2", "确定", "确定")

        # 等待解绑完成
        self.page.wait_for(".unbind-success", max_timeout=15)
