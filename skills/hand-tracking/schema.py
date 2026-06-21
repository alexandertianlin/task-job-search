
"""Hand Tracking Skill — Pydantic Input/Output Schema"""

from pydantic import BaseModel, Field
from typing import Optional, List


class HandTrackingInput(BaseModel):
    image_path: str = Field(description="输入图像文件的路径")
    max_hands: int = Field(default=2, ge=1, le=10, description="最大检测手数")
    min_detection_confidence: float = Field(
        default=0.5, ge=0.0, le=1.0, description="最小检测置信度"
    )
    return_3d: bool = Field(default=False, description="是否返回 3D 关键点")


class HandLandmark(BaseModel):
    x: float = Field(description="归一化 x 坐标 [0, 1]")
    y: float = Field(description="归一化 y 坐标 [0, 1]")
    z: Optional[float] = Field(default=None, description="归一化 z 深度 [0, 1]")
    visibility: float = Field(default=1.0, ge=0.0, le=1.0, description="关键点可见度")


class HandResult(BaseModel):
    hand_id: int = Field(description="手部编号 (0 开始)")
    handedness: str = Field(description="左手/右手")
    landmarks_21: List[HandLandmark] = Field(description="21 个手部关键点")
    landmarks_3d: Optional[List[HandLandmark]] = Field(default=None, description="3D 关键点")
    confidence: float = Field(description="检测置信度")


class HandTrackingOutput(BaseModel):
    success: bool = Field(description="调用是否成功")
    num_hands: int = Field(default=0, description="检测到的手部数量")
    hands: List[HandResult] = Field(default_factory=list, description="手部检测结果列表")
    annotated_image_path: Optional[str] = Field(default=None, description="标注后的图像路径")
    error: Optional[str] = Field(default=None, description="错误信息（若失败）")
    latency_ms: float = Field(default=0.0, description="处理耗时（毫秒）")
