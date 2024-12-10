import cv2
import numpy as np

def multi_scale_template_matching(screenshot, target_image, scale_range=(0.5, 1.5), step=0.1, threshold=0.8):
    best_match = None
    best_val = 0
    best_loc = None
    best_w, best_h = None, None

    for scale in np.arange(scale_range[0], scale_range[1], step):
        resized_target = cv2.resize(target_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        w, h = resized_target.shape[::-1]

        res = cv2.matchTemplate(screenshot, resized_target, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val > threshold and max_val > best_val:
            best_val = max_val
            best_match = res
            best_loc = max_loc
            best_w, best_h = w, h

    return best_match, best_loc, best_w, best_h
