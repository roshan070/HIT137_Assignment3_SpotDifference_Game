class GameRound:
    

    def __init__(self, image_path: str, generator: DifferenceGenerator) -> None:
        self.image_path = image_path
        self.original_bgr = ImageLoader.load_bgr(image_path)
        self.modified_bgr, self.regions = generator.create_modified_image(self.original_bgr)
        self.mistakes = 0
        self.locked = False
        self.completed = False

    @property
    def remaining(self) -> int:
        
        return sum(1 for region in self.regions if not region.found and not region.revealed)

    @property
    def found_count(self) -> int:
        """Number of correctly found differences in this round."""
        return sum(1 for region in self.regions if region.found)

    def process_click(self, x: int, y: int) -> Tuple[str, Optional[DifferenceRegion]]:
        if self.locked or self.completed:
            return "locked", None

        for region in self.regions:
            if not region.found and not region.revealed:
                if region.contains_click(x, y, CLICK_TOLERANCE_PIXELS):
                    region.found = True
                    if self.found_count == TOTAL_DIFFERENCES:
                        self.completed = True
                        self.locked = True
                        return "completed", region
                    return "found", region

        self.mistakes += 1
        if self.mistakes >= MAX_MISTAKES:
            self.locked = True
        return "mistake", None

    def reveal_unfound(self) -> None:
        for region in self.regions:
            if not region.found:
                region.revealed = True
        self.locked = True

    def render_original_with_marks(self) -> np.ndarray:
        return self._draw_marks(self.original_bgr.copy())

    def render_modified_with_marks(self) -> np.ndarray:
        return self._draw_marks(self.modified_bgr.copy())

    def _draw_marks(self, image: np.ndarray) -> np.ndarray:
        for region in self.regions:
            if region.found:
                self._draw_circle_with_outline(image, region, RED_BGR)
            elif region.revealed:
                self._draw_circle_with_outline(image, region, BLUE_BGR)
        return image

    @staticmethod
    def _draw_circle_with_outline(
        image: np.ndarray,
        region: DifferenceRegion,
        colour: Tuple[int, int, int],
        ) -> None:
        cx, cy = region.centre
        radius = region.radius
        cv2.circle(image, (cx, cy), radius, BLACK_BGR, thickness=5, lineType=cv2.LINE_AA)
        cv2.circle(image, (cx, cy), radius, colour, thickness=3, lineType=cv2.LINE_AA)

    def debug_summary(self) -> str:
        """Return a readable summary useful for marker testing or debugging."""
        lines = [f"Image: {os.path.basename(self.image_path)}"]
        lines.extend(str(region) for region in self.regions)
        return "\n".join(lines)
