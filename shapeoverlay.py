class ShapeOverlayAlteration(Alteration):
    name = "Subtle shape"
    def apply(self, image: np.ndarray, region: DifferenceRegion, rng: random.Random) -> None:
        overlay = image.copy()
        x1, y1 = region.x, region.y
        x2, y2 = region.x + region.width, region.y + region.height
        cx, cy = region.centre

        roi = self._roi(image, region)
        mean_colour = tuple(int(v) for v in cv2.mean(roi)[:3])
        colour = tuple(int(np.clip(c + rng.choice([-45, 45]), 0, 255)) for c in mean_colour)

        if rng.choice([True, False]):
            radius = max(8, min(region.width, region.height) // 3)
            cv2.circle(overlay, (cx, cy), radius, colour, thickness=-1)
        else:
            inset_x = max(4, region.width // 5)
            inset_y = max(4, region.height // 5)
            cv2.rectangle(
                overlay,
                (x1 + inset_x, y1 + inset_y),
                (x2 - inset_x, y2 - inset_y),
                colour,
                thickness=-1,
            )

        cv2.addWeighted(overlay, 0.30, image, 0.70, 0, dst=image)