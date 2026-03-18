import minium

class AddVehicleNumberTest(minium.MiniTest):
    def test_click_all_messages(self):
        """测试循环点击所有消息数据"""
        # 导航到消息列表页
        self.app.redirect_to("/page/message_list/message_list")
        self.page.wait_for(2)

        # 获取所有消息项
        messages = self.page.get_elements(".part3")
        total = len(messages)
        self.logger.info(f"当前有 {total} 条消息")

        if total == 0:
            return

        # 循环点击每条消息
        for i in range(total):
            # 重新获取元素避免失效
            item = self.page.get_elements(".part3")[i]
            item.click()
            self.page.wait_for(1)

            # 滑动详情页（固定值滚动）
            # self.page.scroll_to(700, 2000)
            self.page.wait_for(1)

            # 验证详情页
            title = self.page.get_element(".title").inner_text
            self.logger.info(f"消息 {i+1} 标题: {title}")

            # 返回列表页
            self.page.get_element("image").click()
            self.page.wait_for(1)