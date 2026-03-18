import minium

import time

shouldSkip = True


class AddVehicleNumberTest(minium.MiniTest):
    def test_click_all_messages(self):
        """测试循环点击所有消息数据（动态获取数量）"""
        try:
            # 导航到消息列表页
            self.app.redirect_to("/page/message_list/message_list")
            self.page.wait_for(2)

            # 等待消息列表加载完成
            self._wait_for_element(".part3", max_timeout=10)

            # 获取所有消息项
            message_items = self.page.get_elements(".part3")
            total_messages = len(message_items)

            self.logger.info(f"当前页面有 {total_messages} 条消息")

            # 验证是否有消息数据
            if total_messages == 0:
                self.logger.warning("当前没有消息数据")
                return

            # 循环点击每条消息
            for index in range(total_messages):
                try:
                    self.logger.info(f"点击第 {index + 1}/{total_messages} 条消息")

                    # 重新获取消息列表，避免元素引用失效
                    message_items = self.page.get_elements(".part3")
                    if index >= len(message_items):
                        self.logger.warning(f"索引 {index + 1} 超出当前消息列表范围")
                        break

                    item = message_items[index]

                    # 滚动到元素位置确保可见
                    self._scroll_to_element(item)
                    self.page.wait_for(0.5)

                    # 点击消息项（增加重试机制）
                    self._click_with_retry(item, max_retries=3)
                    self.page.wait_for(2)
                    self.page.scroll_to(700, 2000)

                    # 在消息详情页执行操作
                    self._verify_message_detail(index + 1, total_messages)

                    # 滚动详情页
                    self._scroll_message_detail()

                    # 返回消息列表页
                    self._click_back_button()
                    self.page.wait_for(2)

                except Exception as e:
                    self.logger.error(f"处理第 {index + 1} 条消息失败: {str(e)}")
                    # 继续执行下一条，不中断测试
                    continue

        except Exception as e:
            self.logger.error(f"测试失败: {str(e)}")
            raise

    def _verify_message_detail(self, current_index, total_messages):
        """验证消息详情页内容"""
        try:
            # 等待详情页加载
            self._wait_for_element(".title", max_timeout=5)

            # 获取并验证标题
            title = self.page.get_element(".title").inner_text
            self.logger.info(f"消息 {current_index}/{total_messages} 标题: {title}")

            # 获取并验证发布时间
            time_text = self.page.get_element(".time").inner_text
            self.logger.info(f"发布时间: {time_text}")

            # 验证内容区域
            if self.page.get_elements(".content"):
                self.logger.info("内容区域存在")

        except Exception as e:
            self.logger.error(f"验证消息详情失败: {str(e)}")
            raise

    def _scroll_message_detail(self, steps=10, wait_time=0.3):
        """滚动消息详情页从顶部到底部"""
        try:
            # 获取页面元素
            page = self.page.get_element("page")
            content = self.page.get_element(".conBox")

            if not page or not content:
                self.logger.warning("未找到页面或内容元素，无法滚动")
                return

            # 正确调用 bounding_client_rect() 方法获取元素尺寸
            page_rect = page.bounding_client_rect()
            content_rect = content.bounding_client_rect()

            page_height = page_rect["height"]
            content_height = content_rect["height"]

            # 如果内容高度小于页面高度，无需滚动
            if content_height <= page_height:
                self.logger.info("内容无需滚动")
                return

            # 计算每步滚动距离
            step_distance = (content_height - page_height) / steps

            # 执行滚动
            for i in range(steps):
                scroll_y = (i + 1) * step_distance
                self.page.scroll_to(0, scroll_y)
                self.page.wait_for(wait_time)
                self.logger.info(f"滚动进度: {int((i + 1) / steps * 100)}%")

            self.logger.info("详情页滚动完成")

        except Exception as e:
            self.logger.warning(f"滚动详情页失败: {str(e)}")
            # 尝试备用方法
            self._scroll_alternative()

    def _scroll_alternative(self):
        """备用滚动方法：使用touch操作模拟手指滑动"""
        try:
            # 获取屏幕中点坐标
            screen_width = self.page.get_element("page").bounding_client_rect()["width"]
            screen_height = self.page.get_element("page").bounding_client_rect()["height"]

            start_x = screen_width / 2
            start_y = screen_height * 0.8
            end_y = screen_height * 0.2

            # 模拟手指向下滑动多次
            for i in range(3):
                self.page.touch_action([
                    {"action": "press", "x": start_x, "y": start_y},
                    {"action": "moveTo", "x": start_x, "y": end_y},
                    {"action": "release"}
                ])
                self.page.wait_for(1)

        except Exception as e:
            self.logger.error(f"备用滚动方法也失败: {str(e)}")

    def _click_back_button(self):
        """点击返回按钮（增加重试机制）"""
        try:
            # 尝试通过image标签定位
            back_btn = self.page.get_elements("image")
            if back_btn:
                back_btn[0].click()
                return

            # 尝试通过文本定位
            back_btn = self.page.get_elements("view", inner_text="返回")
            if back_btn:
                back_btn[0].click()
                return

            # 尝试通过class定位
            back_btn = self.page.get_elements(".back-btn")
            if back_btn:
                back_btn[0].click()
                return

            self.logger.warning("未找到返回按钮，尝试使用navigateBack")
            # 直接调用navigateBack
            self.app.navigateBack()

        except Exception as e:
            self.logger.error(f"点击返回按钮失败: {str(e)}")
            # 尝试备用方法
            self.app.navigateBack()

    def _wait_for_element(self, selector, max_timeout=10):
        """兼容版本的元素等待方法"""
        try:
            # 尝试新版本方法
            self.page.wait_for(selector, max_timeout=max_timeout)
        except Exception as e:
            self.logger.warning(f"wait_for 失败: {str(e)}")
            # 尝试旧版本方法
            try:
                self.page.wait_for(selector, max_timeout=max_timeout)
            except Exception as e2:
                self.logger.error(f"所有等待方法均失败: {str(e2)}")
                raise

    def _scroll_to_element(self, element):
        """滚动到元素位置"""
        try:
            # 尝试使用 scroll_into_view
            self.page.scroll_into_view(element)
        except Exception as e:
            self.logger.warning(f"scroll_into_view 失败: {str(e)}")
            # 手动计算滚动位置
            try:
                # 正确调用 bounding_client_rect() 获取元素位置
                rect = element.bounding_client_rect()
                # 滚动到元素顶部位置，加上一些偏移确保元素完全可见
                self.page.scroll_to(0, rect["top"] - 100)
            except Exception as e2:
                self.logger.error(f"手动滚动也失败: {str(e2)}")
                # 最后尝试使用 touch_action 滑动到元素
                self._scroll_to_element_touch(element)

    def _scroll_to_element_touch(self, element):
        """使用 touch_action 滑动到元素位置（最后的备选方案）"""
        try:
            # 获取屏幕尺寸
            screen_width = self.page.get_element("page").bounding_client_rect()["width"]
            screen_height = self.page.get_element("page").bounding_client_rect()["height"]

            # 获取元素位置
            element_rect = element.bounding_client_rect()
            element_y = element_rect["top"]

            # 如果元素已经可见，不需要滚动
            if element_y >= 0 and element_y < screen_height:
                return

            # 计算滑动方向和距离
            start_y = screen_height * 0.8
            end_y = screen_height * 0.2

            # 计算需要滑动的次数
            scroll_times = min(5, int(element_y / screen_height) + 1)

            for i in range(scroll_times):
                self.page.touch_action([
                    {"action": "press", "x": screen_width / 2, "y": start_y},
                    {"action": "moveTo", "x": screen_width / 2, "y": end_y},
                    {"action": "release"}
                ])
                self.page.wait_for(0.5)

                # 检查元素是否已经可见
                element_rect = element.bounding_client_rect()
                if element_rect["top"] >= 0 and element_rect["top"] < screen_height:
                    break

        except Exception as e:
            self.logger.error(f"touch 滚动到元素失败: {str(e)}")

    def _click_with_retry(self, element, max_retries=3):
        """带重试机制的点击操作"""
        for attempt in range(max_retries):
            try:
                element.click()
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"点击失败，重试 ({attempt + 1}/{max_retries}): {str(e)}")
                    self.page.wait_for(1)
                else:
                    raise