from tkinter import ttk, messagebox, StringVar


class Timer:
    def __init__(self, root, on_tick, on_end, time_sec=30):
        self.__root = root
        self.__limit = time_sec
        self.__time = 0
        self.__timer = None
        self.__on_tick = on_tick
        self.__on_end = on_end

    @property
    def time(self):
        return self.__time

    @property
    def limit(self):
        return self.__limit

    def start(self):
        self.__time = self.__limit
        self.__timer = self.__root.after(1000, self.__tick)

    def __tick(self):
        if self.__time > 0:
            self.__time -= 1
            self.__on_tick()
            self.__timer = self.__root.after(1000, self.__tick)
            return

        self.__on_end()
        self.__root.after_cancel(self.__timer)


class TestModeGUI:
    def __init__(self, root, on_start, on_end, time=30):
        self.__root = root

        self.__on_start = on_start
        self.__on_end = on_end

        self.__time = StringVar()
        self.__timer_label = ttk.Label(self.__root, textvariable=self.__time, font=("Arial", 16))

        self.__timer = Timer(self.__root, self.__update_time, self.__end, time)

        self.__start_button = ttk.Button(self.__root, text="Режим теста", command=self.__start)
        self.__start_button.pack(pady=10)

    def __update_time(self):
        self.__time.set(f"Осталось времени: {self.__timer.time}")

    def __start(self):
        if not messagebox.askyesno("Режим теста", "Вы точно хотите войти в режим теста?"):
            return

        self.__timer_label.pack()
        self.__start_button["state"] = "disabled"
        self.__on_start()
        self.__timer.start()
        self.__update_time()

    def __end(self):
        messagebox.showinfo("Режим теста", "Тест завершён!")
        self.__start_button["state"] = "normal"
        self.__timer_label.pack_forget()
        self.__on_end()
