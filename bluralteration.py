class BlurAlteration(Alteration):
    name = "Local blur"

    def apply(self, image: np.ndarray, region: DifferenceRegion, rng: random.Random) -> None:
        roi = self._roi(image, region)
        kernel_size = rng.choice([9, 11, 13])
        blurred = cv2.GaussianBlur(roi, (kernel_size, kernel_size), 0)
        image[region.y : region.y + region.height, region.x : region.x + region.width] = blurred