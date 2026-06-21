
# Skill: Hand Tracking (手势追踪)

> 提供基于 MediaPipe / 自定义模型的手部 21 关键点检测能力。

---

## 功能

- 2D 手部关键点检测 (21 keypoints)
- 3D 手部关键点检测
- 多手同时追踪

## 接口

```python
class HandTracker:
    def detect_hands(frame: np.ndarray) -> List[HandLandmarks]
    def draw_landmarks(frame: np.ndarray, landmarks: List[HandLandmarks])
```

## 依赖

- opencv-python >= 4.8.0
- mediapipe >= 0.10.0
- numpy >= 1.24.0

## 使用方式

在 `_TASK_SPEC.md` 的 Skills 声明一段引用此 skill：

```yaml
skills:
  - name: hand-tracking
    path: skills/hand-tracking/SKILL.md
    purpose: 实时手部关键点检测
```

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-06-01 | 初始版本，MediaPipe 基础检测 |

---

> **最后更新**: 2026-06-01
