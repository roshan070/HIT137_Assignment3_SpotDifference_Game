class SpotDifferenceApp(tk.Tk):

    def _init_(self) -> None:
        super()._init_()
        self.title("HIT137 Spot the Difference - OpenCV + Tkinter")
        self.configure(bg=WINDOW_BG)
        self.minsize(1180, 650)

        self.generator = DifferenceGenerator()
        self.round: Optional[GameRound] = None
        self.total_found = 0
        self.completed_rounds = 0

        self._build_menu()
        self._build_toolbar()
        self._build_image_area()
        self._build_status_bar()
        self._update_status("Ready. Load a JPG, PNG or BMP image to begin.")

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Load Image", command=self.load_image)
        file_menu.add_command(label="Reveal Differences", command=self.reveal_differences)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="How to Play", command=self.show_help)
        help_menu.add_command(label="About OOP Design", command=self.show_oop_summary)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menu_bar)

    def _build_toolbar(self) -> None:
        toolbar = tk.Frame(self, bg="#dbe7f0", padx=10, pady=8)
        toolbar.pack(side="top", fill="x")

        self.load_button = tk.Button(
            toolbar,
            text="Load New Image",
            command=self.load_image,
            font=("Arial", 11, "bold"),
            width=16,
        )
        self.load_button.pack(side="left", padx=4)

        self.reveal_button = tk.Button(
            toolbar,
            text="Reveal Unfound",
            command=self.reveal_differences,
            font=("Arial", 11),
            width=16,
            state="disabled",
        )
        self.reveal_button.pack(side="left", padx=4)

        self.help_button = tk.Button(
            toolbar,
            text="Help",
            command=self.show_help,
            font=("Arial", 11),
            width=10,
        )
        self.help_button.pack(side="left", padx=4)

        self.info_label = tk.Label(
            toolbar,
            text="Only click the modified image on the right.",
            bg="#dbe7f0",
            fg="#1b263b",
            font=("Arial", 11),
        )
        self.info_label.pack(side="left", padx=18)

    def _build_image_area(self) -> None:
        area = tk.Frame(self, bg=WINDOW_BG, padx=12, pady=12)
        area.pack(fill="both", expand=True)

        self.original_panel = ImagePanel(area, "Original Image - Reference Only")
        self.original_panel.grid(row=0, column=0, padx=10, pady=6, sticky="nsew")

        self.modified_panel = ImagePanel(area, "Modified Image - Click Here", clickable=True)
        self.modified_panel.grid(row=0, column=1, padx=10, pady=6, sticky="nsew")
        self.modified_panel.canvas.bind("<Button-1>", self.handle_modified_click)

        area.columnconfigure(0, weight=1)
        area.columnconfigure(1, weight=1)
        area.rowconfigure(0, weight=1)

    def _build_status_bar(self) -> None:
        status_frame = tk.Frame(self, bg="#edf2f4", padx=8, pady=8)
        status_frame.pack(side="bottom", fill="x")

        self.remaining_var = tk.StringVar(value="Remaining: -")
        self.mistakes_var = tk.StringVar(value="Mistakes: 0/3")
        self.score_var = tk.StringVar(value="Total found: 0")
        self.rounds_var = tk.StringVar(value="Completed rounds: 0")
        self.message_var = tk.StringVar(value="Ready")

        for text_var in [self.remaining_var, self.mistakes_var, self.score_var, self.rounds_var]:
            label = tk.Label(
                status_frame,
                textvariable=text_var,
                bg="#edf2f4",
                fg="#1b263b",
                font=("Arial", 11, "bold"),
                padx=12,
            )
            label.pack(side="left")

        message_label = tk.Label(
            status_frame,
            textvariable=self.message_var,
            bg="#edf2f4",
            fg="#495057",
            font=("Arial", 11),
            anchor="e",
        )
        message_label.pack(side="right", fill="x", expand=True)

    def load_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Choose image for Spot the Difference",
            filetypes=SUPPORTED_FILE_TYPES,
        )
        if not path:
            return

        try:
            new_round = GameRound(path, self.generator)
        except Exception as exc:
            messagebox.showerror("Image loading error", str(exc))
            self._update_status(f"Could not load image: {exc}")
            return

        self.round = new_round
        self.reveal_button.config(state="normal")
        self._refresh_images()
        self._update_status(f"New round loaded: {os.path.basename(path)}")

    def handle_modified_click(self, event: tk.Event) -> None:
        if self.round is None:
            self._update_status("Please load an image first.")
            return

        if self.round.locked:
            self._update_status("This round is locked. Load a new image to continue.")
            return

        coordinates = self.modified_panel.display_to_image_coordinates(event.x, event.y)
        if coordinates is None:
            self._update_status("Click inside the modified image area.")
            return

        x, y = coordinates
        result, region = self.round.process_click(x, y)

        if result == "found" and region is not None:
            self.total_found += 1
            self._update_status(f"Correct: {region.alteration_name} found.")
        elif result == "completed" and region is not None:
            self.total_found += 1
            self.completed_rounds += 1
            self.reveal_button.config(state="disabled")
            self._update_status("Excellent! All 5 differences were found.")
            messagebox.showinfo(
                "Round complete",
                "Well done! You found all 5 differences. Load a new image to continue.",
            )
        elif result == "mistake":
            if self.round.mistakes >= MAX_MISTAKES:
                self.reveal_button.config(state="normal")
                self._update_status("Too many incorrect guesses. Load a new image or reveal answers.")
                messagebox.showwarning(
                    "Round locked",
                    "You made 3 mistakes. No more guesses are allowed for this image.",
                )
            else:
                remaining_chances = MAX_MISTAKES - self.round.mistakes
                self._update_status(f"Incorrect click. {remaining_chances} mistake chance(s) left.")
        else:
            self._update_status("This round is locked. Load a new image to continue.")

        self._refresh_images()

    def reveal_differences(self) -> None:
        if self.round is None:
            self._update_status("Please load an image first.")
            return

        self.round.reveal_unfound()
        self.reveal_button.config(state="disabled")
        self._refresh_images()
        self._update_status("All unfound differences have been revealed in blue. Load a new image to restart.")

    def _refresh_images(self) -> None:
        if self.round is None:
            return

        self.original_panel.show_image(self.round.render_original_with_marks())
        self.modified_panel.show_image(self.round.render_modified_with_marks())
        self.remaining_var.set(f"Remaining: {self.round.remaining}")
        self.mistakes_var.set(f"Mistakes: {self.round.mistakes}/{MAX_MISTAKES}")
        self.score_var.set(f"Total found: {self.total_found}")
        self.rounds_var.set(f"Completed rounds: {self.completed_rounds}")

    def _update_status(self, message: str) -> None:
        self.message_var.set(message)

    def show_help(self) -> None:
        messagebox.showinfo(
            "How to Play",
            "1. Click 'Load New Image' and choose a JPG, PNG or BMP image.\n"
            "2. The left image is the original reference.\n"
            "3. The right image has exactly 5 hidden differences. Click only the right image.\n"
            "4. Correct answers are circled in red on both images.\n"
            "5. You can make a maximum of 3 mistakes per image.\n"
            "6. Use 'Reveal Unfound' to show remaining differences in blue.",
        )

    def show_oop_summary(self) -> None:
        messagebox.showinfo(
            "OOP Design Summary",
            "Classes used:\n"
            "- SpotDifferenceApp: main Tkinter application.\n"
            "- ImagePanel: reusable image display canvas.\n"
            "- GameRound: current game state, score, mistakes and feedback.\n"
            "- DifferenceGenerator: creates random non-overlapping differences.\n"
            "- DifferenceRegion: stores each hidden region.\n"
            "- Alteration base class with 4 subclasses:\n"
            "  ColourShiftAlteration, BlurAlteration, BrightnessAlteration, ShapeOverlayAlteration.\n\n"
            "Inheritance and polymorphism are shown because all alteration subclasses override apply(), "
            "and the generator calls apply() through the Alteration base class reference.",
        )