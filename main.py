"""Wildcat Explorer: an educational website built with Drafter."""

from dataclasses import dataclass
from bakery import assert_equal
from drafter import *


# A global constant is allowed by the project rubric.
STATUSES = [
    "Least Concern",
    "Near Threatened",
    "Vulnerable",
    "Endangered",
    "Critically Endangered",
]


@dataclass
class Wildcat:
    """Store the information shown for one wildcat."""

    name: str
    scientific_name: str
    size: str
    habitat: str
    status: str
    description: str


@dataclass
class State:
    """Store the collection and information that changes as people use the site."""

    wildcats: list[Wildcat]
    favorites: list[str]
    search_text: str
    selected_status: str
    profile_visits: int


def create_wildcats() -> list[Wildcat]:
    """Create the starting collection of wildcats."""
    return [
        Wildcat(
            "Snow Leopard",
            "Panthera uncia",
            "30-55 inches long",
            "Mountains of Central Asia",
            "Vulnerable",
            "Thick fur and a long tail help snow leopards stay warm and balance.",
        ),
        Wildcat(
            "Caracal",
            "Caracal caracal",
            "2-3 feet long",
            "Africa, the Middle East, and parts of Asia",
            "Least Concern",
            "Caracals are known for their long ears with black tufts.",
        ),
        Wildcat(
            "Serval",
            "Leptailurus serval",
            "2-3 feet long",
            "Grasslands and wetlands in Africa",
            "Least Concern",
            "Servals have long legs and large ears that help them hunt.",
        ),
        Wildcat(
            "Ocelot",
            "Leopardus pardalis",
            "2-3 feet long",
            "Forests and grasslands in Central and South America",
            "Least Concern",
            "Ocelots have spotted coats that help them blend in.",
        ),
        Wildcat(
            "Pallas's Cat",
            "Otocolobus manul",
            "18-26 inches long",
            "Grasslands and rocky areas in Central Asia",
            "Least Concern",
            "Pallas's cats have round faces and thick fur.",
        ),
        Wildcat(
            "Fishing Cat",
            "Prionailurus viverrinus",
            "2-3 feet long",
            "Wetlands and rivers in Asia",
            "Vulnerable",
            "Fishing cats are strong swimmers and hunt near water.",
        ),
        Wildcat(
            "African Wildcat",
            "Felis lybica",
            "18-30 inches long",
            "Africa and parts of the Middle East",
            "Least Concern",
            "African wildcats are closely related to domestic cats.",
        ),
        Wildcat(
            "Canada Lynx",
            "Lynx canadensis",
            "2-3 feet long",
            "Forests in Canada and Alaska",
            "Least Concern",
            "Canada lynxes have large paws that help them walk on snow.",
        ),
    ]


def find_wildcat(state: State, name: str) -> Wildcat | None:
    """Find a wildcat by name, ignoring capitalization and extra spaces."""
    wanted_name = name.strip().casefold()
    for wildcat in state.wildcats:
        if wildcat.name.casefold() == wanted_name:
            return wildcat
    return None


@route
def index(state: State) -> Page:
    """Show the welcome page and links to the site's features."""
    return Page(
        state,
        [
            Header("Wildcat Explorer"),
            "Welcome to Wildcat Explorer!",
            "Learn about wildcat size, habitat, and conservation status.",
            Button("Explore Wildcats", "explore"),
            Button("Wildcat Profiles", "profile"),
            Button("Search Wildcats", "search"),
            Button("Conservation Status", "conservation"),
            Button("My Favorites", "favorites"),
        ],
    )


@route
def explore(state: State) -> Page:
    """List the wildcats and let visitors update their favorites."""
    content = [
        Header("Explore Wildcats"),
        "Here are the wildcats in our collection:",
    ]

    for wildcat in state.wildcats:
        content.extend(
            [
                Header(wildcat.name),
                "Scientific name: " + wildcat.scientific_name,
                "Size: " + wildcat.size,
                "Habitat: " + wildcat.habitat,
                "Conservation status: " + wildcat.status,
            ]
        )
        if wildcat.name in state.favorites:
            content.append(
                Button(
                    "Remove Favorite",
                    "toggle_favorite",
                    arguments=[("wildcat_name", wildcat.name)],
                )
            )
        else:
            content.append(
                Button(
                    "Add to Favorites",
                    "toggle_favorite",
                    arguments=[("wildcat_name", wildcat.name)],
                )
            )

    content.extend(
        [
            "Want to add a wildcat to the collection?",
            Button("Add a Wildcat", "add_wildcat"),
            Button("Home", "index"),
        ]
    )
    return Page(state, content)


