Komunikacja pomiędzy klientem a serwerem odbywa się przy pomocy datagramów. Klient wysyła datagram zawierający liczby, serwer odpowiada datagramem zawierającym pojedynczą liczbę (obliczoną sumę) bądź komunikat o błędzie.

Zawartość datagramów interpretujemy jako tekst w ASCII. Ciągi cyfr ASCII interpretujemy jako liczby dziesiętne. Datagram może zawierać albo cyfry i spacje, albo pięć znaków składających się na słowo „ERROR”; żadne inne znaki nie są dozwolone (ale patrz następny akapit).