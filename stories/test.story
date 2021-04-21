Q:START:Si parte!
Sei pronto per iniziare?
A:1:Yes:jmp 001

Q:001:Questo è il titolo della domanda.
Dalla riga seguente inizia il testo.
Può essere impostata su più righe.
Ma nessuna riga deve iniziare con i marcatori speciali.

Possono esserci righe vuote.
La domanda finisce quando si trova la riga delle risposte.
Tutte le risposte fanno riferimento a questa domanda.
Le risposte vengono codificate con il numero da digitare
la risposta in testo e i comandi. Lo 0 non si può usare.
A:1:Uno:jmp 002
A:2:Perdi:jmp LOSE
A:3:Restart:jmp START
A:4:Aumenti il punteggio:scorejmp 5 003
A:5:Riduci il punteggio e perdi:scorejmp -5 LOSE

Q:002:Questo è il titolo della seconda domanda.
Testo
A:1:Vinci:jmp WIN