@route
def profile(state: State) -> Page:
    """Show a form for looking up a full wildcat profile."""
    return Page(
        state,
        [
            Header("Wildcat Profiles"),
            "Enter the name of a wildcat to learn more about it.",
            TextBox("wildcat_name"),
            Button("Find Wildcat", "show_profile"),
            Button("Home", "index"),
        ],
    )


@route
def show_profile(state: State, wildcat_name: str) -> Page:
    """Show one wildcat's full profile and count the profile lookup."""
    state.profile_visits += 1
    wildcat = find_wildcat(state, wildcat_name)
    content = [Header("Wildcat Profile")]

    if wildcat is None:
        content.append("Sorry, that wildcat was not found. Check the spelling and try again.")
    else:
        content.extend(
            [
                Header(wildcat.name),
                "Scientific name: " + wildcat.scientific_name,
                "Size: " + wildcat.size,
                "Habitat: " + wildcat.habitat,
                "Conservation status: " + wildcat.status,
                wildcat.description,
            ]
        )

    content.extend(
        [Button("Search Again", "profile"), Button("Home", "index")]
    )
    return Page(state, content)


@route
def search(state: State) -> Page:
    """Show a form for searching wildcat names."""
    return Page(
        state,
        [
            Header("Search Wildcats"),
            "Enter all or part of a wildcat's name:",
            TextBox("search_term", state.search_text),
            Button("Search", "do_search"),
            Button("Home", "index"),
        ],
    )


@route
def do_search(state: State, search_term: str) -> Page:
    """Find and display every wildcat whose name contains the search text."""
    state.search_text = search_term.strip()
    content = [Header("Search Results")]
    matches = []

    for wildcat in state.wildcats:
        if state.search_text.casefold() in wildcat.name.casefold():
            matches.append(wildcat)

    if matches:
        for wildcat in matches:
            content.extend(
                [
                    Header(wildcat.name),
                    "Size: " + wildcat.size,
                    "Habitat: " + wildcat.habitat,
                    "Status: " + wildcat.status,
                ]
            )
    else:
        content.append("No wildcats matched your search.")

    content.extend([Button("Search Again", "search"), Button("Home", "index")])
    return Page(state, content)


@route
def conservation(state: State) -> Page:
    """Show the conservation status filter form."""
    return Page(
        state,
        [
            Header("Conservation Status"),
            "Choose a conservation status:",
            SelectBox("status", STATUSES),
            Button("Filter Wildcats", "filter_conservation"),
            Button("Home", "index"),
        ],
    )


@route
def filter_conservation(state: State, status: str) -> Page:
    """Show all wildcats with the chosen conservation status."""
    state.selected_status = status
    content = [Header("Conservation Results")]
    matches = []

    for wildcat in state.wildcats:
        if wildcat.status == state.selected_status:
            matches.append(wildcat)

    if matches:
        for wildcat in matches:
            content.extend(
                [Header(wildcat.name), "Status: " + wildcat.status]
            )
    else:
        content.append("No wildcats have this status.")

    content.extend(
        [Button("Filter Again", "conservation"), Button("Home", "index")]
    )
    return Page(state, content)


@route
def favorites(state: State) -> Page:
    """Show saved favorites and a form for updating them by name."""
    content = [Header("My Favorite Wildcats"), "Your favorites:"]

    if not state.favorites:
        content.append("You have not added any favorites yet.")
    else:
        for favorite in state.favorites:
            content.append(favorite)

    content.extend(
        [
            "Enter a wildcat name to add or remove it:",
            TextBox("wildcat_name"),
            Button("Update Favorites", "toggle_favorite"),
            Button("Home", "index"),
        ]
    )
    return Page(state, content)


