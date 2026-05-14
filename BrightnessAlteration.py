class BrightnessAlteration(Alteration): 
    name = "Brightness change"

    def apply(self, image: np.ndarray, region: DifferenceRegion, rng: random.Random) -> None:
        roi = self._roi(image, region)
        alpha = rng.choice([0.86, 0.90, 1.10, 1.14])
        beta = rng.choice([-8, -4, 4, 8])
        adjusted = cv2.convertScaleAbs(roi, alpha=alpha, beta=beta)
        image[region.y : region.y + region.height, region.x : region.x + region.width] = adjusted