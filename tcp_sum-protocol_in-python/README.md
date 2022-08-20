Komunikacja pomiędzy klientem a serwerem odbywa się przy pomocy połączenia strumieniowego. Klient wysyła jedną lub więcej linii zawierających liczby. Dla każdej odebranej linii serwer zwraca linię zawierającą pojedynczą liczbę (obliczoną sumę) bądź komunikat o błędzie.

Ogólna definicja linii jest zapożyczona z innych protokołów tekstowych: ciąg drukowalnych znaków ASCII (być może pusty) zakończony dwuznakiem \r\n.

Linia z liczbami zawierać może tylko cyfry i spacje. Ciągi cyfr należy interpretować jako liczby dziesiętne. Spacje służą jako separatory liczb, każda spacja musi znajdować się pomiędzy dwiema cyframi. Linia nie może być pusta, musi zawierać przynajmniej jedną liczbę.

Linia sygnalizująca niemożność poprawnego obliczenia sumy zawiera pięć liter składających się na słowo „ERROR” (po tych literach oczywiście jest jeszcze terminator linii, czyli \r\n).

Serwer może, ale nie musi, zamykać połączenie w reakcji na nienaturalne zachowanie klienta. Obejmuje to wysyłanie danych binarnych zamiast znaków ASCII, wysyłanie linii o długości przekraczającej przyjęty w kodzie źródłowym serwera limit, długi okres nieaktywności klienta, itd. Jeśli serwer narzuca maksymalną długość linii, to limit ten powinien wynosić co najmniej 1024 bajty (1022 drukowalne znaki i dwubajtowy terminator linii).

Serwer nie powinien zamykać połączenia jeśli udało mu się odebrać poprawną linię w sensie ogólnej definicji, ale dane w niej zawarte są niepoprawne (np. oprócz cyfr i spacji są przecinki). Powinien wtedy zwracać komunikat o błędzie i przechodzić do przetwarzania następnej linii przesłanej przez klienta.

Serwer powinien zwracać komunikat błędu również wtedy, gdy przesłane przez klienta liczby bądź ich suma przekraczają zakres typu całkowitoliczbowego wykorzystywanego przez serwer do prowadzenia obliczeń.