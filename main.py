import tkinter as tk
from tkinter import filedialog
import random

from ansi_x9_17 import ANSI_X9_17
import monobit_test as test1
import runs_test as test2
import random_excursion_variant_test as test3

class RandomSequenceGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Генератор псевдослучайной последовательности")
        master.geometry("650x500")  # Установка размера окна

        self.label = tk.Label(master, text="Введите параметры генератора:")
        self.label.grid(row=0, column=0, columnspan=2)

        self.label_seed = tk.Label(master, text="Seed:")
        self.label_seed.grid(row=1, column=0)
        self.entry_seed = tk.Entry(master)
        self.entry_seed.grid(row=1, column=1)
        # self.load_seed_button = tk.Button(master, text="Загрузить из файла", command=self.load_seed_from_file)
        # self.load_seed_button.grid(row=1, column=2)

        self.label_key = tk.Label(master, text="Key:")
        self.label_key.grid(row=2, column=0)
        self.entry_key = tk.Entry(master)
        self.entry_key.grid(row=2, column=1)
        # self.load_key_button = tk.Button(master, text="Загрузить из файла", command=self.load_key_from_file)
        # self.load_key_button.grid(row=2, column=2)

        self.label_m = tk.Label(master, text="m:")
        self.label_m.grid(row=3, column=0)
        self.entry_m = tk.Entry(master)
        self.entry_m.grid(row=3, column=1)

        self.generate_button = tk.Button(master, text="Сгенерировать", command=self.generate_sequence)
        self.generate_button.grid(row=4, column=0, columnspan=2)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=5, column=0, columnspan=2)

        # Растягиваем текстовое поле для результатов тестов по всей ширине окна
        self.results_text = tk.Text(master, height=15, width=80)
        self.results_text.grid(row=6, column=0, columnspan=2)

        # Размещаем кнопку "Сохранить результаты тестов" по центру
        self.save_results_button = tk.Button(master, text="Сохранить результаты тестов", command=self.save_results)
        self.save_results_button.grid(row=7, column=0, columnspan=2, pady=10)

    def load_seed_from_file(self):
        filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),))
        if filename:
            with open(filename, "r") as file:
                seed = file.read()
                self.entry_seed.delete(0, tk.END)
                self.entry_seed.insert(0, seed)

    def load_key_from_file(self):
        filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),))
        if filename:
            with open(filename, "r") as file:
                key = file.read()
                self.entry_key.delete(0, tk.END)
                self.entry_key.insert(0, key)

    def generate_sequence(self):
        try:
            seed = int(self.entry_seed.get(), base=2)
            key = int(self.entry_key.get(), base=2)
            m = int(self.entry_m.get(), base=10)

            sequence = str()

            for i in range(m):
                sequence += bin(next(ANSI_X9_17(seed, key)))[2:]

            self.result_label.config(text="Последовательность сгенерирована")
        except ValueError:
            self.result_label.config(text="Ошибка: неверные параметры")
            return

        self.generated_sequence = sequence
        self.test1 = test1.test(sequence)
        self.test2 = test2.test(sequence)
        self.test3 = test3.test(sequence)

        self.results_text.delete(1.0, tk.END)

        self.results = f'''
        Result: {self.generated_sequence}
        ----------------------------------------------------
        Test 1
        Zeroes: {self.test1["zeroes"]}
        Ones: {self.test1["ones"]}
        S: {self.test1["s"]}
        P: {self.test1["p"]}
        Success: {self.test1["success"]}
        ----------------------------------------------------
        Test 2
        Zeroes: {self.test2["zeroes"]}
        Ones: {self.test2["ones"]}
        Prop: {self.test2["prop"]}
        Vobs: {self.test2["vobs"]}
        P: {self.test2["p"]}
        Success: {self.test2["success"]}
        ----------------------------------------------------
        Test 3
        n: {self.test3["n"]}
        J: {self.test3["J"]}
        Count: {self.test3["count"]}
        PList: {self.test3["plist"]}
        P_Average: {self.test3["p_average"]}
        Success: {self.test3["success"]}
        '''

        print(self.results)

        self.results_text.insert(1.0, self.results)
    def save_results(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"),))
            if filename:
                with open(filename, "w") as file:
                    file.write(self.results_text.get("1.0", tk.END))
                self.result_label.config(text=f"Результаты тестов сохранены в {filename}")
            else:
                self.result_label.config(text="Сохранение отменено")
        except AttributeError:
            self.result_label.config(text="Ошибка: сначала выполните тесты")

root = tk.Tk()
app = RandomSequenceGeneratorApp(root)
root.mainloop()
