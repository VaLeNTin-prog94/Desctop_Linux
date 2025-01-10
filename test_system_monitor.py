import unittest
import sqlite3
import psutil
import os
import time

class TestSystemMonitorApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Создает временную базу данных для тестирования.
        """
        cls.db_file = 'test_system_monitor.db'
        cls.conn = sqlite3.connect(cls.db_file)
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage (
                id INTEGER PRIMARY KEY,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        """
        Удаляет временную базу данных после завершения тестов.
        """
        cls.conn.close()
        os.remove(cls.db_file)

    def setUp(self):
        """
        Очищает таблицу usage перед каждым тестом.
        """
        self.cursor.execute('DELETE FROM usage')
        self.conn.commit()

    def test_create_db_connection(self):
        """
        Тестирует создание соединения с базой данных.
        """
        conn = sqlite3.connect(self.db_file)
        self.assertIsNotNone(conn)
        conn.close()

    def test_insert_usage(self):
        """
        Тестирует вставку метрик использования в базу данных.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        disk_info = psutil.disk_usage('/')
        disk_usage = disk_info.percent

        self.cursor.execute('INSERT INTO usage (cpu_usage, memory_usage, disk_usage) VALUES (?, ?, ?)',
                            (cpu_usage, memory_usage, disk_usage))
        self.conn.commit()

        # Проверяем, что значение было корректно вставлено
        self.cursor.execute('SELECT * FROM usage ORDER BY id DESC LIMIT 1')
        last_entry = self.cursor.fetchone()
        self.assertIsNotNone(last_entry)
        self.assertEqual(last_entry[1], cpu_usage)  # cpu_usage
        self.assertEqual(last_entry[2], memory_usage)  # memory_usage
        self.assertEqual(last_entry[3], disk_usage)  # disk_usage

    def test_update_metrics(self):
        """
        Тестирует возможность обновления метрик (проверка с имитацией).
        """
        cpu_usage_before = psutil.cpu_percent(interval=1)
        time.sleep(1)  # Ждем, чтобы позволить изменениям CPU
        cpu_usage_after = psutil.cpu_percent(interval=1)

        self.assertNotEqual(cpu_usage_before, cpu_usage_after)

    def test_show_history(self):
        """
        Тестирует, что получение исторических данных работает корректно.
        """
        # Вставляем тестовые данные
        for _ in range(5):
            self.test_insert_usage()

        # Получаем историю
        self.cursor.execute('SELECT COUNT(*) FROM usage')
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 5)

if __name__ == '__main__':
    unittest.main()