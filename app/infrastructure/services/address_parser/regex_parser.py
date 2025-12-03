import re
from typing import Dict, Optional

from app.application.dtos.location import ParsedAddressDTO
from app.infrastructure.services.address_parser.base import BaseAddressParser


class RegexAddressParser(BaseAddressParser):
    """
    Универсальный regex-парсер русских адресов.
    Логика: всегда возвращаем ParsedAddressDTO.
    Все внутренние парсеры возвращают dict или None.
    """

    def __init__(self):
        self.street_abbreviations = {
            r"ул\.": "улица",
            r"пр\.": "проспект",
            r"пр-т": "проспект",
            r"ш\.": "шоссе",
            r"пер\.": "переулок",
            r"наб\.": "набережная",
            r"б-р": "бульвар",
            r"ал\.": "аллея",
            r"пл\.": "площадь",
            r"мкр\.": "микрорайон",
            r"г\.": "город",
            r"пос\.": "поселок",
            r"с\.": "село",
            r"д\.": "деревня",
            r"р-н": "район",
        }

        self.not_city_keywords = {
            "россия",
            "область",
            "край",
            "республика",
            "район",
            "округ",
            "автономный",
            "деревня",
            "село",
            "поселок",
            "микрорайон",
            "жилой",
            "спальный",
            "центр",
        }

        self.street_patterns = [
            r"\b(?:ул|улица|пр|проспект|ш|шоссе|пер|переулок|наб|набережная|б-р|бульвар|пл|площадь)\b",
            r"\b(?:дом|д|корпус|корп|строение|стр|квартира|кв)\b",
            r"\d+[а-я]?$",
        ]

    async def parse_address(self, address: str) -> ParsedAddressDTO:
        """Основной метод парсинга"""
        if not address or not address.strip():
            return self._empty_result()

        original_address = address.strip()
        normalized_address = self._normalize_spaces(original_address)

        parsers = [
            self._parse_explicit_with_comma,
            self._parse_explicit_with_city_abbr,
            self._parse_implicit_city_pattern,
            self._parse_street_like_pattern,
        ]

        for parser in parsers:
            result = parser(normalized_address)
            if result and self._is_plausible_result(result):
                return self._finalize_result(result, original_address)

        # fallback — просто улица
        return self._finalize_result(
            {"city": None, "street": self._normalize_street(normalized_address)},
            original_address,
        )

    # ---------------- ПАРСЕРЫ ---------------- #

    def _parse_explicit_with_comma(self, address: str) -> Optional[Dict]:
        patterns = [
            r"^(?P<city>[^,]+?)\s*,\s*(?P<street>.+)$",
            r"^(?P<street>.+?)\s*,\s*(?P<city>[^,]+)$",
        ]
        for pattern in patterns:
            match = re.match(pattern, address, re.IGNORECASE)
            if match:
                city_candidate = self._normalize_city(match.group("city"))
                street_candidate = self._normalize_street(match.group("street"))
                if self._is_likely_city(city_candidate) and self._is_likely_street(
                    street_candidate
                ):
                    return {"city": city_candidate, "street": street_candidate}
        return None

    def _parse_explicit_with_city_abbr(self, address: str) -> Optional[Dict]:
        patterns = [
            r"^(?:г\.|город)\s*(?P<city>[а-яё\s-]{3,}?)(?:\s|$)(?P<street>.+)$",
            r"^(?P<street>.+?)(?:\s|$)(?:г\.|город)\s*(?P<city>[а-яё\s-]{3,})$",
        ]
        for pattern in patterns:
            match = re.match(pattern, address, re.IGNORECASE)
            if match:
                city_candidate = self._normalize_city(match.group("city"))
                street_candidate = self._normalize_street(match.group("street"))
                if self._is_likely_city(city_candidate) and self._is_likely_street(
                    street_candidate
                ):
                    return {"city": city_candidate, "street": street_candidate}
        return None

    def _parse_implicit_city_pattern(self, address: str) -> Optional[Dict]:
        words = address.split()
        if len(words) < 3:
            return None
        for i in range(1, len(words)):
            city_candidate = " ".join(words[:i])
            street_candidate = " ".join(words[i:])
            if self._is_likely_city(city_candidate) and self._is_likely_street(
                street_candidate
            ):
                return {
                    "city": self._normalize_city(city_candidate),
                    "street": self._normalize_street(street_candidate),
                }
        return None

    def _parse_street_like_pattern(self, address: str) -> Optional[Dict]:
        has_street_indicators = any(
            re.search(pattern, address, re.IGNORECASE)
            for pattern in self.street_patterns
        )
        has_city_indicators = (
            re.search(r"\b(?:г\.|город)\b", address, re.IGNORECASE) or "," in address
        )
        if has_street_indicators and not has_city_indicators:
            return {"city": None, "street": self._normalize_street(address)}
        return None

    # ---------------- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ---------------- #

    def _is_likely_city(self, city_candidate: str) -> bool:
        """Проверяет, похоже ли на название города"""
        if not city_candidate or len(city_candidate) < 2:
            return False

        # Проверяем, что это не ключевое слово из списка исключений
        city_lower = city_candidate.lower()
        if any(keyword in city_lower for keyword in self.not_city_keywords):
            return False

        # Город обычно состоит из букв, пробелов и дефисов
        if not re.match(r"^[а-яё\s-]+$", city_candidate, re.IGNORECASE):
            return False

        # Город обычно не содержит цифр (кроме случаев типа "Краснодар-2")
        if re.search(r"\d", city_candidate):
            # Но разрешаем цифры в конце через дефис
            if not re.match(r"^[а-яё\s-]+\-\d+$", city_candidate, re.IGNORECASE):
                return False

        return True

    def _is_likely_street(self, street_candidate: str) -> bool:
        """Проверяет, похоже ли на название улицы"""
        if not street_candidate or len(street_candidate) < 3:
            return False

        # Улица может содержать цифры (номера домов)
        # Проверяем наличие улично-подобных паттернов
        has_street_indicators = any(
            re.search(pattern, street_candidate, re.IGNORECASE)
            for pattern in self.street_patterns
        )

        # Если есть явные указатели улицы - ок
        if has_street_indicators:
            return True

        # Иначе проверяем, что есть хотя бы одно слово и возможно число
        words = street_candidate.split()
        if len(words) == 0:
            return False

        # Хотя бы одно слово должно быть не числом
        non_numeric_words = [
            word for word in words if not word.replace(".", "").isdigit()
        ]
        return len(non_numeric_words) > 0

    def _is_plausible_result(self, result: Dict) -> bool:
        if result.get("city") and len(result["city"]) < 2:
            return False
        if result.get("street") and len(result["street"]) < 3:
            return False
        return True

    def _normalize_city(self, city: str) -> Optional[str]:
        if not city:
            return None
        city = re.sub(r"^(г\.|город)\s*", "", city.strip(), flags=re.IGNORECASE)
        city = re.sub(r"\s+", " ", city).strip()
        return " ".join(word.title() for word in city.split())

    def _normalize_street(self, street: str) -> str:
        if not street:
            return ""
        street = street.strip()
        for abbrev, full in self.street_abbreviations.items():
            street = re.sub(abbrev, full, street, flags=re.IGNORECASE)
        return self._normalize_spaces(street)

    def _normalize_spaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def _finalize_result(self, result: Dict, original_address: str) -> ParsedAddressDTO:
        if result["city"]:
            full_address = f"{result['city']}, {result['street']}"
        else:
            full_address = result["street"]
        return ParsedAddressDTO(
            city=result.get("city"),
            street=result.get("street", ""),
            full_address=full_address or original_address,
        )

    def _empty_result(self) -> ParsedAddressDTO:
        return ParsedAddressDTO(city=None, street="", full_address="")
