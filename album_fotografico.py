def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file.readline()
            for riga in file:
                if not riga.strip():
                    continue # Salta le righe vuote

                foto = riga.strip().split(",")
                foto[3] = int(foto[3])
                foto[4] = int(foto[4])
                anno = foto[4]

                trovato = False
                for gruppo in album:
                    if gruppo[0] == anno:
                        gruppo[1].append(foto)
                        trovato = True
                        break

                if not trovato:
                    album.append([anno, [foto]])

    except FileNotFoundError:
        return None
    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album e al file."""

    if mese < 1 or mese > 12:
        return None

    # Controlla che il codice non sia già presente.
    if cerca_foto(album, codice) is not None:
        return None

    foto = [codice, titolo, autore, mese, anno]

    # Scrive la nuova foto in fondo al file.
    try:
        with open(file_path, "r+", encoding="utf-8") as file:
            # "r+" apre un file esistente sia in lettura sia in scrittura
            contenuto = file.read()

            # Dopo read() siamo alla fine del file.
            # Se manca l'ultimo a capo, lo aggiungiamo.
            if contenuto and not contenuto.endswith("\n"): # if contenuto controlla che il file non sia vuoto
                file.write("\n")

            file.write(f"{codice},{titolo},{autore},{mese},{anno}\n")

    except OSError:
        return None

    # Cerca il gruppo dell'anno e aggiunge la foto.
    for gruppo in album:
        if gruppo[0] == anno:
            gruppo[1].append(foto)
            return foto

    # Se l'anno non esiste, crea un nuovo gruppo.
    album.append([anno, [foto]])
    return foto



def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # l’album contiene più gruppi, uno per ogni anno. Ogni gruppo contiene nella posizione 0 l’anno
    # e nella posizione 1 una lista di foto.
    for gruppo in album:
        for foto in gruppo[1]:
            if foto[0] == codice:
                return f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {foto[4]}"
    return None




def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    for gruppo in album:
        if gruppo[0] == anno:
            titoli = []
            for foto in gruppo[1]:
                titoli.append(foto[1])
            return sorted(titoli)
    return None



def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
