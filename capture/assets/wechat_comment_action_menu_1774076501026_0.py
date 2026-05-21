"""微信评论操作菜单 helper。

适用前提：
1. 调用前已完成目标评论长按，且当前评论操作菜单已经弹出。
2. 当前场景下无障碍节点拿不到“不喜欢/投诉”菜单项时，回退使用 OCR 锚点推算槽位点击。

设计取舍：
1. 不依赖页面正文结构，只依赖评论操作菜单自身的文案顺序。
2. 先用全屏坐标 OCR 找稳定锚点（复制/转发/翻译）所在行，再裁这一条菜单区域重跑坐标 OCR。
3. 若目标文案本身没有坐标，退化为“锚点中心距 + 固定槽位顺序”推算点击点。
"""

from __future__ import annotations

import json
import time
from statistics import median
from typing import Dict, List, Optional

from value_utils import to_text as _to_text


MENU_SLOT_ORDER = ("复制", "转发", "翻译", "不喜欢", "投诉")
MENU_SLOT_INDEX = {label: index for index, label in enumerate(MENU_SLOT_ORDER)}
MENU_ANCHOR_LABELS = ("复制", "转发", "翻译")
MENU_SCREENSHOT_MODE = 0
MENU_BAND_MARGIN_RATIO = 0.04
MENU_BAND_HEIGHT_RATIO = 0.12
MENU_BAND_MIN_HEIGHT = 220


def _normalize_text(value: object) -> str:
    return "".join(_to_text(value, strip=True).split())


def _center_from_box(box: object) -> Optional[Dict[str, float]]:
    if not isinstance(box, list) or not box:
        return None
    points = []
    for item in box:
        if not isinstance(item, list) or len(item) < 2:
            continue
        try:
            points.append((float(item[0]), float(item[1])))
        except Exception:
            continue
    if not points:
        return None
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return {
        "center_x": sum(xs) / len(xs),
        "center_y": sum(ys) / len(ys),
        "left": min(xs),
        "top": min(ys),
        "right": max(xs),
        "bottom": max(ys),
    }


def _center_from_rect(
    *,
    x: object = None,
    y: object = None,
    width: object = None,
    height: object = None,
) -> Optional[Dict[str, float]]:
    try:
        left = float(x)
        top = float(y)
        rect_width = float(width)
        rect_height = float(height)
    except Exception:
        return None
    if rect_width <= 0 or rect_height <= 0:
        return None
    return {
        "center_x": left + rect_width / 2.0,
        "center_y": top + rect_height / 2.0,
        "left": left,
        "top": top,
        "right": left + rect_width,
        "bottom": top + rect_height,
    }


def _extract_ocr_entries(result: Dict[str, object]) -> List[Dict[str, float]]:
    entries: List[Dict[str, float]] = []
    seen = set()

    def _append(
        raw_text: object,
        *,
        box: object = None,
        x: object = None,
        y: object = None,
        width: object = None,
        height: object = None,
    ) -> None:
        text = _normalize_text(raw_text)
        if not text:
            return
        geometry = _center_from_box(box) or _center_from_rect(
            x=x,
            y=y,
            width=width,
            height=height,
        )
        if not geometry:
            return
        dedupe_key = (
            text,
            int(round(geometry["center_x"])),
            int(round(geometry["center_y"])),
        )
        if dedupe_key in seen:
            return
        seen.add(dedupe_key)
        entries.append({"text": text, **geometry})

    for line in result.get("lines", []) or []:
        _append(
            line.get("str"),
            x=line.get("x"),
            y=line.get("y"),
            width=line.get("width"),
            height=line.get("height"),
        )
        for word in line.get("words", []) or []:
            _append(
                word.get("str") or word.get("text"),
                box=word.get("box"),
                x=word.get("x"),
                y=word.get("y"),
                width=word.get("width"),
                height=word.get("height"),
            )
    for word in result.get("words", []) or []:
        _append(
            word.get("text") or word.get("str"),
            box=word.get("box"),
            x=word.get("x"),
            y=word.get("y"),
            width=word.get("width"),
            height=word.get("height"),
        )
    return entries


def _find_anchor(entries: List[Dict[str, float]]) -> Optional[Dict[str, float]]:
    for anchor_text in MENU_ANCHOR_LABELS:
        for entry in entries:
            if entry["text"] == anchor_text:
                return entry
    for anchor_text in MENU_ANCHOR_LABELS:
        for entry in entries:
            if anchor_text in entry["text"]:
                return entry
    return None


def _build_crop_rect(zbot, anchor: Dict[str, float]) -> Dict[str, int]:
    screen_width = int(getattr(getattr(zbot, "device", None), "width", 1080) or 1080)
    screen_height = int(getattr(getattr(zbot, "device", None), "height", 2400) or 2400)
    margin_x = max(24, int(screen_width * MENU_BAND_MARGIN_RATIO))
    band_height = max(MENU_BAND_MIN_HEIGHT, int(screen_height * MENU_BAND_HEIGHT_RATIO))
    y = int(round(anchor["center_y"])) - band_height // 2
    if y < 0:
        y = 0
    if y + band_height > screen_height:
        y = max(0, screen_height - band_height)
    width = max(1, screen_width - margin_x * 2)
    return {"x": margin_x, "y": y, "w": width, "h": band_height}


