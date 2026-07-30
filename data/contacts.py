"""Per-country contact pools for order create from/to data (index 0-9)."""

from __future__ import annotations

import random
from typing import Any, TypedDict


class Contact(TypedDict):
    name: str
    phone_number: str
    email: str
    address1: str
    postcode: str


CONTACTS: dict[str, list[Contact]] = {
    "sg": [
        {
            "name": "Dini Shipper",
            "phone_number": "+6582410442",
            "email": "diniseprilia@gmail.com",
            "address1": "1 Raffles Blvd, Singapore",
            "postcode": "039593",
        },
        {
            "name": "Marie Anne",
            "phone_number": "+6581320334",
            "email": "marie.anne@gmail.com",
            "address1": "Blk 101 Pasir Ris Drive #14-092",
            "postcode": "519111",
        },
        {
            "name": "Wei Ming Tan",
            "phone_number": "+6591234567",
            "email": "weiming.tan@example.com",
            "address1": "10 Bayfront Avenue, Marina Bay Sands",
            "postcode": "018956",
        },
        {
            "name": "Sarah Lim",
            "phone_number": "+6598765432",
            "email": "sarah.lim@example.com",
            "address1": "3 Church Street, Samsung Hub",
            "postcode": "049483",
        },
        {
            "name": "Ahmad Rahman",
            "phone_number": "+6587654321",
            "email": "ahmad.rahman@example.com",
            "address1": "Blk 55 Changi Road #02-15",
            "postcode": "419909",
        },
        {
            "name": "Priya Nair",
            "phone_number": "+6581122334",
            "email": "priya.nair@example.com",
            "address1": "1 HarbourFront Walk, VivoCity",
            "postcode": "098585",
        },
        {
            "name": "Jason Ong",
            "phone_number": "+6593344556",
            "email": "jason.ong@example.com",
            "address1": "68 Orchard Road, Plaza Singapura",
            "postcode": "238839",
        },
        {
            "name": "Emily Koh",
            "phone_number": "+6585566778",
            "email": "emily.koh@example.com",
            "address1": "Blk 233 Bishan Street 22 #08-120",
            "postcode": "570233",
        },
        {
            "name": "Daniel Chua",
            "phone_number": "+6596677889",
            "email": "daniel.chua@example.com",
            "address1": "2 Jurong East Street 21, IMM Building",
            "postcode": "609601",
        },
        {
            "name": "Nurul Hassan",
            "phone_number": "+6587788990",
            "email": "nurul.hassan@example.com",
            "address1": "Blk 308 Clementi Avenue 4 #05-345",
            "postcode": "120308",
        },
    ],
    "my": [
        {
            "name": "Aisyah Binti Ali",
            "phone_number": "+60123456789",
            "email": "aisyah.ali@example.com",
            "address1": "No. 12 Jalan Ampang, Kuala Lumpur",
            "postcode": "50450",
        },
        {
            "name": "Wei Jie Chong",
            "phone_number": "+60198765432",
            "email": "weijie.chong@example.com",
            "address1": "88 Jalan Bukit Bintang, KL",
            "postcode": "55100",
        },
        {
            "name": "Siti Nurhaliza",
            "phone_number": "+60111222333",
            "email": "siti.nur@example.com",
            "address1": "15 Persiaran KLCC, Petronas Twin Towers",
            "postcode": "50088",
        },
        {
            "name": "Rajesh Kumar",
            "phone_number": "+60122334455",
            "email": "rajesh.kumar@example.com",
            "address1": "23 Jalan Tun Razak, Kuala Lumpur",
            "postcode": "50400",
        },
        {
            "name": "Mei Ling Wong",
            "phone_number": "+60133445566",
            "email": "meiling.wong@example.com",
            "address1": "Lot 10, Mid Valley Megamall, KL",
            "postcode": "59200",
        },
        {
            "name": "Hafiz Abdullah",
            "phone_number": "+60144556677",
            "email": "hafiz.abdullah@example.com",
            "address1": "No. 5 Jalan Sultan Ismail, KL",
            "postcode": "50250",
        },
        {
            "name": "Farah Zainal",
            "phone_number": "+60155667788",
            "email": "farah.zainal@example.com",
            "address1": "45 Jalan Imbi, Bukit Bintang",
            "postcode": "55100",
        },
        {
            "name": "Kelvin Tee",
            "phone_number": "+60166778899",
            "email": "kelvin.tee@example.com",
            "address1": "1 Jalan Dutamas 1, Solaris Dutamas",
            "postcode": "50480",
        },
        {
            "name": "Amira Hassan",
            "phone_number": "+60177889900",
            "email": "amira.hassan@example.com",
            "address1": "G-12 Publika Shopping Gallery, KL",
            "postcode": "50480",
        },
        {
            "name": "Benjamin Lee",
            "phone_number": "+60188990011",
            "email": "benjamin.lee@example.com",
            "address1": "No. 9 Jalan P. Ramlee, Kuala Lumpur",
            "postcode": "50250",
        },
    ],
    "id": [
        {
            "name": "Budi Santoso",
            "phone_number": "+6281234567890",
            "email": "budi.santoso@example.com",
            "address1": "Jl. Sudirman No. 1, Jakarta Pusat",
            "postcode": "10220",
        },
        {
            "name": "Siti Aminah",
            "phone_number": "+6281298765432",
            "email": "siti.aminah@example.com",
            "address1": "Jl. Thamrin No. 10, Jakarta",
            "postcode": "10230",
        },
        {
            "name": "Andi Wijaya",
            "phone_number": "+6282111223344",
            "email": "andi.wijaya@example.com",
            "address1": "Jl. Gatot Subroto Kav. 52, Jakarta",
            "postcode": "12710",
        },
        {
            "name": "Dewi Lestari",
            "phone_number": "+6282233445566",
            "email": "dewi.lestari@example.com",
            "address1": "Jl. Melawai Raya No. 15, Blok M",
            "postcode": "12160",
        },
        {
            "name": "Rizky Pratama",
            "phone_number": "+6282344556677",
            "email": "rizky.pratama@example.com",
            "address1": "Jl. Kemang Raya No. 8, Jakarta Selatan",
            "postcode": "12730",
        },
        {
            "name": "Putri Ayu",
            "phone_number": "+6282455667788",
            "email": "putri.ayu@example.com",
            "address1": "Jl. Senopati No. 22, Jakarta Selatan",
            "postcode": "12190",
        },
        {
            "name": "Agus Setiawan",
            "phone_number": "+6282566778899",
            "email": "agus.setiawan@example.com",
            "address1": "Jl. Asia Afrika No. 8, Bandung",
            "postcode": "40111",
        },
        {
            "name": "Maya Sari",
            "phone_number": "+6282677889900",
            "email": "maya.sari@example.com",
            "address1": "Jl. Tunjungan No. 5, Surabaya",
            "postcode": "60275",
        },
        {
            "name": "Fajar Nugroho",
            "phone_number": "+6282788990011",
            "email": "fajar.nugroho@example.com",
            "address1": "Jl. Malioboro No. 60, Yogyakarta",
            "postcode": "55213",
        },
        {
            "name": "Indah Permata",
            "phone_number": "+6282899001122",
            "email": "indah.permata@example.com",
            "address1": "Jl. Teuku Umar No. 12, Denpasar",
            "postcode": "80114",
        },
    ],
}


