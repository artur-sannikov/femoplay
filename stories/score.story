Q:START:Prova dello score
Sei pronto per iniziare?
A:1:SI:scorejmp 01 2

Q:01:Primo bivio
Hai aumentato il punteggio.

Se arrivi a zero esci, altrimenti rimani qui a vita!

A:1:Diminuiscilo:scorejmp 01 -1
A:2:Aumentalo:scorejmp 01 1

