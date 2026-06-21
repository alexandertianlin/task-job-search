
# Skill: Camera Calibration (相机标定)

> 提供 ChArUco 板标定、立体外参标定功能。

---

## 功能

- ChArUco 板检测
- 单目相机内参标定
- 双目立体外参标定
- 标定结果保存/加载

## 接口

```python
class CameraCalibrator:
    def detect_charuco(image: np.ndarray, board: CharucoBoard) -> DetectionResult
    def calibrate_intrinsic(images: List[np.ndarray], board: CharucoBoard) -> CameraMatrix
    def calibrate_stereo(left_images, right_images, board) -> StereoParams
```

## 依赖

- opencv-python >= 4.8.0 (contrib)
- numpy >= 1.24.0

## 使用方式

在 `_TASK_SPEC.md` 的 Skills 声明一段引用此 skill。

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-06-10 | 初始版本，基础标定功能 |

---

> **最后更新**: 2026-06-10
