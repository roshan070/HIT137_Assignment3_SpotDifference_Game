class DifferenceGenerator:
    def _init_(self, alteration_types: Optional[Sequence[Alteration]] = None) -> None:
        self._alterations: List[Alteration] = list(
            alteration_types
            if alteration_types is not None
            else [
                ColourShiftAlteration(),
                BlurAlteration(),
                BrightnessAlteration(),
                ShapeOverlayAlteration(),
            ]
        )
        self._rng = random.Random()

    @property
    def alteration_names(self) -> List[str]:
       
        return [alteration.name for alteration in self._alterations]

    def create_modified_image(
        self,
        original_bgr: np.ndarray,
        count: int = TOTAL_DIFFERENCES,
    ) -> Tuple[np.ndarray, List[DifferenceRegion]]:
        """Clone the image and create exactly count random differences."""
        height, width = original_bgr.shape[:2]
        self._validate_image_size(width, height)

        modified = original_bgr.copy()
        regions: List[DifferenceRegion] = []

        for _ in range(count):
            alteration = self._rng.choice(self._alterations)
            region = self._make_non_overlapping_region(width, height, regions, alteration.name)
            alteration.apply(modified, region, self._rng)
            regions.append(region)

        return modified, regions

    def _validate_image_size(self, width: int, height: int) -> None:
        if width < 280 or height < 180:
            raise ValueError(
                "Please choose a larger image. Recommended minimum size is 280 x 180 pixels."
            )

    def _make_non_overlapping_region(
        self,
        image_width: int,
        image_height: int,
        existing: List[DifferenceRegion],
        alteration_name: str,
    ) -> DifferenceRegion:
        """Keep trying random rectangles until a non-overlapping one is found."""
        min_side = max(28, min(image_width, image_height) // 14)
        max_w = max(min_side + 1, image_width // 5)
        max_h = max(min_side + 1, image_height // 5)
        margin = max(12, min(image_width, image_height) // 45)

        for _ in range(1000):
            w = self._rng.randint(min_side, max_w)
            h = self._rng.randint(min_side, max_h)
            x = self._rng.randint(margin, image_width - w - margin)
            y = self._rng.randint(margin, image_height - h - margin)
            candidate = DifferenceRegion(x, y, w, h, alteration_name)

            if all(not candidate.overlaps(other, margin=margin) for other in existing):
                return candidate

        raise ValueError(
            "Could not place all differences without overlap. Try a larger or less crowded image."
        )