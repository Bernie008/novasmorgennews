# novasmorgennews

morgenpodcast.py erstellt aus den ersten 10 Nachrichten von tagesschau.de einen ca. 3-minütigen Podast als MP3.
Der Workflow wird täglich um 10 Uhr (UTC) ausgeführt.
Nach Erstellung des MP3 wird eine Mail an den eingetragenen Empfänger geschickt.

WICHTIG:
- Zur Erstellung des Podcast-Texts und der MP3 ist ein OpenAI-API-Key notwendig, der als Secret OPENAI_API_KEY angelegt wird.
- Der Versand der E-Mail erfordert weitere Secrets:
  - SMTP_SERVER	smtp.gmail.com
  - SMTP_PORT	465
  - EMAIL_USERNAME	dein.email@gmail.com
  - EMAIL_PASSWORD	Ein App-Passwort (nicht dein normales - kann z.B. im Google-Konto erzeugt werden)
  - EMAIL_RECIPIENT	empfänger@example.com
 
  
