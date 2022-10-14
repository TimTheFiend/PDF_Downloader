# PDF Downloader

## Klargøring af Python v3.10
Dette program gør brug af en række forskellige *3rd-party libraries* som er noteret i [krav-filen](requirements.txt); for at programmet kan køre skal indholdet af filen installeres, hvilket gøres igennem `cmd.exe`, eller "Command Prompt".<br>I den følgende beskrivelse er der kun taget udgangspunkt i klargøring til Windows, samt at Python (minimum version 3.10) er installeret på forhånd.

### Command Prompt
Åbn et command prompt (vil blive omtalt som `cmd`), enten ved at gå ind i start-menuen og skrive navnet, eller ved at trykke tasterne `WIN+R` som åbner et `RUN` vindue, hvor der indtastes "cmd" efterfulgt af `Enter`. Et cmd-vindue burde være synligt.

### `pip` Installering
Naviger til filstien til dette projekt; Dette kan gøres med kommandoen `cd` efterfulgt af filstien.
Indtast følgende ind og vent på installationen færdiggøres:<br>
`pip install -r requirements.txt`<br>
Nu er Python klar til at kører programmet.

## Start programmet
Programmet kan startes via `cmd` ved at skrive: "`py -m main.py`".

## Indstillinger
For at køre programmet skal de relevante data indsættes i filen [constants.py](constants.py). Følgende linjer skal sættes for at programmet kan køre.<br>
### FILE/DIRECTORY INFORMATION
-  `EXCEL_FILEPATH`
   -  Skal pege på excel-filen hvor der skal læses fra.
-   `OUTPUT_DIR`
    -   Skal pege på den mappe hvor PDFerne skal gemmes på succesfuld download.
-   `FILE_STATUS_EXCEL_FILEPATH`
    -   Filstien på det Excel-ark som indeholder information om download statusen for alle elementer. Programmet står selv for at generere dokumentet.
-   `FILE_STATUS_EXCEL_SHEETNAME`
    -   Titlen på *sheet*et der bliver skrevet til.

**OBS!** Filstier skal starte med `r`, og være omgivet af enten `""` eller `''`

### SPREADSHEET -> COLUMN INFORMATION
- `ID_COL_NAME`
  - Navnet på kolonnen der indeholder rækkens ID (BRnum).
- `URL_COL_NAME`
  - Navnet på kolonnen der indeholder PDF URLs.
- `URL_BACKUP_COL_NAME`
  - Navnet på kolonnen der indeholder *backup* PDF URLs.

**OBS!** Ovenstående felter er case-sensitive.

### SETTING
- `NUMBER_OF_THREADS`
  - Antallet af [thread](https://docs.python.org/3/library/threading.html)s der skal gøres brug af til downloading. Værdien skal være et heltal.<br>**OBS!** Højre tal er ikke nødvendigvis lig med hurtigere eksekveringstid.
- `TIMEOUT_REQUEST_MAX`
  - Antallet i sekunder hvor lang tid en download må bruge på at forbinde til URLen. Vær opmærksom på at ved komma-værdier skal der bruges `.` i stedet for komma.<br>**OBS!** Højre tal har større chance for at forbinde, og vil derfor øge eksekveringstiden.