def _infer_click_point(entries: List[Dict[str, float]], label: str) -> Optional[Dict[str, float]]:
    target_index = MENU_SLOT_INDEX.get(label)
    if target_index is None:
        return None

    exact_matches = [entry for entry in entries if entry["text"] == label]
    if exact_matches:
        best = exact_matches[0]
        return {
            "x": best["center_x"],
            "y": best["center_y"],
            "source": "ocr_exact",
            "reference": best["text"],
        }

    indexed_entries: Dict[int, Dict[str, float]] = {}
    for entry in entries:
        entry_index = MENU_SLOT_INDEX.get(entry["text"])
        if entry_index is None or entry_index in indexed_entries:
            continue
        indexed_entries[entry_index] = entry
    if len(indexed_entries) < 2:
        return None

    ordered_entries = sorted(indexed_entries.items(), key=lambda item: item[0])
    pitch_values = []
    for idx in range(1, len(ordered_entries)):
        left_index, left_entry = ordered_entries[idx - 1]
        right_index, right_entry = ordered_entries[idx]
        slot_delta = right_index - left_index
        if slot_delta <= 0:
            continue
        pitch_values.append((right_entry["center_x"] - left_entry["center_x"]) / slot_delta)
    if not pitch_values:
        return None

    pitch = float(median(pitch_values))
    if pitch <= 40:
        return None
    row_center_y = float(median([entry["center_y"] for _, entry in ordered_entries]))
    reference_index, reference_entry = min(
        ordered_entries,
        key=lambda item: abs(item[0] - target_index),
    )
    target_center_x = reference_entry["center_x"] + (target_index - reference_index) * pitch
    return {
        "x": target_center_x,
        "y": row_center_y,
        "source": "ocr_anchor_pitch",
        "reference": reference_entry["text"],
        "reference_slot": reference_index,
        "pitch": pitch,
    }


def infer_menu_action_click_point(
    zbot,
    label: str,
    *,
    log_prefix: str = "[WECHAT_COMMENT_MENU]",
) -> Optional[Dict[str, object]]:
    screenshot_path = None
    try:
        screenshot_path = zbot.captureScreenshot(
            "storage/",
            f"wechat_comment_menu_{int(time.time() * 1000)}.png",
            MENU_SCREENSHOT_MODE,
        )
        image = zbot.image.load(screenshot_path)
        full_screen_b64 = zbot.image.toBase64(image, "png", 70)
        full_screen_payload = zbot.ai.ocr_with_position(full_screen_b64)
        full_screen_result = full_screen_payload.get("result", {}) if isinstance(full_screen_payload, dict) else {}
        full_screen_entries = _extract_ocr_entries(full_screen_result)
        anchor = _find_anchor(full_screen_entries)
        if not anchor:
            if hasattr(zbot, "log"):
                zbot.log(f"{log_prefix} {label} failed: full-screen anchor missing")
            return None

        crop_rect = _build_crop_rect(zbot, anchor)
        crop_image = zbot.image.crop(image, crop_rect["x"], crop_rect["y"], crop_rect["w"], crop_rect["h"])
        crop_b64 = zbot.image.toBase64(crop_image, "png", 80)
        crop_payload = zbot.ai.ocr_with_position(crop_b64)
        crop_result = crop_payload.get("result", {}) if isinstance(crop_payload, dict) else {}
        crop_entries = _extract_ocr_entries(crop_result)
        point = _infer_click_point(crop_entries, label)
        if not point:
            if hasattr(zbot, "log"):
                zbot.log(
                    f"{log_prefix} {label} failed: target missing; crop_rect="
                    f"{json.dumps(crop_rect, ensure_ascii=False)}"
                )
            return None

        return {
            "label": label,
            "click_x": int(round(crop_rect["x"] + point["x"])),
            "click_y": int(round(crop_rect["y"] + point["y"])),
            "source": point["source"],
            "anchor_text": anchor["text"],
            "crop_rect": crop_rect,
        }
    finally:
        if screenshot_path and hasattr(zbot, "files") and hasattr(zbot.files, "remove"):
            try:
                zbot.files.remove(screenshot_path)
            except Exception:
                pass


def click_menu_action(
    zbot,
    label: str,
    *,
    settle_ms: int = 1200,
    log_prefix: str = "[WECHAT_COMMENT_MENU]",
) -> Optional[Dict[str, object]]:
    click_meta = infer_menu_action_click_point(zbot, label, log_prefix=log_prefix)
    if not click_meta:
        return None
    if hasattr(zbot, "log"):
        zbot.log(
            f"{log_prefix} click {label}: anchor={click_meta['anchor_text']} "
            f"source={click_meta['source']} point=({click_meta['click_x']},{click_meta['click_y']})"
        )
    zbot.automator.click(click_meta["click_x"], click_meta["click_y"])
    if hasattr(zbot, "sleep"):
        zbot.sleep(settle_ms)
    return click_meta


__all__ = [
    "MENU_SCREENSHOT_MODE",
    "_extract_ocr_entries",
    "_infer_click_point",
    "click_menu_action",
    "infer_menu_action_click_point",
]
