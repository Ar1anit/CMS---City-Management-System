class User:

    def __init__(self, vorname, nachname, dob, email, passwort, auth_code, rechte, profilbild, lieblingsdatensatz, is_logged_in):
        self.vorname = vorname
        self.nachname = nachname
        self.dob = dob
        self.email = email
        self.passwort = passwort
        self.auth_code = auth_code
        self.rechte = rechte
        self.profilbild = profilbild
        self.lieblingsdatensatz = lieblingsdatensatz
        self.is_logged_in = is_logged_in
        self.added_diagrams = []
        self.profilinfo = "Ich liebe Datensätze"

    def __repr__(self):
        return f"User obj.: {self.email}."
