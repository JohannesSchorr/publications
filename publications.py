import requests
import logging
import json
import http.client


http.client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


ORCID_API = "https://pub.orcid.org/v3.0/"


def fetch_data(orcid: str, put_code: str = "") -> dict:
    """ """
    api_address = f"{ORCID_API}{orcid}/works/{put_code}"
    with requests.Session() as s:
        print("start request")
        r = s.get(
            api_address,
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
            },
        )
        print("finished request")
        if r.status_code != 200:
            raise ValueError()

        return json.loads(r.text)


def collect_put_codes(overview_data: dict) -> list[int]:
    return [data["work-summary"][0]["put-code"] for data in overview_data["group"]]


def value(entry_data: dict, key: str) -> str:
    if isinstance(entry_data, dict):
        if key in list(entry_data.keys()):
            if entry_data[key] is not None and "value" in list(entry_data[key].keys()):
                return entry_data[key]["value"]
    return ""


class Person:
    def __init__(self, entry_data: str):
        self.entry_data = entry_data
        self.name = self.get_name()

    def get_name(self) -> str:
        return self.entry_data["credit-name"]["value"]

    def first_name(self) -> str:
        if ", " in self.name:
            split_position = self.name.find(", ")
            return self.name[split_position + 1 :]
        else:
            reversed_name = self.name[::-1]
            split_position = reversed_name.find(" ")
            return self.name[:-split_position]

    def last_name(self) -> str:
        if ", " in self.name:
            split_position = self.name.find(", ")
            return self.name[:split_position]
        else:
            reversed_name = self.name[::-1]
            split_position = reversed_name.find(" ")
            return self.name[-split_position:]

    def print_name(self) -> str:
        return f"{self.last_name()}, {self.first_name()[0]}."

    def e_mail(self) -> str:
        return self.entry_data["contributor-email"]

    def orcid_address(self) -> str:
        return self.entry_data["contributor-orcid"]["uri"]

    def role(self) -> str:
        if self.entry_data["contributor-attributes"] == None:
            return ""
        return self.entry_data["contributor-attributes"]["contributor-role"]

    def is_autor(self) -> bool:
        if self.role() == "author":
            return True
        elif "writing" in self.role():
            return True
        else:
            return False

    def is_editor(self) -> bool:
        if self.role() == "editor":
            return True
        else:
            return False

    def link_address(self) -> str:
        if self.orcid_address() is not None:
            return self.orcid_address()
        elif self.e_mail() is not None:
            return f"mailto:{self.e_mail}"
        else:
            return ""

    def to_(self, format="") -> str:
        if self.link_address() == "":
            format = ""
        if format == "md":
            return f"[{self.print_name()}]({self.link_address()})"
        elif format == "rst":
            return f"`{self.print_name()} <{self.link_address()}>`"
        else:
            return self.print_name()


class Publication:
    def __init__(self, orcid: str, put_code: int):
        self.put_code = put_code
        self.orcid = orcid
        self.json = fetch_data(self.orcid, self.put_code)
        self.contributors = self.extract_contributors()

    @property
    def entry_data(self) -> dict:
        return self.json["bulk"][0]["work"]

    def extract_contributors(self) -> list[Person]:
        return [
            Person(entry) for entry in self.entry_data["contributors"]["contributor"]
        ]

    def authors(self) -> list[Person]:
        return [person for person in self.contributors if person.is_autor()]

    def print_authors(self, format: str = "") -> str:
        authors = [f"**{author.to_(format)}**" for author in self.authors()]
        return "; ".join(authors)

    def editors(self) -> list[Person]:
        return [person for person in self.contributors if person.is_editor()]

    def print_editors(self, format: str = "") -> str:
        editors = [f"{editor.to_(format)}" for editor in self.editors()]
        return "; ".join(editors)

    def bibtex(self) -> str:
        return self.entry_data["citation"]["citation-value"]

    def year(self) -> str:
        return self.entry_data["publication-date"]["year"]["value"]

    def title(self) -> str:
        return self.entry_data["title"]["title"]["value"]

    def journal_title(self) -> str:
        return value(self.entry_data, "journal-title")

    def url(self, format="") -> str:
        url: str = value(self.entry_data, "url")
        if url == "":
            return ""
        no_http = url
        if "doi" in url:
            doi_classifier = "doi: "
            doi_start = no_http.find("/10.")
            no_http = no_http[doi_start + 1 :]
        else:
            doi_classifier = ""
            no_http = "Link"
        return f"{doi_classifier}{self.external_link(url, no_http, format)}"

    def external_link(self, url: str, no_http: str, format: str = "md"):
        no_http = no_http.replace("https://", "").replace("http://", "")
        if format == "md":
            return f"[{no_http}]({url})"
        elif format == "rst":
            return f"`{no_http}<{url}>`_"
        else:
            return url

    def _to_(self, format: str) -> str:
        publication = [
            self.print_authors(format),
            f"*{self.title()}*",
            f"{self.journal_title()}",
            self.print_editors(),
            f"{self.url(format)}",
            f"{self.year()}",
        ]
        publication = [entry for entry in publication if entry != ""]
        return ", ".join(publication)

    def to_markdown(self):
        return self._to_("md")

    def to_rst(self) -> str:
        return self._to_("rst")


if __name__ == "__main__":
    orcid = "0009-0008-8267-272X"
    overview_data = fetch_data(orcid)
    put_codes = collect_put_codes(overview_data)
    publications = []
    for code in put_codes:
        publications.append(Publication(orcid, code))

    publications.sort(key=lambda x: int(x.year()), reverse=True)

    year = ""
    for publication in publications:
        if publication.year() == year:
            print(f"# {publication.year()}")
            print()
        print(publication.to_markdown())
        print()
