// Funktion zum Laden von Tagebucheinträgen für einen bestimmten Benutzer
async function loadDiaryEntries(username, searchparameter) {
    // API-Endpunkt für Tagebucheinträge des Benutzers
    const apiUrl = `/api/diary?username=${username}&searchparameter=${searchparameter}`;

    try {
        // Lade die Tagebucheinträge vom Server
        const entries = await loadJSON(apiUrl);
        console.log(entries);

        // Holen Sie die HTML-Liste, in die die Einträge eingefügt werden sollen
        const entriesList = document.getElementById('diary-entries');

        // Iteriere durch die Einträge und erstelle jeweils eine Box
        entries.forEach(entry => {
            const div_row = createDiaryBox(entry.id, entry.entry_title, entry.entry_date, entry.entry_content);
            entriesList.appendChild(div_row);
        });

    } catch (error) {
        // Fehlerbehandlung: Bei einem Fehler weiterleiten zur Startseite
        console.error('Error fetching data:', error);
        window.location.href = "/";
    }
}

// Funktion zum Löschen eines Tagebucheintrags
async function deleteDiaryEntry(event) {
    // Extrahiere die ID des zu löschenden Eintrags aus dem Button
    var button = event.target.id;
    var delete_button = document.getElementById(button);
    const parent = delete_button.getAttribute("parent");
    var formdata = {
        "id": parent
    };

    try {
        // API-Endpunkt für das Löschen eines Tagebucheintrags
        const apiUrl = `/api/diary`;

        // Sende Anfrage zum Löschen an den Server
        const response = await deleteJSON(apiUrl, formdata);

        // Entferne die gelöschte Eintrag-Box aus dem DOM
        var entry = document.getElementById(parent);
        entry.remove();
    } catch (error) {
        // Fehlerbehandlung, falls das Löschen fehlschlägt
    }
}

// Funktion zum Hinzufügen eines neuen Tagebucheintrags
async function addDiaryEntry(event) {
    event.preventDefault();

    // Holen Sie sich Werte aus den Formularfeldern
    var title = document.getElementById("entry_title").value;
    var date = document.getElementById("entry_date").value;
    var content = document.getElementById("entry_content").value;

    // Überprüfen, ob alle Felder ausgefüllt sind
    if (title.trim() === '' || date.trim() === '' || content.trim() === '') {
        throw new Error('Tagebucheintrag unvollständig!');
    }

    // Formulardaten für den neuen Eintrag
    var formdata = {
        "username": urlParams.get('username'),
        "entry": {
            "entry_title": title,
            "entry_date": date,
            "entry_content": content
        }
    };

    try {
        // API-Endpunkt für das Hinzufügen eines Tagebucheintrags
        const apiUrl = `/api/diary`;

        // Sende Anfrage zum Hinzufügen an den Server
        const response = await postJSON(apiUrl, formdata);

        // Setze das Formular zurück und lade die Seite neu
        document.getElementById('diary-form').reset();
        document.getElementById('entry_date').value = formattedDate;
        location.reload();
    } catch (error) {
        // Fehlerbehandlung, falls das Hinzufügen fehlschlägt
        throw new Error('Nicht veröffentlicht!');
    }
}

// Überprüfe, ob ein Benutzername in den URL-Parametern vorhanden ist
const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username');
const searchparameter = urlParams.get('searchparameter');
if (username === null || username === undefined) {
    // Wenn kein Benutzername vorhanden ist, leite zur Startseite weiter
    window.location.href = "/";
}

// Holen Sie das aktuelle Datum und formatieren Sie es als yyyy-mm-dd
var currentDate = new Date();
var formattedDate = currentDate.toISOString().slice(0, 10);

// Setze den Wert des Datumsfeldes auf das heutige Datum
document.getElementById('entry_date').value = formattedDate;

// Lade vorhandene Tagebucheinträge für den Benutzer
loadDiaryEntries(username, searchparameter);

// Füge dem "Posten"-Button einen Eventlistener hinzu, der die Funktion zum Hinzufügen aufruft
document.getElementById('post-button').addEventListener('click', async function (event) {
    addDiaryEntry(event);
});

// Funktion zum Erstellen einer Box für einen Tagebucheintrag
function createDiaryBox(id, title, date, content) {
    const div_row = document.createElement('div');
    div_row.setAttribute("id", id)
    div_row.className = "row"
    const div_col = document.createElement("div");
    div_col.className = "col";
    const entryDiv = document.createElement("div");
    entryDiv.className = "card mt-3";

    // Erstelle und füge Titel mit Löschbutton hinzu
    var titleElement = document.createElement("div");
    titleElement.className = "card-header d-flex justify-content-between align-items-center";
    titleElement.textContent = title;

    // Erstelle den Löschbutton
    var deleteButton = document.createElement("button");
    deleteButton.setAttribute("parent", id);
    deleteButton.setAttribute("id", "delete_" + id);
    deleteButton.className = "btn btn-outline-danger btn-sm";
    deleteButton.innerHTML = "&times;"; // HTML-Code für das 'x'-Zeichen
    deleteButton.addEventListener("click", function (event) {
        deleteDiaryEntry(event);
    });

    // Füge den Löschbutton zum TitelElement hinzu
    titleElement.appendChild(deleteButton);
    entryDiv.appendChild(titleElement);

    // Erstelle und füge das Datum hinzu
    var dateElement = document.createElement("div");
    dateElement.className = "card-body text-muted";
    dateElement.textContent = date;
    entryDiv.appendChild(dateElement);

    // Erstelle und füge den Textinhalt hinzu
    var contentElement = document.createElement("div");
    contentElement.className = "card-body";
    contentElement.innerContent = content;
    entryDiv.appendChild(contentElement);

    div_col.appendChild(entryDiv);
    div_row.appendChild(div_col);
    return div_row;
}

document.getElementById("search-button").addEventListener("click", function () {
    const value = document.getElementById("search").value;
    const url = new URL(window.location.href);
    url.searchParams.set("searchparameter", value);
    window.location.href = url.toString();
});

document.getElementById('btn-clear').addEventListener('click', function () {
    document.getElementById('search').value = '';
    document.getElementById('search').focus();
});
