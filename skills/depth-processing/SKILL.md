
# Skill: Depth Processing (深度处理)

> 提供 Orbbec Astra Plus 深度图像的采集、处理和分析能力。

---

## 功能

- 深度图获取（双摄像头源）
- 深度图预处理（滤波、孔洞填充）
- 点云生成
- 深度与 RGB 对齐

## 接口

```python
class DepthProcessor:
    def get_depth_frame(source: int) -> np.ndarray
    def filter_depth(depth: np.ndarray) -> np.ndarray
    def depth_to_pointcloud(depth: np.ndarray, intrinsic: CameraMatrix) -> PointCloud
```

## 依赖

- open3d >= 0.17.0
- opencv-python >= 4.8.0
- numpy >= 1.24.0

## 使用方式

在 `_TASK_SPEC.md` 的 Skills 声明一段引用此 skill。

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-06-05 | 初始版本，基础深度处理 |

---

> **最后更新**: 2026-06-05
