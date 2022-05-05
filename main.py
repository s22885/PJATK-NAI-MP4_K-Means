import data_migrate
import indiv_kmeans
import str_carve

from tkinter import *

root = Tk()
root.title("Midas")
root.geometry("500x500")


class Elder:
    kmean: indiv_kmeans.Kmeans
    separator: str = ";"

    def __init__(self, master):
        my_frame = Frame(master)
        my_frame.pack()
        self.button_clear_board = Button(master, text="wyczyść konsolke", command=self.clear_board)
        self.button_clear_board.pack()
        self.button_new_kmeans = Button(master, text="nowe kmeans", command=self.create_indiv_kmeans)
        self.button_new_kmeans.pack()
        self.button_load_data = Button(master, text="ładowanie danych", command=self.load_data)
        self.button_load_data.pack()
        self.button_add_vec = Button(master, text="dodaj punkt", command=self.add_vec_promp)
        self.button_add_vec.pack()
        self.button_extract_data = Button(master, text="zwróć datę", command=self.data_extract)
        self.button_extract_data.pack()
        self.button_kmeans_compute = Button(master, text="rozpocznij grupowanie", command=self.indiv_kmeans_compute)
        self.button_kmeans_compute.pack()
        self.promp_win = Text(root, height=200, width=200)
        self.promp_win.pack()

    def create_indiv_kmeans(self):
        promp = self.get_prompt()
        promp = promp.split(sep=" ")
        if len(promp) == 3:
            try:
                dim = int(promp[0])
                k = int(promp[1])
                stop_prop = float(promp[2])
                tmp_indiv_kmeans = indiv_kmeans.Kmeans.new_kmeans(dim, k, stop_prop)
                if tmp_indiv_kmeans is None:
                    self.say_board("błąd parsowania format dla kmeans to:\n<liczba_wymiarów> <ilość_grup> "
                                   "<parametr_różnicy_stopu_float>")
                    self.kmean = None
                else:
                    self.kmean = tmp_indiv_kmeans
                    self.say_board("udało się kmeans stworzone")

            except ValueError:
                self.say_board("błąd parsowania format dla kmeans to:\n<liczba_wymiarów> <ilość_grup> "
                               "<parametr_różnicy_stopu_float>")
        else:
            self.say_board("błąd parsowania format dla kmeans to:\n<liczba_wymiarów> <ilość_grup> "
                           "<parametr_różnicy_stopu_float>")

    def data_extract(self):
        if self.kmean is not None:
            self.say_board(self.kmean.to_text())
        else:
            self.say_board("proszę stworzyć kmeans")

    def add_vec_promp(self):
        if self.kmean is not None:
            tmp_data = str_carve.get_vecs(self.get_prompt(), separator=" ")
            tmp_res = self.kmean.add_vecs(tmp_data)
            if tmp_res:
                self.say_board("poprawnie dodany punkt")
            else:
                self.say_board("błąd parsowania")
        else:
            self.say_board("proszę stworzyć kmeans")

    def indiv_kmeans_compute(self):
        if self.kmean is not None:
            tmp_res = self.kmean.compute()
            if tmp_res:
                self.say_board("dane po agregacji")
            else:
                self.say_board("błąd brak danych")
        else:
            self.say_board("proszę stworzyć kmeans")

    def load_data(self):
        if self.kmean is not None:
            tmp_data = data_migrate.data_load(self.get_prompt())
            if tmp_data[0]:
                dims = str_carve.get_vecs(tmp_data[1], separator=self.separator)
                load_res = self.kmean.add_vecs(dims)
                self.say_board(f"pozytywnie załadowane dane: {load_res[0]}\n"
                               f"nie załadowane dane: {load_res[1]}\n")
            else:
                self.say_board("błąd ładowania danych")
        else:
            self.say_board("proszę stworzyć kmeans")

    def get_prompt(self):
        return self.promp_win.get("1.0", "end-1c")

    def set_separator(self):
        self.separator = self.get_prompt()

    def clear_board(self):
        self.promp_win.delete(1.0, "end")

    def say_board(self, text_s):
        self.promp_win.insert(1.0, text_s)


e = Elder(root)

root.mainloop()
