from taskbreaker.i18n import _
"""Regelbaserad nedbrytning av uppgifter till mikrosteg."""

# Nyckelord → steg-mallar för vanliga uppgifter
TASK_TEMPLATES = {
    "städa": {
        "keywords": ["städa", "städning", "rensa", "plocka"],
        "steps": [
            "Hämta en sopsäck och ställ den vid dörren",
            "Plocka upp allt skräp från golvet",
            "Lägg smutstvätt i tvättkorgen",
            "Torka av alla ytor med en trasa",
            "Dammsug golvet",
            "Töm papperskorgen",
            "Kolla att allt ser bra ut – klart!",
        ],
    },
    "diska": {
        "keywords": ["diska", "disk", "tallrikar"],
        "steps": [
            "Skrapa av matrester i soporna",
            "Fyll ho med varmt vatten och diskmedel",
            "Börja med glas och bestick",
            "Diska tallrikar och skålar",
            "Diska kastruller och stekpannor",
            "Skölj allt ordentligt",
            "Ställ upp allt på torkställ",
            "Torka av diskbänken",
        ],
    },
    "tvätta": {
        "keywords": ["tvätta", "tvätt", "kläder"],
        "steps": [
            "Sortera tvätten i vitt, mörkt och kulört",
            "Fyll maskinen (inte för fullt!)",
            "Häll i tvättmedel",
            "Välj rätt program och starta",
            "Häng upp tvätten när den är klar",
            "Vik och lägg in torra kläder",
        ],
    },
    "laga mat": {
        "keywords": ["laga mat", "matlagning", "middag", "lunch", "frukost", "laga"],
        "steps": [
            "Bestäm vad du ska laga",
            "Kolla att du har alla ingredienser",
            "Plocka fram ingredienser och redskap",
            "Följ receptet steg för steg",
            "Duka bordet",
            "Servera maten",
            "Ställ in rester i kylen",
        ],
    },
    "handla": {
        "keywords": ["handla", "affären", "köpa", "inköp"],
        "steps": [
            "Skriv en inköpslista",
            "Kolla vad du redan har hemma",
            "Ta med påsar och plånbok",
            "Gå till affären",
            "Handla enligt listan",
            "Betala i kassan",
            "Packa upp varorna hemma",
        ],
    },
    "plugga": {
        "keywords": ["plugga", "studera", "läsa", "läxa", "prov", "tenta"],
        "steps": [
            "Välj vad du ska plugga på",
            "Stäng av distraktioner (mobil, sociala medier)",
            "Läs igenom materialet en gång snabbt",
            "Gör anteckningar av det viktigaste",
            "Testa dig själv på det du läst",
            "Ta en kort paus (5 min)",
            "Repetera det du hade svårt för",
        ],
    },
    "träna": {
        "keywords": ["träna", "träning", "gym", "springa", "motion"],
        "steps": [
            "Ta på dig träningskläder",
            "Fyll vattenflaskan",
            "Gör 5 minuters uppvärmning",
            "Kör ditt träningspass",
            "Stretcha i 5 minuter",
            "Duscha och byt om",
        ],
    },
    "mejl": {
        "keywords": ["mejl", "mail", "e-post", "svara"],
        "steps": [
            "Öppna mejlen",
            "Läs igenom det viktigaste först",
            "Svara på korta mejl direkt",
            "Markera mejl som kräver längre svar",
            "Skriv längre svar ett i taget",
            "Kolla att allt viktigt är besvarat",
        ],
    },
}


def break_down_task(task_text: str) -> list[str]:
    """Bryt ner en uppgift till mikrosteg.

    Försöker matcha mot kända mallar först.
    Om ingen mall matchar, skapar generella steg.
    """
    task_lower = task_text.lower().strip()

    # Matcha mot mallar
    for template in TASK_TEMPLATES.values():
        for keyword in template["keywords"]:
            if keyword in task_lower:
                return template["steps"]

    # Generell nedbrytning om ingen mall matchar
    return _generic_breakdown(task_text)


def _generic_breakdown(task_text: str) -> list[str]:
    """Skapa generella mikrosteg för en okänd uppgift."""
    task = task_text.strip().rstrip(".")
    return [
        f"Bestäm exakt vad '{task}' innebär",
        "Samla ihop det du behöver",
        "Börja med den enklaste delen",
        "Gör nästa del",
        "Kontrollera att allt blev rätt",
        "Klart! Bra jobbat!",
    ]
