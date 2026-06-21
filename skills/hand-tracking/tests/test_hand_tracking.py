
"""Hand Tracking Skill — 单元测试"""

import pytest
from ..schema import HandTrackingInput, HandTrackingOutput
from ..impl import execute


def test_execute_invalid_path():
    """测试无效图像路径"""
    args = HandTrackingInput(image_path="/nonexistent/image.jpg")
    result = execute(args)
    assert result.success is False
    assert "无法读取" in result.error


def test_execute_input_validation():
    """测试输入参数校验"""
    args = HandTrackingInput(
        image_path="test.jpg",
        max_hands=2,
        min_detection_confidence=0.5,
        return_3d=False,
    )
    assert args.max_hands == 2
    assert args.return_3d is False


def test_execute_output_schema():
    """测试输出结构完整性"""
    args = HandTrackingInput(image_path="test.jpg")
    result = execute(args)
    assert isinstance(result, HandTrackingOutput)
    assert hasattr(result, "success")
    assert hasattr(result, "latency_ms")
    assert result.latency_ms >= 0
