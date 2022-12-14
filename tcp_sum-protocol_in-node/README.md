> **Note**
> Zamiast samej specyfikacji jest implementacja w Node.js

Napisz specyfikację strumieniowego protokołu sumowania liczb. Dopuść możliwość przesyłania przez jedno połączenie wielu ciągów liczb do zsumowania i wielu odpowiedzi (obliczonych sum albo komunikatów o wystąpieniu błędu). Zastanów się, czego użyć jako terminatora mówiącego „w tym miejscu kończy się ciąg liczb” — dwuznaku \r\n, tak jak w wielu innych protokołach sieciowych? A może czegoś innego (ale wtedy miej jakieś uzasadnienie odejścia od powszechnie przyjętej konwencji)? Czy odpowiedzi serwera będą używać takiego samego terminatora?

Rozważ, czy trzeba do specyfikacji dodawać warunek ograniczający długość przesyłanych przez klienta zapytań, np. 1024 bajty łącznie z terminatorem. To ułatwiłoby implementowanie serwera, bo dzięki temu programista piszący serwer mógłby zadeklarować roboczy bufor o rozmiarze 1024 bajtów i to na pewno wystarczyłoby, aby wczytać do niego całe zapytanie. Ale czy to jest niezbędne? Czy problem dodawania liczb wymaga, aby serwer odebrał całe zapytanie, zanim zacznie je przetwarzać?

Zastanów się nad algorytmem serwera. Będzie on musiał być bardziej złożony niż w przypadku serwera UDP. Tam pojedyncza operacja odczytu zawsze zwracała jeden kompletny datagram, czyli jeden kompletny ciąg liczb do zsumowania. W przypadku połączeń TCP niestety tak łatwo nie jest.

Po pierwsze, jeśli klient od razu po nawiązaniu połączenia wysłał kilka zapytań jedno za drugim, to serwer może je odebrać sklejone ze sobą. Pojedyncza operacja odczytu ze strumienia może np. zwrócić 15 bajtów odpowiadających znakom 2 2\r\n10 22 34\r\n — jak widać są to dwa ciągi liczb. Serwer w odpowiedzi powinien zwrócić 4\r\n66\r\n.

Po drugie, operacja odczytu może zwrócić tylko początkową część zapytania. Kod serwera musi wtedy ponownie wywołać read(). Takie ponawianie odczytów i odbieranie kolejnych fragmentów ciągu liczb musi trwać aż do chwili odebrania \r\n — dopiero wtedy wiemy, że dotarliśmy do końca zapytania.

Po trzecie, mogą się zdarzyć oba powyższe przypadki równocześnie. Serwer może np. odczytać ze strumienia 9 bajtów odpowiadających znakom 2 2\r\n10 2.