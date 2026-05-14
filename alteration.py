class Alteration(ABC):

    name = "Base alteration"

    @abstractmethod
    def apply(
        self,
        image: np.ndarray,
        region: DifferenceRegion,
        rng: random.Random,
    ) -> None:
        
        raise NotImplementedError

    def _roi(self, image: np.ndarray, region: DifferenceRegion) -> np.ndarray:
        
        return image[region.y : region.y + region.height, region.x : region.x + region.width]
