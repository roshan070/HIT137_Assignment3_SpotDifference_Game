class ColourShiftAlteration(Alteration):
    
    name = "Colour shift"

    def apply(self, image: np.ndarray, region: DifferenceRegion, rng: random.Random) -> None:
        roi = self._roi(image, region)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        h_shift = rng.choice([-14, -10, 10, 14])
        s_shift = rng.choice([-22, 22, 28])
        v_shift = rng.choice([-18, 18, 24])

        hsv_int = hsv.astype(np.int16)
        hsv_int[:, :, 0] = (hsv_int[:, :, 0] + h_shift) % 180
        hsv_int[:, :, 1] = np.clip(hsv_int[:, :, 1] + s_shift, 0, 255)
        hsv_int[:, :, 2] = np.clip(hsv_int[:, :, 2] + v_shift, 0, 255)

        shifted = cv2.cvtColor(hsv_int.astype(np.uint8), cv2.COLOR_HSV2BGR)
        image[region.y : region.y + region.height, region.x : region.x + region.width] = shifted