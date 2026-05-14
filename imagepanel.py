class ImagePanel(tk.Frame):

    def _init_(self, master: tk.Widget, title: str, clickable: bool = False) -> None:
        super()._init_(master, bg=WINDOW_BG)
        self.title = title
        self.clickable = clickable
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.displayed_width = 1
        self.displayed_height = 1
        self._photo: Optional[ImageTk.PhotoImage] = None

        title_label = tk.Label(
            self,
            text=title,
            font=("Arial", 13, "bold"),
            bg=WINDOW_BG,
            fg="#1b263b",
        )
        title_label.pack(pady=(0, 6))

        self.canvas = tk.Canvas(
            self,
            width=DISPLAY_WIDTH,
            height=DISPLAY_HEIGHT,
            bg=PANEL_BG,
            highlightthickness=1,
            highlightbackground="#aab7c4",
        )
        self.canvas.pack()

        self.canvas.create_text(
            DISPLAY_WIDTH // 2,
            DISPLAY_HEIGHT // 2,
            text="Load an image to start",
            fill="#6c757d",
            font=("Arial", 13),
        )

    def show_image(self, image_bgr: np.ndarray) -> None:
        self.canvas.delete("all")
        image_h, image_w = image_bgr.shape[:2]
        self.scale = min(DISPLAY_WIDTH / image_w, DISPLAY_HEIGHT / image_h, 1.0)
        self.displayed_width = max(1, int(image_w * self.scale))
        self.displayed_height = max(1, int(image_h * self.scale))
        self.offset_x = (DISPLAY_WIDTH - self.displayed_width) // 2
        self.offset_y = (DISPLAY_HEIGHT - self.displayed_height) // 2

        display_bgr = cv2.resize(
            image_bgr,
            (self.displayed_width, self.displayed_height),
            interpolation=cv2.INTER_AREA,
        )
        display_rgb = cv2.cvtColor(display_bgr, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(display_rgb)
        self._photo = ImageTk.PhotoImage(pil_image)

        self.canvas.create_image(self.offset_x, self.offset_y, image=self._photo, anchor="nw")

    def display_to_image_coordinates(self, event_x: int, event_y: int) -> Optional[Tuple[int, int]]:
        if not (
            self.offset_x <= event_x <= self.offset_x + self.displayed_width
            and self.offset_y <= event_y <= self.offset_y + self.displayed_height
        ):
            return None

        x = int((event_x - self.offset_x) / self.scale)
        y = int((event_y - self.offset_y) / self.scale)
        return x, y