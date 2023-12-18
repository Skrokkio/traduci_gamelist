from tkinter import filedialog
from tkinter import Tk, Label, Button, StringVar
from googletrans import Translator
import xml.etree.ElementTree as ET
from tqdm import tqdm
import os
import  time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_input_xml_file(label_var):
    file_path = filedialog.askopenfilename(
        title="Seleziona il file XML di input",
        filetypes=[("File XML", "*.xml"), ("Tutti i file", "*.*")]
    )
    label_var.set(file_path)

def translate_text(text, dest='it', max_retries=5):
    translator = Translator()

    for _ in range(max_retries):
        try:
            translation = translator.translate(text, dest=dest)
            if translation and hasattr(translation, 'text') and translation.text:
                return translation.text
            else:
                print("La traduzione è vuota o manca il testo.")
                return text
        except Exception as e:
            print(f"Errore durante la traduzione: {e}")
            time.sleep(1)  # Attendi un secondo prima di un nuovo tentativo

    print("Impossibile tradurre il testo. Saltando questo elemento.")
    return text

def translate_and_save(node, game_name):
    name_element = node.find('name')
    desc_element = node.find('desc')

    if name_element is not None and desc_element is not None:
        game_name = name_element.text.strip()
        translation = translate_text(desc_element.text)
        desc_element.text = translation

def process_xml(xml_file_path, output_file_path, status_label_var):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    total_games = len(list(root.iter('game')))
    for game_node in tqdm(root.iter('game'), total=total_games, desc="Traduzione in corso", unit="gioco"):
        name_element = game_node.find('name')
        game_name = name_element.text.strip() if name_element is not None else "Sconosciuto"
        translate_and_save(game_node, game_name)

    # Salva il file XML modificato
    tree.write(output_file_path, encoding="utf-8")
    status_label_var.set("Traduzione completata")

if __name__ == "__main__":
    root = Tk()
    root.title("Traduttore gamelist.xml")  
    root.geometry("400x300")

    selected_file_label_var = StringVar()
    status_label_var = StringVar()

    # Funzione lambda per passare argomenti alla funzione select_input_xml_file
    select_file_button = Button(root, text="Scegli File", command=lambda: select_input_xml_file(selected_file_label_var))
    select_file_button.pack(pady=10)

    selected_file_label = Label(root, textvariable=selected_file_label_var)
    selected_file_label.pack()

    status_label = Label(root, textvariable=status_label_var)
    status_label.pack()

    translate_button = Button(root, text="Traduci", command=lambda: process_xml(selected_file_label_var.get(), "gamelist_tradotto.xml", status_label_var))
    translate_button.pack(pady=10)

    root.mainloop()