def get_contacts(country: str) -> list[Contact]:
    key = country.strip().lower()
    contacts = CONTACTS.get(key)
    if not contacts:
        raise ValueError(f"No contact pool for country={country!r}")
    return contacts


def resolve_contact(country: str, selector: str) -> Contact:
    """Resolve contact by 'Random' or 'index-N' (0-9)."""
    contacts = get_contacts(country)
    raw = selector.strip()
    lowered = raw.lower()

    if lowered == "random":
        return random.choice(contacts)

    if lowered.startswith("index-"):
        try:
            index = int(lowered.split("-", 1)[1])
        except ValueError as exc:
            raise ValueError(
                f"Invalid from_data/to_data selector {selector!r}. Use Random or index-0..9"
            ) from exc
        if index < 0 or index >= len(contacts):
            raise ValueError(
                f"Contact index {index} out of range for {country} "
                f"(valid: 0-{len(contacts) - 1})"
            )
        return contacts[index]

    raise ValueError(
        f"Invalid from_data/to_data selector {selector!r}. Use Random or index-0..9"
    )


def contact_to_party(contact: Contact, country_code: str) -> dict[str, Any]:
    return {
        "name": contact["name"],
        "phone_number": contact["phone_number"],
        "email": contact["email"],
        "address": {
            "address1": contact["address1"],
            "country": country_code.upper(),
            "postcode": contact["postcode"],
        },
    }
