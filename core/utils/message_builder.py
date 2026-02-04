import json
from typing import List, Dict, Any, Optional
from astrbot import logger


class MessageBuilder:


    @staticmethod
    def create_text_event(
        text: str,
        color: str = "white",
        bold: bool = False,
        italic: bool = False,
        underlined: bool = False,
        strikethrough: bool = False,
        obfuscated: bool = False,
        font: Optional[str] = None,
        insertion: Optional[str] = None
    ) -> Dict[str, Any]:
        component = {
            "text": text,
            "color": color,
            "bold": bold,
            "italic": italic,
            "underlined": underlined,
            "strikethrough": strikethrough,
            "obfuscated": obfuscated
        }

        if font:
            component["font"] = font
        if insertion:
            component["insertion"] = insertion

        return component

    @staticmethod
    def add_hover_event(
        component: Dict[str, Any],
        hover_text: str,
        hover_color: str = "aqua",
        hover_bold: bool = True
    ) -> Dict[str, Any]:
        component["hoverEvent"] = {
            "action": "show_text",
            "contents": {
                "text": hover_text,
                "color": hover_color,
                "bold": hover_bold
            }
        }
        return component

    @staticmethod
    def add_click_event(
        component: Dict[str, Any],
        click_value: str,
        click_action: str = "OPEN_URL"
    ) -> Dict[str, Any]:
        action = click_action.lower()
        component["clickEvent"] = {
            "action": action,
            "value": click_value
        }
        return component

    @staticmethod
    def create_broadcast_message(components: List[Dict[str, Any]]) -> Dict[str, Any]:

        if not components:
            raise ValueError("components 不能为空")

        root = components[0]
        if len(components) > 1:
            root["extra"] = components[1:]

        return {
            "api": "broadcast",
            "data": {
                "message": root
            }
        }

    @staticmethod
    def create_private_message(
        uuid: str,
        component: Dict[str, Any],
        nickname: str = ""
    ) -> Dict[str, Any]:
        return {
            "api": "send_private_msg",
            "data": {
                "uuid": uuid,
                "nickname": nickname,
                "message": component
            },
            "echo": "1"
        }

    @staticmethod
    def create_simple_broadcast(message: str, sender: str = None) -> Dict[str, Any]:
        text = f"{sender}: {message}" if sender else message
        component = MessageBuilder.create_text_event(text)
        return MessageBuilder.create_broadcast_message([component])

    @staticmethod
    def create_rich_broadcast(
        text: str,
        color: str = "#E6E6FA",
        bold: bool = False,
        click_url: str = "",
        hover_text: str = "",
        images: List[str] = None,
        click_action: str = "OPEN_URL"
    ) -> Dict[str, Any]:
        components = [
            MessageBuilder.create_text_event(text, color=color, bold=bold)
        ]

        main = components[0]

        if hover_text:
            MessageBuilder.add_hover_event(main, hover_text, "gold", True)

        if click_url:
            MessageBuilder.add_click_event(main, click_url, click_action)

        if images:
            for image_url in images:
                if not image_url:
                    continue
                img = MessageBuilder.create_text_event(
                    f" [图片]",
                    color="gray",
                    underlined=True
                )
                MessageBuilder.add_click_event(img, image_url, "OPEN_URL")
                components.append(img)

        return MessageBuilder.create_broadcast_message(components)

    @staticmethod
    def create_admin_announcement(
        text: str,
        click_value: str = "",
        hover_text: str = "",
        click_action: str = "SUGGEST_COMMAND"
    ) -> Dict[str, Any]:
        components = []

        prefix = MessageBuilder.create_text_event(
            "[管理员公告] ",
            color="red",
            bold=True
        )
        components.append(prefix)

        main = MessageBuilder.create_text_event(text)

        if hover_text:
            MessageBuilder.add_hover_event(main, hover_text, "gold", True)

        if click_value:
            MessageBuilder.add_click_event(main, click_value, click_action)

        components.append(main)

        return MessageBuilder.create_broadcast_message(components)

    @staticmethod
    def log_message(message: Dict[str, Any], message_type: str = "消息"):
        logger.debug(
            f"发送的{message_type}: {json.dumps(message, ensure_ascii=False)}"
        )
