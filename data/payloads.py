valid_payload = {
    "sellerID": 126612,
    "name": "test item",
    "price": 123,
    "statistics": {"likes": 1, "viewCount": 500, "contacts": 1000},
}


valid_payloads_value = [
    {
        "sellerID": 111111,
        "name": "Minimal item",
        "price": 1,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    },
    {
        "sellerID": 500000,
        "name": "Middle item",
        "price": 555555,
        "statistics": {"likes": 555555, "viewCount": 555555, "contacts": 555555},
    },
    {
        "sellerID": 999999,
        "name": "Maximal item",
        "price": 999999,
        "statistics": {"likes": 999999, "viewCount": 999999, "contacts": 999999},
    },
    {
        "sellerID": 999999,
        "name": "Maximal item",
        "price": 999999999999,
        "statistics": {
            "likes": 999999999999,
            "viewCount": 999999999999,
            "contacts": 999999999999,
        },
    },
    {
        "sellerID": 500000,
        "name": "null",
        "price": 0,
        "statistics": {"likes": 555, "viewCount": 555, "contacts": 555},
    },
    {
        "sellerID": 500000,
        "name": "null",
        "price": 555,
        "statistics": {"likes": 0, "viewCount": 555, "contacts": 555},
    },
    {
        "sellerID": 500000,
        "name": "null",
        "price": 555,
        "statistics": {"likes": 555, "viewCount": 0, "contacts": 555},
    },
    {
        "sellerID": 500000,
        "name": "null",
        "price": 555,
        "statistics": {"likes": 555, "viewCount": 555, "contacts": 0},
    },
]


invalid_payloads_list = [
    {
        "name": "Ivan",
        "price": 123,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    },  # miss sellerID
    {
        "sellerID": 126612,
        "price": 123,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    },  # miss name
    {
        "sellerID": 126612,
        "name": "test item",
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    },  # miss price
    {"sellerID": 126612, "name": "test item", "price": 123},  # miss statistics
    {
        "sellerID": 126612,
        "name": "test item",
        "price": 123,
        "statistics": {"viewCount": 1, "contacts": 1},
    },  # miss likes
    {
        "sellerID": 126612,
        "name": "test item",
        "price": 123,
        "statistics": {"likes": 1, "contacts": 1},
    },  # miss viewCount
    {
        "sellerID": 126612,
        "name": "test item",
        "price": 123,
        "statistics": {"likes": 1, "viewCount": 1},
    },  # miss contacts
    {"sellerID": 126612, "name": "test item", "price": 123, "likes": 1, "viewCount": 1},
]

invalid_payloads = (
    [
        # sellerID
        {
            "sellerID": val,
            "name": "test sellerID",
            "price": 123,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
        }
        for val in ["abc", "", " ", None, -1, 0, "@", "#", "%", "'", '"']
    ]
    + [
        # name
        {
            "sellerID": 126612,
            "name": val,
            "price": 123,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
        }
        for val in [123, "", None, -1, 0, " "]
    ]
    + [
        # price
        {
            "sellerID": 126612,
            "name": "test price",
            "price": val,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
        }
        for val in ["abc", "", " ", None, -1, "@", "#", "%"]
    ]
    + [
        # statistics
        {"sellerID": 126612, "name": "test statistics", "price": 123, "statistics": val}
        for val in [
            # none типы
            {"likes": None, "viewCount": 1, "contacts": 1},
            {"likes": 1, "viewCount": None, "contacts": 1},
            {"likes": 1, "viewCount": 1, "contacts": None},
            # строки
            {"likes": "", "viewCount": 1, "contacts": 1},
            {"likes": 1, "viewCount": "", "contacts": 1},
            {"likes": 1, "viewCount": 1, "contacts": ""},
            # отрицательные значения
            {"likes": -1, "viewCount": 1, "contacts": 1},
            {"likes": 1, "viewCount": -1, "contacts": 1},
            {"likes": 1, "viewCount": 1, "contacts": -1},
            # неверный тип
            {"likes": "a", "viewCount": 1, "contacts": 1},
            {"likes": 1, "viewCount": "a", "contacts": 1},
            {"likes": 1, "viewCount": 1, "contacts": "a"},
            # пробелы
            {"likes": " ", "viewCount": 1, "contacts": 1},
            {"likes": 1, "viewCount": " ", "contacts": 1},
            {"likes": 1, "viewCount": 1, "contacts": " "},
        ]
    ]
)

invalid_get_item_id_400 = [
    "abc",
    1,
    -1,
    0,
    1_1,
    None,
    " ",
    "&",
    "@",
    "$",
    "%",
    "!",
    "'",
    '"',
    "' OR 1=1",
    "<script>",
]

invalid_get_item_id_404 = [
    "#",
    "",
    "/",
    "///",
    "?",
]

invalid_get_item_id = [
    "abc",
    1,
    -1,
    0,
    None,
    "",
    " ",
    "@",
    "#",
    "$",
    "%",
    "!",
    "'",
    '"',
    "' OR 1=1",
    "<script>",
    "/",
    "///",
    "?",
    "&",
]

invalid_get_user_id = [
    "abc",
    -1,
    0,
    None,
    " ",
    "@",
    "#",
    "$",
    "%",
    "!",
    "'",
    '"',
    "' OR 1=1",
    "<script>",
    "?",
    "&",
]

payload_field = ["sellerID", "name", "price", "statistics"]
