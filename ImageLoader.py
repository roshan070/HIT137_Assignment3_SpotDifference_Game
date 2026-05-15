class ImageLoader:
    
    @staticmethod
    def load_bgr(path: str) -> np.ndarray:
        
        raw = np.fromfile(path, dtype=np.uint8)
        image = cv2.imdecode(raw, cv2.IMREAD_UNCHANGED)

        if image is None:
            raise ValueError("The selected file could not be read as an image.")

        if len(image.shape) == 2:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        if image.shape[2] == 4:
            bgr = image[:, :, :3]
            alpha = image[:, :, 3].astype(float) / 255.0
            white = np.full_like(bgr, 255)
            blended = (bgr.astype(float) * alpha[:, :, None]) + (
                white.astype(float) * (1.0 - alpha[:, :, None])
            )
            return blended.astype(np.uint8)

        if image.shape[2] == 3:
            return image

        raise ValueError("Unsupported image channel format.")