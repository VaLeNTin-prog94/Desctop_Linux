import psutil
import tkinter as tk
from tkinter import StringVar, IntVar, ttk
import sqlite3
import time


def create_db_connection(db_file='system_monitor.db'):
    """
    Создает соединение с базой данных SQLite.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage (
            id INTEGER PRIMARY KEY,
            cpu_usage REAL,
            memory_usage REAL,
            disk_usage REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn, cursor


class SystemMonitorApp:
    def __init__(self):
        self.conn, self.cursor = create_db_connection()  # Создаем соединение с базой данных

        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Мониторинг системы")

        self.start_time = None  # Время начала записи
        self.recording = IntVar(value=0)  # Инициализация recording здесь

        # Переменные для загрузки системы
        self.cpu_var = StringVar()
        self.memory_var = StringVar()
        self.disk_var = StringVar()
        self.timer_var = StringVar()

        # Настраиваем вывод меток
        tk.Label(self.root, textvariable=self.cpu_var).pack()
        tk.Label(self.root, textvariable=self.memory_var).pack()
        tk.Label(self.root, textvariable=self.disk_var).pack()
        tk.Label(self.root, textvariable=self.timer_var).pack()

        # Интервал обновления
        self.update_interval = IntVar(value=1)
        tk.Label(self.root, text="Интервал обновления (сек):").pack()
        tk.Entry(self.root, textvariable=self.update_interval).pack()

        # Кнопка начать/остановить запись
        self.record_button = tk.Button(self.root, text="Начать запись", command=self.toggle_recording)
        self.record_button.pack()

        # Кнопка для просмотра истории
        history_button = tk.Button(self.root, text="Просмотреть историю", command=self.show_history)
        history_button.pack()

        # Обновляем метрики и запускаем главное событие
        self.update_metrics()

    def record_usage(self, cpu_usage, memory_usage, disk_usage):
        """
        Записывает метрики загрузки системы в базу данных.
        """
        self.cursor.execute('INSERT INTO usage (cpu_usage, memory_usage, disk_usage) VALUES (?, ?, ?)',
                            (cpu_usage, memory_usage, disk_usage))
        self.conn.commit()

    def update_metrics(self):
        """
        Обновляет метрики загрузки ЦП, ОЗУ и ПЗУ и отображает их в интерфейсе.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        disk_info = psutil.disk_usage('/')
        disk_usage = disk_info.percent

        self.cpu_var.set(f"Загрузка ЦП: {cpu_usage}%")
        self.memory_var.set(f"Загрузка ОЗУ: {memory_usage}%")
        self.disk_var.set(f"Загрузка ПЗУ: {disk_usage}%")

        # Запись в базу данных
        if self.recording.get():  # Проверяем, нажата ли кнопка записи
            self.record_usage(cpu_usage, memory_usage, disk_usage)
            self.update_timer()  # Обновляем таймер записи

        self.root.after(self.update_interval.get() * 1000, self.update_metrics)

    def toggle_recording(self):
        """
        Переключает состояние записи метрик.
        """
        if self.recording.get() == 0:  # Начинаем запись
            self.recording.set(1)
            self.record_button.config(text="Остановить")
            self.start_time = time.time()  # Устанавливаем время начала записи
            self.update_timer()
        else:  # Останавливаем запись
            self.recording.set(0)
            self.record_button.config(text="Начать запись")
            self.timer_var.set("Время записи: 0 сек")  # Сбрасываем таймер

    def update_timer(self):
        """
        Обновляет таймер записи метрик.
        """
        if self.recording.get():
            elapsed_time = int(time.time() - self.start_time)
            self.timer_var.set(f"Время записи: {elapsed_time} сек")
            self.root.after(1000, self.update_timer)  # Обновляем таймер каждую секунду

    def show_history(self):
        """
        Открывает новое окно с историей записей метрик.
        """
        history_window = tk.Toplevel(self.root)
        history_window.title("История записей")

        columns = ("ID", "ЦП (%)", "ОЗУ (%)", "ПЗУ (%)", "Время")
        tree = ttk.Treeview(history_window, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)

        # Получаем данные из базы данных
        self.cursor.execute('SELECT * FROM usage')
        for row in self.cursor.fetchall():
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill="both")
        # Добавляем кнопку закрытия
        tk.Button(history_window, text="Закрыть", command=history_window.destroy).pack()

    def run(self):
        """
        Запускает главное событие.
        """
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """
        Закрывает соединение с базой данных перед выходом.
        """
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    app = SystemMonitorApp()  # Создаем и запускаем приложение
    app.run()