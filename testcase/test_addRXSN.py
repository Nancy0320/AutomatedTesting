import minium
from ddt import data
import time

shouldSkip = True


@minium.ddt_class
class AddVehicleNumberTest(minium.MiniTest):
    @data(*range(1))
    def test_add(self, test_num):
        """
        添加车辆编号并解绑车辆
        """
        try:
            self.logger.info(f"开始第 {test_num + 1} 次测试")

            # 1. 返回首页
            self._click_element("image", "返回按钮", timeout=5)

            # 2. 绑定设备流程
            self._bind_device()

            # 3. 选择车辆信息
            self._select_vehicle_info()

            # 4. 查看并解绑车辆
            self._unbind_vehicle()

            self.logger.info(f"成功完成第 {test_num + 1} 次测试")

        except Exception as e:
            self.logger.error(f"第 {test_num + 1} 次测试失败: {str(e)}")
            # 使用其他方式获取页面信息
            try:
                self.logger.debug("当前页面截图已保存")
                self.capture("error_screenshot.png")  # 保存截图代替native
            except:
                pass
            raise

    def _click_element(self, selector, element_name, timeout=10, **kwargs):
        """封装点击操作，添加等待和重试"""
        self.page.wait_for(selector, max_timeout=timeout)

        # 处理inner_text的情况
        if "inner_text" in kwargs:
            elements = self.page.get_elements(selector)
            for element in elements:
                if element.inner_text == kwargs["inner_text"]:
                    element.click()
                    time.sleep(0.5)
                    return element
            raise Exception(f"未找到{element_name}: {selector} with text {kwargs['inner_text']}")
        else:
            element = self.page.get_element(selector)
            if not element:
                raise Exception(f"未找到{element_name}: {selector}")
            element.click()
            time.sleep(0.5)
            return element

    def _bind_device(self):
        """绑定设备流程"""
        self.logger.info("开始绑定设备流程")

        # 等待绑定按钮容器
        self.page.wait_for(".bind_Button", max_timeout=10)

        # 查找所有.bind_device元素，然后通过文本过滤
        bind_devices = self.page.get_elements(".bind_device")
        target_device = None
        for device in bind_devices:
            if device.inner_text == "绑定设备充电":
                target_device = device
                break

        if not target_device:
            raise Exception("未找到'绑定设备充电'按钮")

        target_device.click()

        # 输入设备编号
        input_ele = self._click_element("input.input_text", "设备编号输入框")
        input_ele.input("924010604")

        # 确认添加
        self._click_element(".bind-btn", "确认添加按钮", inner_text="确认添加")
        self.logger.info("设备绑定成功")

    def _select_vehicle_info(self):
        """选择车辆信息"""
        self.logger.info("开始选择车辆信息")

        # 选择款式
        self._click_element("view", "电动自行车选项", inner_text="电动自行车")

        # 选择品牌
        self._click_element("view", "凤凰品牌", inner_text="凤凰")

        # 选择型号
        self._click_element("view", "型号1", inner_text="型号1")

        # 确认添加
        self._click_element(".confirm_btn", "确定添加按钮", inner_text="确定添加")
        self.logger.info("车辆信息选择完成")

    def _unbind_vehicle(self):
        """解绑车辆流程"""
        self.logger.info("开始解绑车辆流程")

        # 查看详情
        self._click_element(".slide5", "查看详情按钮", inner_text="查看详情")

        # 解绑车辆
        self._click_element(".unbind_btn", "我要解绑按钮", inner_text="我要解绑")

        # 确认解绑
        self._click_element(".unbind2", "解绑确认按钮", inner_text="确定")
        self.logger.info("车辆解绑成功")