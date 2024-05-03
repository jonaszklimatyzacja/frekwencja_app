frekwencja_app to program obliczający stosunek obecności do nieobecności względem poszczególnej jednostki lekcyjnej.
Działa on dla dziennika Vulcan używając Vulcan API
https://www.vulcan.edu.pl/
https://github.com/kapi2289/vulcan-api

Upewnij się, że uruchamiasz program w wersji pythona nie innej niż 3.11
https://www.python.org/downloads/
W innych wersjach nie działa vulcan-api

Do poprawnego działania programu potrzebne jest zainstalowanie biblioteki vulcan-api
Jeśli masz pythona w wersji 3.11 to możesz to zrobić za pomocą pliku install_vulcan_api.bat

W aplikacji należy podać 3 wartości (Token, Symbol, PIN), które znajdziemy w Uczeń > Dostęp mobilny > Wygeneruj kod dostępu
Po logowaniu program połączy się z naszym kontem tak jak dziennik mobilny i nie będzie wymagane dalsze logowanie

Program uruchamiamy za pomocą pliku run.bat

Mogą pojawić się rekordy lekcji, których aktualnie nie ma w planie. Kod pobiera WSZYSTKIE wpisy o frekwencji, jakie zostały dodane w tym roku szkolnym, wystąpienie takich anomalii może oznaczać, że kiedyś została w tym miejscu wpisana lekcja.