@route
def toggle_favorite(state: State, wildcat_name: str) -> Page:
    """Add a wildcat to favorites or remove it if it is already saved."""
    wildcat = find_wildcat(state, wildcat_name)
    if wildcat is None:
        return Page(
            state,
            [
                Header("Wildcat Not Found"),
                "Enter the name of a wildcat in the collection.",
                Button("View Favorites", "favorites"),
                Button("Explore Wildcats", "explore"),
            ],
        )

    if wildcat.name in state.favorites:
        state.favorites.remove(wildcat.name)
        message = wildcat.name + " was removed from your favorites."
    else:
        state.favorites.append(wildcat.name)
        message = wildcat.name + " was added to your favorites."

    return Page(
        state,
        [
            Header("Favorites Updated"),
            message,
            Button("View Favorites", "favorites"),
            Button("Home", "index"),
        ],
    )


@route
def add_wildcat(state: State) -> Page:
    """Show the form for adding a wildcat to the collection."""
    return Page(
        state,
        [
            Header("Add a Wildcat"),
            "Enter information about the wildcat you want to add.",
            "Name:",
            TextBox("name"),
            "Scientific name:",
            TextBox("scientific_name"),
            "Size:",
            TextBox("size"),
            "Habitat:",
            TextBox("habitat"),
            "Conservation status:",
            SelectBox("status", STATUSES),
            "Description:",
            TextArea("description", "", rows=4),
            Button("Save Wildcat", "save_wildcat"),
            Button("Home", "index"),
        ],
    )


@route
def save_wildcat(
    state: State,
    name: str,
    scientific_name: str,
    size: str,
    habitat: str,
    status: str,
    description: str,
) -> Page:
    """Validate the submitted details and add a new wildcat."""
    name = name.strip()
    scientific_name = scientific_name.strip()
    size = size.strip()
    habitat = habitat.strip()
    description = description.strip()

    if not name or not scientific_name or not size or not habitat or not description:
        return Page(
            state,
            [
                Header("Missing Information"),
                "Please complete every field before saving.",
                Button("Go Back", "add_wildcat"),
            ],
        )

    if find_wildcat(state, name) is not None:
        return Page(
            state,
            [
                Header("Wildcat Already Exists"),
                "That wildcat is already in the collection.",
                Button("Go Back", "add_wildcat"),
            ],
        )

    if status not in STATUSES:
        return Page(
            state,
            [
                Header("Invalid Conservation Status"),
                "Please choose a status from the list.",
                Button("Go Back", "add_wildcat"),
            ],
        )

    state.wildcats.append(
        Wildcat(name, scientific_name, size, habitat, status, description)
    )
    return Page(
        state,
        [
            Header("Wildcat Saved!"),
            name + " has been added to the collection.",
            Button("Explore Wildcats", "explore"),
            Button("Add Another Wildcat", "add_wildcat"),
            Button("Home", "index"),
        ],
    )


def run_route_tests() -> None:
    """Use assert_equal to check that all routes work and update state correctly."""
    state = State(create_wildcats(), [], "", "", 0)
    assert_equal(index(state) is not None, True)
    assert_equal(explore(state) is not None, True)
    assert_equal(profile(state) is not None, True)
    show_profile(state, "Caracal")
    assert_equal(state.profile_visits, 1)
    assert_equal(search(state) is not None, True)
    do_search(state, "  lynx  ")
    assert_equal(state.search_text, "lynx")
    assert_equal(conservation(state) is not None, True)
    filter_conservation(state, "Vulnerable")
    assert_equal(state.selected_status, "Vulnerable")
    assert_equal(favorites(state) is not None, True)
    toggle_favorite(state, "caracal")
    assert_equal(state.favorites, ["Caracal"])
    assert_equal(add_wildcat(state) is not None, True)
    original_count = len(state.wildcats)
    save_wildcat(
        state,
        "Pampas Cat",
        "Leopardus colocola",
        "18-30 inches long",
        "Grasslands in South America",
        "Least Concern",
        "A small wildcat found in South America.",
    )
    assert_equal(len(state.wildcats), original_count + 1)


set_website_title("Wildcat Explorer")
set_site_information(
    "Taylor Huff",
    "Learn about wildcat size, habitat, and conservation status.",
    "Sources: Add the sources you used to research each wildcat.",
    "Planning: An interactive guide to wildcats and their conservation.",
    "Links: Add links to your research sources here.",
)


run_route_tests()
start_server(State(create_wildcats(), [], "", "", 0))

